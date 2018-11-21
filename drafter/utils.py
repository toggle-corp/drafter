class Rect:
    def __init__(self,
                 value=0,
                 top=None, left=None, right=None, bottom=None):
        self.top = top or value
        self.left = left or value
        self.right = right or value
        self.bottom = bottom or value

    def spacing_x(self):
        return self.left + self.right

    def spacing_y(self):
        return self.top + self.bottom



