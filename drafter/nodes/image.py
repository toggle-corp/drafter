import os

import cairo
import gi

gi.require_version('Gdk', '3.0')  # noqa
gi.require_version('Rsvg', '2.0')
from gi.repository import Gdk, GdkPixbuf, Rsvg

from drafter.node import Node


class Image(Node):
    """handle image as either svg or other. provide default filename incase provided one is missing"""

    def init(self):
        if not os.path.isfile(self.filename):
            self.filename = self.default_filename

        if self.filename.split('.')[-1] == 'svg':
            # use rsvg to render the cairo context
            handle = Rsvg.Handle()
            svg = handle.new_from_file(self.filename)
            self.pb = svg.get_pixbuf()

        else:
            self.pb = GdkPixbuf.Pixbuf.new_from_file(self.filename)

        # 1052
        # 744


        # self.pb = GdkPixbuf.Pixbuf.new_from_file_at_scale(self.filename, 100, 100, True)

        self.img_w = self.pb.get_width()
        self.img_h = self.pb.get_height()

    def update_layout(self):
        self.calculate_layout()

        img_w = self.img_w + self.padding.spacing_x()
        img_h = self.img_h + self.padding.spacing_y()

        if not self.w:
            if self.h:
                self.w = img_w * self.h / img_h
            else:
                self.w = img_w

        if not self.h:
            self.h = img_h * self.w / img_w

    def draw_content(self, x, y, w, h):
        self.ctx.save()

        scale_x = w / self.img_w
        scale_y = h / self.img_h

        self.ctx.translate(x, y)
        self.ctx.scale(scale_x, scale_y)

        Gdk.cairo_set_source_pixbuf(self.ctx, self.pb, 0, 0)
        self.ctx.paint()

        self.ctx.restore()
