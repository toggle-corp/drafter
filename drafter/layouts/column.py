from drafter.node import Node


class Column(Node):
    align = 'start'
    justify = 'start'

    def update_layout(self):
        # This is similar to Row but dimensions are swapped

        self.calculate_layout()

        for c in self.children:
            if c.absolute:
                c.update_absolute_layout()

        non_absolute_children = [
            c for c in self.children if not c.absolute
        ]

        if len(non_absolute_children) == 0:
            return

        y = self.y + self.padding.top
        for c in non_absolute_children:
            c.y = y + c.margin.top
            c.update_layout()
            if c.h:
                y += c.h + c.margin.spacing_y()

        if not self.h:
            self.h = y

        total_h = sum([
            c.h + c.margin.spacing_y()
            for c in non_absolute_children
            if not c.absolute and c.h is not None
        ])

        spacing = 0
        if self.justify == 'end':
            y = self.y - self.padding.bottom + self.h - total_h
        elif self.justify == 'center':
            y = self.y + self.h / 2 - total_h / 2
        elif self.justify == 'space-between':
            total_children = sum([
                1 for c in non_absolute_children
                if c.h is not None
            ])
            diff = max(0, (self.h - self.padding.spacing_y()) - total_h)
            spacing = diff / (total_children - 1)
            y = self.y + self.padding.left
        else:
            y = self.y + self.padding.top

        for c in non_absolute_children:
            c.y = y + c.margin.top
            if c.h:
                y += c.h + c.margin.spacing_y() + spacing

        if self.w is None:
            w = 0
            x = self.x + self.padding.left
            for c in non_absolute_children:
                c.x = x + c.margin.left
                c.update_layout()
                if c.w:
                    w = max(w, c.w + c.margin.spacing_x())
            self.w = w

        for c in self.children:
            c.update_layout()

        if self.align == 'end':
            x = self.x - self.padding.right + self.w
        elif self.align == 'center':
            x = self.x + self.w / 2
        else:
            x = self.x + self.padding.left

        for c in non_absolute_children:
            if self.align == 'center' and c.w:
                c.x = x - c.w / 2
            elif self.align == 'end' and c.w:
                c.x = x - c.w - c.margin.right
            else:
                c.x = x + c.margin.left

        for c in self.children:
            c.update_layout()
