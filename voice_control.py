import sounddevice as sd
import whisper
from scipy.io.wavfile import write
from car_state import Carstate

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

model = whisper.load_model("base")

result = model.transcribe("recording.wav", language = "ja")

text = result["text"]
print(text)
car = Carstate()

if "開けて" in text:
    car.window_open()

if "閉めて" in text:
    car.window_close()

if "つけて" in text:
    car.wiper_on()

if "消して" in text:
    car.wiper_off()

car.status()