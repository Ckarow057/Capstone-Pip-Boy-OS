import sys

import pygame

from graphics import redraw
from state import ScreenState

_DATA_GROUP = (ScreenState.DATA, ScreenState.MAP, ScreenState.RADIO)


def _cycle_screen(app_state, direction: int):
    screens = list(ScreenState)
    idx = screens.index(app_state.current_screen)
    app_state.current_screen = screens[(idx + direction) % len(screens)]


def _cycle_data_group(app_state):
    """Button 3 behaviour: enter DATA group or step through DATA→MAP→RADIO."""
    if app_state.current_screen not in _DATA_GROUP:
        app_state.current_screen = ScreenState.DATA
    else:
        idx = _DATA_GROUP.index(app_state.current_screen)
        app_state.current_screen = _DATA_GROUP[(idx + 1) % len(_DATA_GROUP)]


def process_input(app_state):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_RIGHT:
                _cycle_screen(app_state, +1)
            elif event.key == pygame.K_LEFT:
                _cycle_screen(app_state, -1)
            elif event.unicode == '1':
                app_state.current_screen = ScreenState.STAT
            elif event.unicode == '2':
                app_state.current_screen = ScreenState.ITEMS
            elif event.unicode == '3':
                _cycle_data_group(app_state)
            elif event.unicode == '4':
                app_state.current_screen = ScreenState.MAP
            elif event.unicode == '5':
                app_state.current_screen = ScreenState.RADIO
    return True


def update(app_state):
    app_state.animation.update(pygame.time.get_ticks())


def run(ui, app_state):
    running = True

    while running:
        running = process_input(app_state)
        update(app_state)
        redraw(ui.screen, ui, app_state)
        ui.clock.tick(ui.fps)

    pygame.quit()
    sys.exit()