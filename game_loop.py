import sys

import pygame

from graphics import redraw


def process_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return False
    return True


def update(app_state):
    app_state.animation.update(pygame.time.get_ticks())


def run(ui, app_state):
    running = True

    while running:
        running = process_input()
        update(app_state)
        redraw(ui.screen, ui, app_state)
        ui.clock.tick(ui.fps)

    pygame.quit()
    sys.exit()