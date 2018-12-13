import cairo
from gi.repository import Pango, PangoCairo

def get_font(font, font_family, font_size, font_weight):
    """work around for Roboto Condensed not working on OS X"""
    desc = Pango.font_description_from_string(font)

    if font_family is not None:
        font_map = PangoCairo.font_map_get_default()
        new_desc = next(
            (v.list_faces()[0].describe() for v in font_map.list_families()
             if font_family.lower() in v.get_name().lower())
            , None)
        if new_desc:
            desc = new_desc
            desc.set_style(Pango.Style.NORMAL)
            desc.set_weight(Pango.Weight.NORMAL)

    if font_size is not None:
        desc.set_size(font_size * Pango.SCALE)

    if font_weight is not None:
        desc.set_weight(font_weight)

    return desc


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
    CAP_BUTT = cairo.LINE_CAP_BUTT
    CAP_ROUND = cairo.LINE_CAP_ROUND
    CAP_SQUARE = cairo.LINE_CAP_SQUARE

    def __init__(
        self,
        radius=0,
        width=0,
        color=[0, 0, 0, 0],
        line_cap=CAP_BUTT,
        line_dash=[],
    ):
        self.radius = radius
        self.width = width
        self.color = color
        self.line_cap = line_cap
        self.line_dash = line_dash

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
        ctx.set_dash(self.line_dash)
        ctx.set_line_cap(self.line_cap)

        if preserve:
            ctx.stroke_preserve()
        else:
            ctx.stroke()
