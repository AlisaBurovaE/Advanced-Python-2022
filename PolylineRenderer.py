from Vec2d import *
import pygame

class PolylineRenderer:
    def draw_points(gameDisplay, points, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color,
                                 points[p_n].int_pair(),
                                 points[p_n + 1].int_pair(), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(gameDisplay, color,
                                   p.int_pair(), width)

