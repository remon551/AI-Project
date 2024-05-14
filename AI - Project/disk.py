from color import Color


class Disk:
    def __init__(self, color=None):
        self.color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        self._color = new_color

    def flip(self):
        if self.color == Color.BLACK:
            self.color = Color.WHITE
        elif self.color == Color.WHITE:
            self.color = Color.BLACK
