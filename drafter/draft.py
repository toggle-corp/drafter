import cairo


class Draft:
    def __init__(self, filename):
        self.filename = filename


class ImageDraft(Draft):
    def draw(self, node):
        dummy_surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32,
            16, 16,
        )
        dummy_context = cairo.Context(dummy_surface)
        node.set_context(dummy_context)

        node.set_relative_parent(None)
        node.update_layout()

        if not node.can_draw():
            raise Exception('Invalid node')

        width = node.w + node.margin.spacing_x()
        height = node.h + node.margin.spacing_y()

        surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32,
            width, height,
        )
        ctx = cairo.Context(surface)

        node.set_context(ctx)
        node.draw()

        surface.write_to_png(self.filename)


class PdfDraft(Draft):
    surface = None

    def draw(self, node):
        dummy_surface = cairo.PDFSurface(None, 16, 16)
        dummy_context = cairo.Context(dummy_surface)
        node.set_context(dummy_context)

        node.set_relative_parent(None)
        node.update_layout()

        if not node.can_draw():
            raise Exception('Invalid node')

        width = node.w + node.margin.spacing_x()
        height = node.h + node.margin.spacing_y()

        if not self.surface:
            self.surface = cairo.PDFSurface(
                self.filename,
                width, height,
            )
        else:
            self.surface.set_size(width, height)

        ctx = cairo.Context(self.surface)

        node.set_context(ctx)
        node.draw()

        self.surface.show_page()
        return self
