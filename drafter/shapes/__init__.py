import math

import cairo
import gi
gi.require_version('Gdk', '3.0')  # noqa
gi.require_version('Pango', '1.0')  # noqa
gi.require_version('PangoCairo', '1.0')  # noqa

from gi.repository import (
    Pango,
    PangoCairo,
    Gdk,
    GdkPixbuf,
)


from drafter import utils

class Shape:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class LineShape(Shape):
    CAP_BUTT = cairo.LINE_CAP_BUTT
    CAP_ROUND = cairo.LINE_CAP_ROUND
    CAP_SQUARE = cairo.LINE_CAP_SQUARE

    color = [1, 0, 0, 1]
    line_width = 1
    line_color = [0, 0, 0, 1]
    line_dash = []
    line_cap = CAP_BUTT

    def draw_stroke(self, ctx):
        ctx.set_line_width(self.line_width)
        ctx.set_source_rgba(*self.line_color)
        ctx.set_dash(self.line_dash)
        ctx.set_line_cap(self.line_cap)
        ctx.stroke()

    def render(self, ctx):
        pass


class Pie(LineShape):
    center = [0, 0]
    angle1 = 0
    angle2 = math.pi / 2
    radius = 8

    def calc_center(self):
        angle = (self.angle2 + self.angle1) / 2
        if self.angle2 < self.angle1:
            angle = -angle

        c = self.center
        ac = [
            c[0] + self.radius * math.cos(angle),
            c[1] + self.radius * math.sin(angle),
        ]

        return [
            (ac[0] + c[0]) / 2,
            (ac[1] + c[1]) / 2,
        ]

    def calc_central_point(self, dist, centroid=None):
        if not centroid:
            centroid = self.calc_center()
        center = self.center

        theta = math.atan2(centroid[1] - center[1], centroid[0] - center[0])
        return [
            center[0] + dist * math.cos(theta),
            center[1] + dist * math.sin(theta),
        ]

    def render(self, ctx):
        ctx.move_to(*self.center)
        ctx.arc(self.center[0],
                self.center[1],
                self.radius,
                self.angle1,
                self.angle2)
        ctx.close_path()
        ctx.set_source_rgba(*self.color)
        ctx.fill_preserve()
        self.draw_stroke(ctx)


class Arc(LineShape):
    center = [0, 0]
    angle1 = 0
    angle2 = math.pi / 2
    radius = 8

    def calc_center(self):
        angle = (self.angle2 + self.angle1) / 2
        if self.angle2 < self.angle1:
            angle = -angle

        return [
            self.center[0] + self.radius * math.cos(angle),
            self.center[1] + self.radius * math.sin(angle),
        ]

    def render(self, ctx):
        ctx.arc(self.center[0],
                self.center[1],
                self.radius,
                self.angle1,
                self.angle2)
        self.draw_stroke(ctx)


class Circle(Arc):
    angle1 = 0
    angle2 = math.pi * 2


class Line(LineShape):
    p1 = [0, 0]
    p2 = [0, 0]

    def render(self, ctx):
        ctx.move_to(*self.p1)
        ctx.line_to(*self.p2)
        self.draw_stroke(ctx)


class Rectangle(LineShape):
    pos = [0, 0]
    size = [0, 0]
    color = [1, 0, 0, 1]

    def render(self, ctx):
        p = self.pos
        s = self.size
        points = [
            [p[0], p[1]],
            [p[0] + s[0], p[1]],
            [p[0] + s[0], p[1] + s[1]],
            [p[0], p[1] + s[1]],
        ]
        ctx.move_to(*points[0])
        for pt in points[1:]:
            ctx.line_to(*pt)
        ctx.close_path()

        ctx.set_source_rgba(*self.color)
        ctx.fill_preserve()

        self.draw_stroke(ctx)


class Polygon(LineShape):
    points = []
    color = [1, 0, 0, 1]

    def render(self, ctx):
        if len(self.points) == 0:
            return

        ctx.move_to(*self.points[0])
        for pt in self.points[1:]:
            ctx.line_to(*pt)
        ctx.close_path()

        ctx.set_source_rgba(*self.color)
        ctx.fill_preserve()

        self.draw_stroke()


class Arrow:
    p1 = [0, 0]
    p2 = [0, 0]
    arrow_angle = 0.6
    arrow_length = 6

    def get_head_vertices(self):
        angle = math.atan2(
            self.p2[1] - self.p1[1],
            self.p2[0] - self.p1[0],
        ) + math.pi

        hx1 = self.p2[0] + \
            self.arrow_length * math.cos(angle - self.arrow_angle)
        hy1 = self.p2[1] + \
            self.arrow_length * math.sin(angle - self.arrow_angle)
        hx2 = self.p2[0] + \
            self.arrow_length * math.cos(angle + self.arrow_angle)
        hy2 = self.p2[1] + \
            self.arrow_length * math.sin(angle + self.arrow_angle)

        return [hx1, hy1], [hx2, hy2]


class OpenArrow(Arrow, LineShape):
    def render(self, ctx):
        hp1, hp2 = self.get_head_vertices()

        ctx.move_to(*self.p1)
        ctx.line_to(*self.p2)

        ctx.line_to(*hp1)
        ctx.move_to(*self.p2)
        ctx.line_to(*hp2)

        self.draw_stroke(ctx)


class SolidArrow(Arrow, LineShape):
    color = [0, 0, 0, 1]

    def render(self, ctx):
        hp1, hp2 = self.get_head_vertices()

        ctx.move_to(*self.p1)
        ctx.line_to(*self.p2)

        self.draw_stroke(ctx)

        ctx.move_to(*self.p2)
        ctx.line_to(*hp1)
        ctx.line_to(*hp2)
        ctx.close_path()

        ctx.set_source_rgba(*self.color)
        ctx.fill()


class String(Shape):
    WORD_WRAP = Pango.WrapMode.WORD
    CHAR_WRAP = Pango.WrapMode.WORD_CHAR
    WORD_CHAR_WRAP = Pango.WrapMode.WORD_CHAR

    LEFT = Pango.Alignment.LEFT
    CENTER = Pango.Alignment.CENTER
    RIGHT = Pango.Alignment.RIGHT

    text = None
    markup = None
    font = 'Arial  8'
    color = [0, 0, 0, 1]
    wrap = False
    wrap_mode = WORD_WRAP
    alignment = LEFT

    pos = [0, 0]
    width = None
    height = None

    font_family = None
    font_size = None
    font_weight = None

    def calc_extents(self, ctx):
        if not self.text and not self.markup:
            return [0, 0]

        layout = PangoCairo.create_layout(ctx)
        layout.set_font_description(utils.get_font(self.font, self.font_family, self.font_size, self.font_weight))
        layout.set_alignment(self.alignment)

        if self.text:
            layout.set_text(self.text, -1)
        if self.markup:
            layout.set_markup(self.markup, -1)

        if not self.wrap:
            layout.set_width(-1)
        elif self.width:
            layout.set_width(self.width * Pango.SCALE)
            layout.set_wrap(self.wrap_mode)

        if self.height:
            layout.set_height(self.height)

        extents = layout.get_extents()[1]
        return [
            extents.width / Pango.SCALE,
            extents.height / Pango.SCALE,
        ]

    def calc_center(self, ctx):
        extents = self.calc_extents(ctx)
        return [
            self.pos[0] + extents[0] / 2,
            self.pos[1] + extents[1] / 2,
        ]

    def repos_to_center(self, ctx):
        extents = self.calc_extents(ctx)
        self.pos[0] -= extents[0] / 2
        self.pos[1] -= extents[1] / 2
        return self

    def render(self, ctx):
        if not self.text and not self.markup:
            return

        ctx.save()
        ctx.translate(self.pos[0], self.pos[1])

        layout = PangoCairo.create_layout(ctx)
        layout.set_font_description(utils.get_font(self.font, self.font_family, self.font_size, self.font_weight))
        layout.set_alignment(self.alignment)

        if self.text:
            layout.set_text(self.text, -1)
        if self.markup:
            layout.set_markup(self.markup, -1)

        if not self.wrap:
            layout.set_width(-1)
        elif self.width:
            layout.set_width(self.width * Pango.SCALE)
            layout.set_wrap(self.wrap_mode)

        if self.height:
            layout.set_height(self.height)

        ctx.set_source_rgba(*self.color)
        PangoCairo.show_layout(ctx, layout)

        ctx.restore()


class Image(Shape):
    filename = None
    width = None
    height = None
    pos = [0, 0]
    center = False
    scale_uniform = False

    def render(self, ctx):
        pb = GdkPixbuf.Pixbuf.new_from_file(self.filename)
        img_w = pb.get_width()
        img_h = pb.get_height()

        w = self.width or img_w
        h = self.height or img_h

        ctx.save()

        scale_x = w / img_w
        scale_y = h / img_h
        if self.scale_uniform:
            if not self.height:
                scale_y = scale_x
            elif not self.width:
                scale_x = scale_y

        ctx.translate(self.pos[0], self.pos[1])
        ctx.scale(scale_x, scale_y)
        ctx.translate(-img_w / 2, -img_h / 2)

        Gdk.cairo_set_source_pixbuf(ctx, pb, 0, 0)
        ctx.paint()

        ctx.restore()
