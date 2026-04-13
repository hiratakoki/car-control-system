import cv2
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions
from mediapipe.tasks.python.vision.core.vision_task_running_mode import VisionTaskRunningMode
import sounddevice as sd
from scipy.io.wavfile import write
import whisper
from car_state import Carstate

MODEL_PATH = "hand_landmarker.task"

options = HandLandmarkerOptions(
    base_options = BaseOptions(model_asset_path = MODEL_PATH),
    running_mode = VisionTaskRunningMode.IMAGE,
    num_hands = 1,
)

cap = cv2.VideoCapture(0)

def is_pointing(landmarks):
    if landmarks[8].y > landmarks[6].y:
        return False
    if landmarks[12].y < landmarks[10].y:
        return False
    if landmarks[16].y < landmarks[14].y:
        return False
    if landmarks[20].y < landmarks[18].y:
        return False
    
    return True

model = whisper.load_model("base")
car = Carstate()

with HandLandmarker.create_from_options(options) as landmarker:
    while cap.isOpened():
        ret, frame  = cap.read()  # カメラから1フレーム取得
        if not ret:
            break

        frame = cv2.flip(frame, 1)  #鏡のように左右反転

        # フレームをMediaPipe用に変換
        mp_image = mp.Image(
            image_format = mp.ImageFormat.SRGB,
            data = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        )

        # 手を検出
        result = landmarker.detect(mp_image)

        # TODO: ここに検出結果の処理を書く
        if result.hand_landmarks:
            hand = result.hand_landmarks[0]
            if is_pointing(hand):
                tip_x = hand[8].x
                if tip_x > 0.5:
                    direction = "RIGHT"
                else:
                    direction = "LEFT"
                cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
                if not pointing_before:
                    # 設定
                    duration = 3        #録音する秒数
                    samplerate = 16000  #サンプルレート

                    # ① 録音開始
                    print("録音開始...")
                    data = sd.rec(duration * samplerate, samplerate = samplerate, channels = 1)

                    # ② 録音が終わるまで待つ
                    sd.wait()

                    # ③ ファイルに保存
                    write("recording.wav", samplerate, data)

                    print("録音完了")

                    result = model.transcribe("recording.wav", language = "ja")

                    text = result["text"]
                    print(text)

                    if "開けて" in text:
                        car.window_open(direction.lower())

                    if "閉めて" in text:
                        car.window_close(direction.lower())

                    car.status()

                pointing_before = True
            else:
                pointing_before = False
        else:
            pointing_before = False

        cv2.imshow("Gesture Control", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
