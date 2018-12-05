from drafter.node import Node


class Row(Node):
    align = 'start'
    justify = 'start'

    # TODO: If we separate update_layout into w and h dimensions,
    # the alogrithm will be more optimized and faster.
    def update_layout(self):
        # Update w and h from mathematical expressions to single
        # number, resolving % values.
        self.calculate_layout()

        non_absolute_children = [
            c for c in self.children if not c.absolute
        ]

        if len(non_absolute_children) == 0:
            return

        # If w is not known, calculate it as total of children's w.
        x = self.x + self.padding.left
        for c in non_absolute_children:
            c.x = x + c.margin.left
            if not c.w:
                c.update_layout()
            if c.w:
                x += c.w + c.margin.spacing_x()

        if not self.w:
            self.w = x - self.x + self.padding.right

        # Next calculate x of children based on justify:

        total_w = sum([
            c.w + c.margin.spacing_x()
            for c in non_absolute_children
            if c.w is not None
        ])

        spacing = 0
        if self.justify == 'end':
            x = self.x - self.padding.right + self.w - total_w
        elif self.justify == 'center':
            x = self.x + self.w / 2 - total_w / 2
        elif self.justify == 'space-between':
            total_children = sum([
                1 for c in non_absolute_children
                if c.w is not None
            ])
            diff = max(0, (self.w - self.padding.spacing_x()) - total_w)
            spacing = diff / (total_children - 1)
            x = self.x + self.padding.left
        else:
            x = self.x + self.padding.left

        for c in non_absolute_children:
            c.x = x + c.margin.left
            if c.w:
                x += c.w + c.margin.spacing_x() + spacing

        # Now do similar to h
        if self.h is None:
            h = 0
            y = self.y + self.padding.top
            for c in non_absolute_children:
                c.y = y + c.margin.top
                if not c.h:
                    c.update_layout()
                if c.h:
                    h = max(h, c.h + c.margin.spacing_y())
            self.h = h + self.padding.bottom

        if self.align == 'end':
            y = self.y - self.padding.bottom + self.h
        elif self.align == 'center':
            y = self.y + self.h / 2
        else:
            y = self.y + self.padding.top

        for c in non_absolute_children:
            if self.align == 'center' and c.h:
                c.y = y - c.h / 2
            elif self.align == 'end' and c.h:
                c.y = y - c.h - c.margin.bottom
            else:
                c.y = y + c.margin.top

        for c in self.children:
            if c.absolute:
                c.update_absolute_layout()
            c.update_layout()
