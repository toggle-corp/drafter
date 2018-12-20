import gi
gi.require_version('Pango', '1.0')  # noqa
gi.require_version('PangoCairo', '1.0')  # noqa

from gi.repository import Pango, PangoCairo
from drafter.node import Node

from drafter.nodes.image import Image

from drafter import utils

# TODO Reuse pango context instead of using
# create_layout out of cairo context everytime.


class NP_Text(Node):
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


    def calculate_layout(self):
        super().calculate_layout()

        # layout = PangoCairo.create_layout(self.ctx)

        self.h = 10
        self.x = 10
        self.width = 12
        self.height = 25

    def draw_content(self, x, y, w, h):
        self.ctx.save()

        layout = PangoCairo.create_layout(self.ctx)

        from . import np_conv_ctx
        new_c = PangoCairo.create_context(np_conv_ctx.get_pic(self.text))
        self.ctx.set_source_rgba(*self.color)

        PangoCairo.show_layout(new_c, layout)

        self.ctx.restore()


def smart_conv(self):

        from . import np_conv
        cv = np_conv.get_ctx(self.ctx, self.text)
        self.ctx.set_source_rgba(*self.color)
        p = PangoCairo.create_context(self.ctx)
        xxxx = Pango.Context.load_font(p, Pango.font_description_from_string('Mangal'))

        g_list = []
        for info, pos, extent in zip(cv[0], cv[1], cv[2]):
            cp = Pango.GlyphInfo()
            Pango.GlyphInfo.attr = info.cluster

            cp.geometry.width = extent.width
            cp.geometry.x_offset = pos.x_offset
            cp.geometry.y_offset = pos.y_offset

            cp.glyph = info.codepoint

            g_list.append(cp)


        gs = Pango.GlyphString()
        gs.glyphs = g_list

        from gi.repository import HarfBuzz as hb
        # gs.glyphs = conv_ret.buffer_get_glyph_infos
        PangoCairo.show_glyph_string(self.ctx, xxxx, gs)
        # PangoCairo.show_layout(self.ctx, layout)

        self.ctx.restore()
