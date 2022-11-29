from Vec2d import Vec2d
from PolylineRenderer import PolylineRenderer


class Polyline:
    def __init__(self):
        self.points = []
        self.speeds = []

    def add_point(self, point: Vec2d, speed: Vec2d):
        self.points.append(point)
        self.speeds.append(speed)

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]

            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p].x *= -1

            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p].y *= -1

    def draw_points(self, gameDisplay):
        PolylineRenderer.draw_points(gameDisplay, self.points)

