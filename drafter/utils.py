class Rect:
    def __init__(self, value=0):
        if isinstance(value, list):
            self.top = value[0]
            self.right = value[1]
            self.bottom = value[2]
            self.left = value[3]
        else:
            self.top = value
            self.right = value
            self.bottom = value
            self.left = value

    def spacing_x(self):
        return self.left + self.right

    def spacing_y(self):
        return self.top + self.bottom
