from drafter.node import Node


class DummyRenderer:
    def render(self, ctx):
        pass


dummy_renderer = DummyRenderer()


class Canvas(Node):
    renderer = dummy_renderer

    def draw_content(self, x, y, w, h):
        self.ctx.save()
        self.ctx.translate(x, y)

        self.renderer.w = w
        self.renderer.h = h
        self.renderer.render(self.ctx)

        self.ctx.restore()
