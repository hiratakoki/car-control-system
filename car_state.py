class Carstate:
    def __init__(self):
        self.window = "closed"
        self.wiper = "off"

    def window_open(self):
        self.window = "open"

    def window_close(self):
        self.window = "closed"

    def wiper_on(self):
        self.wiper = "on"

    def wiper_off(self):
        self.wiper = "off"

    def status(self):
        print("=== 車の状態 ===")
        print(f"窓: {self.window}")
        print(f"ワイパー: {self.wiper}")