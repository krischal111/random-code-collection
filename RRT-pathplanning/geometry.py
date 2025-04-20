class StraightEllipse:
    def __init__(self, a, b, x0, y0):
        self.a = a
        self.b = b
        self.x0 = x0
        self.y0 = y0

    def is_inside(self, x, y):
        return ((x - self.x0) ** 2) / (self.a ** 2) + ((y - self.y0) ** 2) / (self.b ** 2) <= 1