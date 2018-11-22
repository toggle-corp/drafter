from drafter.utils import Rect


class Node:
    def __init__(self, **kwargs):
        self.children = []

        self.x = 0
        self.y = 0
        self.width = None
        self.height = None

        self.top = None
        self.left = None
        self.bottom = None
        self.right = None

        self.w = None
        self.h = None
        self.bg_color = None

        self.margin = Rect()
        self.padding = Rect()
        self.parent = None

        self.absolute = False
        self.relative = False
        self.relative_parent = None

        for key, value in kwargs.items():
            setattr(self, key, value)

    def add(self, *nodes):
        for node in nodes:
            if node.parent:
                raise Exception('Node already added to another parent')
            node.parent = self
            self.children.append(node)
        return self

    def set_relative_parent(self, relative_parent):
        self.relative_parent = relative_parent
        if self.relative:
            [c.set_relative_parent(self) for c in self.children]
            return

        [c.set_relative_parent(relative_parent) for c in self.children]

    def update_absolute_layout(self):
        self.calculate_layout()

        if self.relative_parent:
            if self.left is not None:
                self.x = self.relative_parent.x \
                    + self.left + self.margin.left
            elif self.right is not None:
                self.x = self.relative_parent.x + self.relative_parent.w \
                    - self.right - self.margin.right - self.w

            if self.top is not None:
                self.y = self.relative_parent.y \
                    + self.top + self.margin.top
            elif self.bottom is not None:
                self.y = self.relative_parent.y + self.relative_parent.h \
                    - self.bottom - self.margin.bottom - self.h
        self.update_layout()

    def calculate_layout(self):
        parent_w = self.parent and self.parent.w
        parent_h = self.parent and self.parent.h

        if isinstance(self.width, str):
            w = self.width
            if '%' in w:
                if not parent_w:
                    return
                w = w.replace('%', '* {} / 100'.format(parent_w))

            self.w = eval(w)

        else:
            self.w = self.width

        if isinstance(self.height, str):
            h = self.height
            if '%' in h:
                if not parent_h:
                    return
                h = h.replace('%', '* {} / 100'.format(parent_h))

            self.h = eval(h)

        else:
            self.h = self.height

    def update_layout(self):
        pass

    def can_draw(self):
        return (
            self.w is not None and
            self.h is not None
        )

    def draw(self, ctx):
        pass

    def draw_complete(self, ctx):
        if self.bg_color:
            ctx.set_source_rgba(*self.bg_color)
            ctx.rectangle(self.x, self.y, self.w, self.h)
            ctx.fill()

        self.draw(ctx)
        [
            c.draw_complete(ctx)
            for c in self.children
            if c.can_draw()
        ]
