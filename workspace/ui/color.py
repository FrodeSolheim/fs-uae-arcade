import fsui


class Color(fsui.Color):
    def __init__(self, red, green, blue, alpha=0xFF):
        super().__init__(red, green, blue, alpha)
