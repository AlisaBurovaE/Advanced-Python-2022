#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import pickle
import math

SCREEN_DIM = (800, 600)


# =======================================================================================
# Функции для работы с векторами
# =======================================================================================

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


class PolylineRenderer:
    def draw_points(points, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color,
                                 points[p_n].int_pair(),
                                 points[p_n + 1].int_pair(), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(gameDisplay, color,
                                   p.int_pair(), width)


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

    def draw_points(self):
        PolylineRenderer.draw_points(self.points)


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

    def draw_points(self, width=3, color=(255, 255, 255)):
        super().draw_points()
        if self.motion == 'start' or self.motion == 'active':
            PolylineRenderer.draw_points(self.curve_points, "line", width, color)
            if self.motion == 'start':
                self.motion = 'paused'


# =======================================================================================
# Функции отрисовки
# =======================================================================================


def draw_help():
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["E", "More points"])
    data.append(["Q", "Less points"])
    data.append(["", ""])
    data.append(["S", "Save configuration to topsecretdata.txt"])
    data.append(["L", "Load configuration from topsecretdata.txt"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# =======================================================================================
# Функции, отвечающие за расчет сглаживания ломаной
# =======================================================================================


# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")
    pause_text = pygame.font.SysFont('Consolas', 32).render('Pause', True, pygame.color.Color('White'))

    steps = 35
    working = True
    # points = []
    # speeds = []
    knot = Knot(steps)
    show_help = False
    pause = True

    motion = 'start'

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    knot = Knot(steps)
                if event.key == pygame.K_p:
                    pause = not pause
                    knot.motion = 'active'
                if event.key == pygame.K_e:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_q:
                    steps -= 1 if steps > 1 else 0
                if event.key == pygame.K_s:
                    with open("topsecretdata.txt", "wb") as file:
                        pickle.dump(knot, file)
                if event.key == pygame.K_l:
                    try:
                        with open("topsecretdata.txt", "rb") as file:
                            knot = pickle.load(file)
                    except:
                        pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                knot.add_point(Vec2d(event.pos[0], event.pos[1]),
                               Vec2d(random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        knot.set_count(steps)
        knot.draw_points(3, color)

        if pause:
            gameDisplay.blit(pause_text, (100, 100))
            knot.motion = not 'active'

        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
