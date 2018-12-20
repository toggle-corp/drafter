import sys
import os
import math
# import freetype2 as freetype # use Qahirah instance
import qahirah as qah
from qahirah import \
    CAIRO, \
    Colour, \
    Glyph, \
    Vector

import gi
gi.require_version('Pango', '1.0')  # noqa
gi.require_version('PangoCairo', '1.0')  # noqa
from gi.repository import Pango, PangoCairo

ft = qah.get_ft_lib()
import fribidi as fb
from fribidi import \
    FRIBIDI as FB
import harfbuzz as hb

def get_pic(txt):



    text_size = 36
    buf = hb.Buffer.create()
    ft_face = ft.find_face("Mangal")
    ft_face.set_char_size(size = text_size, resolution = qah.base_dpi)
    hb_font = hb.Font.ft_create(ft_face)

    reordered = fb.ReorderLine \
      (
        text_line = txt,
        base_dir = FB.PAR_LTR
      )


    glyphs = []
    glyph_pos = Vector(0, 0)
    for substr, pos1, pos2, level in reordered.each_embedding_run(vis_order = False) :
        buf.reset()
        buf.add_str(substr)
        buf.guess_segment_properties()
        hb.shape(hb_font, buf)
        new_glyphs, end_glyph_pos = buf.get_glyphs(glyph_pos)
        glyph_pos = end_glyph_pos
        glyphs.extend(new_glyphs)
    #end for

    qah_face = qah.FontFace.create_for_ft_face(ft_face)
    glyph_extents = \
        (qah.Context.create_for_dummy()
            .set_font_face(qah_face)
            .set_font_size(text_size)
            .glyph_extents(glyphs)
        )
    figure_bounds = math.ceil(glyph_extents.bounds)
    pix = qah.ImageSurface.create \
      (
        format = CAIRO.FORMAT_RGB24,
        dimensions = figure_bounds.dimensions
      )

    (qah.Context.create(pix)
        .translate(- figure_bounds.topleft)
        .set_source_colour(Colour.grey(1))
        .paint()
        .set_source_colour(Colour.grey(0))
        .set_font_face(qah_face)
        .set_font_size(text_size)
        .show_glyphs(glyphs)
    )
    return qah.Context

    pix.flush().write_to_png('./out.png')