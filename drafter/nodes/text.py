import gi
gi.require_version('Pango', '1.0')  # noqa
gi.require_version('PangoCairo', '1.0')  # noqa

from gi.repository import Pango, PangoCairo
from drafter.node import Node


class Text(Node):
    WORD_WRAP = Pango.WrapMode.WORD
    CHAR_WRAP = Pango.WrapMode.WORD_CHAR
    WORD_CHAR_WRAP = Pango.WrapMode.WORD_CHAR

    text = None
    markup = None
    font = 'Arial  8'
    color = [0, 0, 0, 1]
    wrap = False
    wrap_mode = WORD_WRAP

    def calculate_layout(self):
        super().calculate_layout()

        if not self.text and not self.markup:
            return

        if not self.w or not self.h:
            layout = PangoCairo.create_layout(self.ctx)
            desc = Pango.font_description_from_string(self.font)
            layout.set_font_description(desc)

            if self.text:
                layout.set_text(self.text, -1)
            if self.markup:
                layout.set_markup(self.markup, -1)

            extents = layout.get_extents()[1]

        if not self.w:
            self.w = (extents.width / Pango.SCALE + self.padding.spacing_x())
        elif self.wrap:
            w = self.w - self.padding.spacing_x()
            layout.set_width(w * Pango.SCALE)
            layout.set_wrap(self.wrap_mode)

        if not self.h:
            self.h = (extents.height / Pango.SCALE + self.padding.spacing_y())

    def draw_content(self, x, y, w, h):
        if not self.text and not self.markup:
            return

        self.ctx.save()
        self.ctx.translate(x, y)

        layout = PangoCairo.create_layout(self.ctx)
        desc = Pango.font_description_from_string(self.font)
        layout.set_font_description(desc)

        if self.text:
            layout.set_text(self.text, -1)
        if self.markup:
            layout.set_markup(self.markup, -1)

        if not self.wrap:
            layout.set_width(-1)
        elif w > 0:
            layout.set_width(w * Pango.SCALE)
            layout.set_wrap(self.wrap_mode)

        if h > 0:
            layout.set_height(h)

        self.ctx.set_source_rgba(*self.color)
        PangoCairo.show_layout(self.ctx, layout)

        self.ctx.restore()
