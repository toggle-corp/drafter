from drafter.draft import PdfDraft
from drafter.nodes import Text
from drafter.layouts import Column
from drafter.utils import Rect

import cairo
import gi
gi.require_version('PangoCairo', '1.0')  # noqa

from gi.repository import (
    Pango,
    PangoCairo,
)

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1000, 1000)
context = cairo.Context(surface)
layout = PangoCairo.create_layout(context)

layout.set_wrap(Pango.WrapMode.WORD)
layout.set_font_description(Pango.FontDescription("Arial 10"))
layout.set_text("The Quick Brown Fox Jumps Over The Piqued Gymnast", -1)

PangoCairo.update_layout(context, layout)
PangoCairo.show_layout(context, layout)

context.show_page()

1