from Vec2d import Vec2d
from PolylineRenderer import PolylineRenderer
from Polyline import Polyline


class Knot(Polyline):
    def __init__(self, count):
        super().__init__()
        self.curve_points = []
        self.count = count
        self.motion = 'start'

    def set_count(self, count):
        self.count = count
        self.get_knot()

    def get_point(points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + Knot.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(Knot.get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        self.curve_points = []

        if len(self.points) < 3:
            return

        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            self.curve_points.extend(Knot.get_points(ptn, self.count))

    def add_point(self, point: Vec2d, speed: Vec2d):
        super().add_point(point, speed)
        self.get_knot()

    def set_points(self):
        super().set_points()
        self.get_knot()

    def draw_points(self, gameDisplay, width=3, color=(255, 255, 255)):
        super().draw_points(gameDisplay)
        if self.motion == 'start' or self.motion == 'active':
            PolylineRenderer.draw_points(gameDisplay, self.curve_points, "line", width, color)
            if self.motion == 'start':
                self.motion = 'paused'

