class Rect:
    def __init__(self, value=0):
        if isinstance(value, list):
            self.top = value[0]
            self.right = value[1]
            self.bottom = value[2]
            self.left = value[3]
        else:
            self.top = value
            self.right = value
            self.bottom = value
            self.left = value

    def spacing_x(self):
        return self.left + self.right

    def spacing_y(self):
        return self.top + self.bottom


class Border:
    def __init__(
        self,
        radius=0,
        width=0,
        color=[0, 0, 0, 0],
    ):
        self.radius = radius
        self.width = width
        self.color = color

    def draw(self, ctx, x, y, w, h, preserve=True):
        r = self.radius
        ctx.move_to(x+r, y)
        ctx.line_to(x+w-r, y)
        ctx.curve_to(x+w, y, x+w, y, x+w, y+r)
        ctx.line_to(x+w, y+h-r)
        ctx.curve_to(x+w, y+h, x+w, y+h, x+w-r, y+h)
        ctx.line_to(x+r, y+h)
        ctx.curve_to(x, y+h, x, y+h, x, y+h-r)
        ctx.line_to(x, y+r)
        ctx.curve_to(x, y, x, y, x+r, y)

        ctx.set_line_width(self.width)
        ctx.set_source_rgba(*self.color)
        if preserve:
            ctx.stroke_preserve()
        else:
            ctx.stroke()
