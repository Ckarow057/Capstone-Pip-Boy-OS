import sys

import pygame
import theme

from graphics import redraw
from hardware import HW_EVENT
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


def _scroll_selection(app_state, direction: int):
    """Move the per-screen cursor up/down."""
    if app_state.current_screen == ScreenState.DATA:
        count = len(app_state.quests)
        app_state.selected_quest = (app_state.selected_quest + direction) % count
    elif app_state.current_screen == ScreenState.RADIO:
        count = len(app_state.radio_data["stations"])
        app_state.selected_station = (app_state.selected_station + direction) % count


def _cycle_theme(app_state):
    """Cycle to the next colour theme."""
    app_state.color_theme = (app_state.color_theme + 1) % len(app_state.themes)
    theme.apply_theme(app_state.themes[app_state.color_theme])


def process_input(app_state):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == HW_EVENT:
            action = event.action
            if action == "stat":
                app_state.current_screen = ScreenState.STAT
            elif action == "items":
                app_state.current_screen = ScreenState.ITEMS
            elif action == "data":
                _cycle_data_group(app_state)
            elif action == "scroll_down":
                _scroll_selection(app_state, +1)
            elif action == "scroll_up":
                _scroll_selection(app_state, -1)
            elif action == "theme":
                _cycle_theme(app_state)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_UP:
                _scroll_selection(app_state, -1)
            elif event.key == pygame.K_DOWN:
                _scroll_selection(app_state, +1)
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
            elif event.key == pygame.K_x:
                _cycle_theme(app_state)
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