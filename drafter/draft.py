from drafter.dimens import (
    px,
    px_per_inches,
    set_dpi,
    set_multiplier,
)
import cairo


class Draft:
    def __init__(
            self,
            filename,
            scale=1.0,
            units=px,
            dpi=px_per_inches,
    ):
        self.filename = filename
        self.scale = scale
        self.units = px
        self.dpi = dpi

    def draw(self, root_node):
        set_dpi(self.dpi)

        # call to units() require a multiplier value so
        # reset it to 1 before setting it to actual value.
        set_multiplier(1)
        set_multiplier(1 / self.units(1))

        node = root_node.clone()

        dummy_surface = self.get_dummy_surface()
        dummy_context = cairo.Context(dummy_surface)
        node.set_context(dummy_context)

        node.x = node.margin.left
        node.y = node.margin.top
        node.set_relative_parent(None)
        node.update_layout()

        if not node.can_draw():
            raise Exception('Invalid node')

        width = node.w + node.margin.spacing_x()
        height = node.h + node.margin.spacing_y()

        # All calculations are done in pixels
        # but if user is assuming a different units,
        # just scale accordingly.
        scale = self.scale * self.units(1)

        width *= scale
        height *= scale

        surface = self.get_surface(width, height)
        ctx = cairo.Context(surface)

        node.set_context(ctx)
        ctx.scale(scale, scale)
        node.draw()

        self.finish_drawing(surface)
        return self


class ImageDraft(Draft):
    def get_dummy_surface(self):
        return cairo.ImageSurface(
            cairo.FORMAT_ARGB32,
            16, 16,
        )

    def get_surface(self, width, height):
        return cairo.ImageSurface(
            cairo.FORMAT_ARGB32,
            width, height,
        )

    def finish_drawing(self, surface):
        surface.write_to_png(self.filename)


class PdfDraft(Draft):
    surface = None
    dummy_surface = None

    def get_dummy_surface(self):
        if not self.dummy_surface:
            self.dummy_surface = cairo.PDFSurface(
                None,
                16, 16,
            )
        return self.dummy_surface

    def get_surface(self, width, height):
        if not self.surface:
            self.surface = cairo.PDFSurface(
                self.filename,
                width, height,
            )
        else:
            self.surface.set_size(width, height)
        return self.surface

    def finish_drawing(self, surface):
        surface.show_page()
