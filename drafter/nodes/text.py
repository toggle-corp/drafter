import gi
gi.require_version('Pango', '1.0')  # noqa
gi.require_version('PangoCairo', '1.0')  # noqa

from gi.repository import Pango, PangoCairo
from drafter.node import Node

from drafter import utils


# TODO Reuse pango context instead of using
# create_layout out of cairo context everytime.


class Text(Node):
    WORD_WRAP = Pango.WrapMode.WORD
    CHAR_WRAP = Pango.WrapMode.WORD_CHAR
    WORD_CHAR_WRAP = Pango.WrapMode.WORD_CHAR

    NORMAL = Pango.Weight.NORMAL
    BOLD = Pango.Weight.BOLD

    LEFT = Pango.Alignment.LEFT
    CENTER = Pango.Alignment.CENTER
    RIGHT = Pango.Alignment.RIGHT

    TOP = 9090
    MIDDLE = 9099
    BOTTOM = 9900

    text = None
    markup = None
    font = 'Arial  8'
    color = [0, 0, 0, 1]
    wrap_mode = WORD_WRAP
    alignment = LEFT
    vertical_alignment = TOP
    line_spacing = None

    font_family = None
    font_size = None
    font_weight = None
    font_stretch = None

    auto_scale_height = False

    def calculate_layout(self):
        super().calculate_layout()

        if not self.text and not self.markup:
            return

        layout = PangoCairo.create_layout(self.ctx)
        # if self.font_size:
        #     self.font_size*=.991
        layout.set_font_description(utils.get_font(self.font, self.font_family, self.font_size, self.font_weight, self.font_stretch))
        layout.set_alignment(self.alignment)

        if self.text:
            #TODO: nan!!
            layout.set_text(str(self.text), -1)
        if self.markup:
            layout.set_markup(self.markup, -1)
        if self.line_spacing is not None:
            layout.set_spacing(self.line_spacing * Pango.SCALE)

        if self.w is None:
            extents = layout.get_extents()[1]
            extents = [
                extents.width / Pango.SCALE,
                extents.height / Pango.SCALE,
            ]
            self.extents = extents
            self.w = (extents[0] + self.padding.spacing_x())
        else:
            w = self.w - self.padding.spacing_x()
            layout.set_width(w * Pango.SCALE)
            layout.set_wrap(self.wrap_mode)
            extents = layout.get_extents()[1]
            extents = [
                extents.width / Pango.SCALE,
                extents.height / Pango.SCALE,
            ]
            self.extents = extents

        if self.h is None:
            self.h = (extents[1] + self.padding.spacing_y())

    def draw_content(self, x, y, w, h):
        if not self.text and not self.markup:
            return

        self.ctx.save()
        if self.vertical_alignment == Text.BOTTOM:
            self.ctx.translate(x, y + h - self.extents[1])
        elif self.vertical_alignment == Text.MIDDLE:
            self.ctx.translate(x, y + h / 2 - self.extents[1] / 2)
        else:
            self.ctx.translate(x, y)

        layout = PangoCairo.create_layout(self.ctx)

        desc = utils.get_font(self.font, self.font_family, self.font_size, self.font_weight, self.font_stretch)
        layout.set_font_description(desc)
        layout.set_alignment(self.alignment)

        if self.text:
            #TODO: nan!!
            layout.set_text(str(self.text), -1)
        if self.markup:
            layout.set_markup(self.markup, -1)
        if self.line_spacing is not None:
            layout.set_spacing(self.line_spacing * Pango.SCALE)

        if not w:
            layout.set_width(-1)
        else:
            layout.set_width(w * Pango.SCALE)
            layout.set_wrap(self.wrap_mode)

        if h > 0:
            layout.set_height(h)

        if self.auto_scale_height:
            #WIP!!
            xbearing, ybearing, width, height, xadvance, yadvance = self.ctx.text_extents('DFADSF')
            print('height ', h)
            print('ext h', self.extents[1])
            print('width ', w)
            print('ext w', self.extents[0])

            # print('ext w', self.extents[0])
            print()
            # print('t', height)
            # w / self.extents[0] if w and w < self.extents[0] else 1
            # h / self.extents[1] if h and h < self.extents[1] else 1

            self.ctx.scale(1, h / self.extents[1] if h and h < self.extents[1] else 1)

        self.ctx.set_source_rgba(*self.color)
        PangoCairo.show_layout(self.ctx, layout)

        self.ctx.restore()
