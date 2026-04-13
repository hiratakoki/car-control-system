class Carstate:
    def __init__(self):
        self.window = {"right": "closed", "left": "closed"}
        self.wiper = "off"

    def window_open(self, side):
        self.window[side] = "open"

    def window_close(self, side):
        self.window[side] = "closed"

    def wiper_on(self):
        self.wiper = "on"

    def wiper_off(self):
        self.wiper = "off"

    def status(self):
        print("=== 車の状態 ===")
        print(f"右の窓: {self.window['right']}")
        print(f"左の窓: {self.window['left']}")
        print(f"ワイパー: {self.wiper}")