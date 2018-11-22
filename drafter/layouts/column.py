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

        if self.h is None:
            h = 0
            y = self.y
            for c in non_absolute_children:
                c.y = y + c.margin.top
                c.update_layout()
                if c.h is None:
                    raise Exception('Node layout cannot be calculated')

                y += c.h + c.margin.spacing_y()
                h = c.y + c.h + c.margin.spacing_y()
            self.h = h

        for c in self.children:
            c.update_layout()

        total_h = sum([
            c.h + c.margin.spacing_y()
            for c in non_absolute_children
            if not c.absolute and c.h is not None
        ])

        if self.justify == 'end':
            y = self.y + self.h - total_h
        elif self.justify == 'center':
            y = self.y + self.h / 2 - total_h / 2
        else:
            y = self.y

        for c in non_absolute_children:
            c.y = y + c.margin.top
            if c.h:
                y += c.h + c.margin.spacing_y()

        if self.w is None:
            w = 0
            x = self.x
            for c in non_absolute_children:
                c.x = x + c.margin.left
                c.update_layout()
                if c.w is None:
                    raise Exception('Node layout cannot be calculated')

                w = max(w, c.x + c.w + c.margin.spacing_x())
            self.w = w

        for c in self.children:
            c.update_layout()

        if self.align == 'end':
            x = self.x + self.w
        elif self.align == 'center':
            x = self.x + self.w / 2
        else:
            x = self.x

        for c in non_absolute_children:
            if self.align == 'center' and c.w:
                c.x = x - c.w / 2
            elif self.align == 'end' and c.w:
                c.x = x - c.w - c.margin.right
            else:
                c.x = x + c.margin.left

        for c in self.children:
            c.update_layout()
