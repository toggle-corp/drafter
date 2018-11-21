import cairo


class Draft:
    def __init__(self, node):
        node.set_relative_parent(None)
        node.update_layout()
        if not node.can_draw():
            raise Exception('Invalid node')

        width = node.x + node.w
        height = node.y + node.h

        surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32,
            width, height
        )

        ctx = cairo.Context(surface)
        node.draw_complete(ctx)
        self.ctx = ctx
        self.surface = surface

    def save(self, filename):
        self.surface.write_to_png(filename)
