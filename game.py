#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import pickle
import math

SCREEN_DIM = (800, 600)

from Vec2d import Vec2d
from Knot import Knot

# =======================================================================================
# Функции для работы с векторами
# =======================================================================================

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
        knot.draw_points(gameDisplay, 3, color)

        if pause:
            gameDisplay.blit(pause_text, (100, 100))
            knot.motion = not 'active'

        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
