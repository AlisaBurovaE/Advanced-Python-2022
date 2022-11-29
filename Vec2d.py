
class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other_vector):
        return Vec2d(other_vector.x + self.x, other_vector.y + self.y)

    def __sub__(self, other_vector):
        return Vec2d(other_vector.x - self.x, other_vector.y - self.y)

    def __mul__(self, scalar):
        return Vec2d(scalar * self.x, scalar * self.y)

    def __len__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def int_pair(self):
        return int(self.x), int(self.y)

