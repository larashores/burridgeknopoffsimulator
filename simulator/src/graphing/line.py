import colorsys


class Line:
    last_hue = 0

    def __init__(self, x, label=None, *, color=None):
        self.x = x
        self.label = label
        self.color = color

    @staticmethod
    def reset_color():
        Line.last_hue = 0

    @staticmethod
    def _next_color():
        hue = Line.last_hue / 255
        Line.last_hue = (Line.last_hue + 45) % 255
        return colorsys.hsv_to_rgb(hue, 1.0, 1.0)

    def draw(self, axis, _x_log, _y_log):
        color = self.color if self.color else self._next_color()
        line = axis.axvline(x=self.x, color=color)
        if self.label:
            line.set_label(self.label)
        return line
