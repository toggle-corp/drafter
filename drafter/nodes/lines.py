import cairo
from drafter.node import Node


class Line(Node):
    CAP_BUTT = cairo.LINE_CAP_BUTT
    CAP_ROUND = cairo.LINE_CAP_ROUND
    CAP_SQUARE = cairo.LINE_CAP_SQUARE

    color = [0, 0, 0, 1]
    dash = []
    cap = CAP_BUTT

    def draw_stroke(self):
        self.ctx.set_source_rgba(*self.color)
        self.ctx.set_dash(self.dash)
        self.ctx.set_line_cap(self.cap)
        self.ctx.stroke()


class Hr(Line):
    def draw_content(self, x, y, w, h):
        p1 = [x, y]
        p2 = [x + w, y]
        self.ctx.set_line_width(h)
        self.ctx.move_to(*p1)
        self.ctx.line_to(*p2)
        self.draw_stroke()


class Vr(Line):
    def draw_content(self, x, y, w, h):
        p1 = [x, y]
        p2 = [x, y + h]
        self.ctx.set_line_width(w)
        self.ctx.move_to(*p1)
        self.ctx.line_to(*p2)
        self.draw_stroke()
