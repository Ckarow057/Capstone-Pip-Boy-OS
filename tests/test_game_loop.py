"""Unit tests for game_loop.py non-hardware behavior.

These tests stub pygame/hardware dependencies so they can run anywhere.
"""

import importlib
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import state as _real_state


# --- Build stubs before importing game_loop ---
_pygame_event_stub = types.ModuleType("pygame.event")
_pygame_event_stub.get = MagicMock(return_value=[])

_pygame_time_stub = types.ModuleType("pygame.time")
_pygame_time_stub.get_ticks = MagicMock(return_value=123)

_pygame_stub = types.ModuleType("pygame")
_pygame_stub.QUIT = 12
_pygame_stub.KEYDOWN = 13
_pygame_stub.K_ESCAPE = 27
_pygame_stub.K_UP = 273
_pygame_stub.K_DOWN = 274
_pygame_stub.K_RIGHT = 275
_pygame_stub.K_LEFT = 276
_pygame_stub.K_x = 120
_pygame_stub.event = _pygame_event_stub
_pygame_stub.time = _pygame_time_stub
_pygame_stub.quit = MagicMock()

_hardware_stub = types.ModuleType("hardware")
_hardware_stub.HW_EVENT = 99

_graphics_stub = types.ModuleType("graphics")
_graphics_stub.redraw = MagicMock()


sys.modules["pygame"] = _pygame_stub
sys.modules["pygame.event"] = _pygame_event_stub
sys.modules["pygame.time"] = _pygame_time_stub
sys.modules["hardware"] = _hardware_stub
sys.modules["graphics"] = _graphics_stub

import game_loop

importlib.reload(game_loop)

_ScreenState = _real_state.ScreenState


def _evt(event_type, **kwargs):
    defaults = {"type": event_type, "key": None, "unicode": "", "action": None}
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def _app_state(**overrides):
    base = dict(
        current_screen=_ScreenState.STAT,
        quests=[{"name": "q1"}, {"name": "q2"}, {"name": "q3"}],
        selected_quest=0,
        radio_data={"stations": [{"name": "s1"}, {"name": "s2"}]},
        selected_station=0,
        color_theme=0,
        themes=[{"name": "green"}, {"name": "amber"}],
    )
    base.update(overrides)
    return SimpleNamespace(**base)


class TestGameLoopHelpers(unittest.TestCase):
    def setUp(self):
        self.theme_patcher = patch.object(game_loop.theme, "apply_theme")
        self.apply_theme_mock = self.theme_patcher.start()

    def tearDown(self):
        self.theme_patcher.stop()

    def test_cycle_screen_wraps_both_directions(self):
        app_state = _app_state(current_screen=_ScreenState.STAT)
        game_loop._cycle_screen(app_state, -1)
        self.assertEqual(app_state.current_screen, _ScreenState.RADIO)

        game_loop._cycle_screen(app_state, +1)
        self.assertEqual(app_state.current_screen, _ScreenState.STAT)

    def test_cycle_data_group_enters_and_steps_group(self):
        app_state = _app_state(current_screen=_ScreenState.ITEMS)

        game_loop._cycle_data_group(app_state)
        self.assertEqual(app_state.current_screen, _ScreenState.DATA)

        game_loop._cycle_data_group(app_state)
        self.assertEqual(app_state.current_screen, _ScreenState.MAP)

        game_loop._cycle_data_group(app_state)
        self.assertEqual(app_state.current_screen, _ScreenState.RADIO)

        game_loop._cycle_data_group(app_state)
        self.assertEqual(app_state.current_screen, _ScreenState.DATA)

    def test_scroll_selection_wraps_for_data_and_radio(self):
        app_state = _app_state(current_screen=_ScreenState.DATA, selected_quest=0)
        game_loop._scroll_selection(app_state, -1)
        self.assertEqual(app_state.selected_quest, 2)

        app_state.current_screen = _ScreenState.RADIO
        app_state.selected_station = 0
        game_loop._scroll_selection(app_state, -1)
        self.assertEqual(app_state.selected_station, 1)

    def test_cycle_theme_updates_index_and_applies_palette(self):
        app_state = _app_state(color_theme=0, themes=[{"id": 1}, {"id": 2}, {"id": 3}])
        game_loop._cycle_theme(app_state)

        self.assertEqual(app_state.color_theme, 1)
        self.apply_theme_mock.assert_called_once_with({"id": 2})


class TestProcessInput(unittest.TestCase):
    def setUp(self):
        _pygame_event_stub.get.reset_mock(return_value=True)
        _pygame_event_stub.get.return_value = []
        self.theme_patcher = patch.object(game_loop.theme, "apply_theme")
        self.apply_theme_mock = self.theme_patcher.start()

    def tearDown(self):
        self.theme_patcher.stop()

    def test_quit_event_stops_loop(self):
        _pygame_event_stub.get.return_value = [_evt(_pygame_stub.QUIT)]
        app_state = _app_state()

        keep_running = game_loop.process_input(app_state)
        self.assertFalse(keep_running)

    def test_escape_key_stops_loop(self):
        _pygame_event_stub.get.return_value = [_evt(_pygame_stub.KEYDOWN, key=_pygame_stub.K_ESCAPE)]
        app_state = _app_state()

        keep_running = game_loop.process_input(app_state)
        self.assertFalse(keep_running)

    def test_number_key_switches_to_radio(self):
        _pygame_event_stub.get.return_value = [_evt(_pygame_stub.KEYDOWN, unicode="5")]
        app_state = _app_state(current_screen=_ScreenState.STAT)

        keep_running = game_loop.process_input(app_state)

        self.assertTrue(keep_running)
        self.assertEqual(app_state.current_screen, _ScreenState.RADIO)

    def test_hardware_theme_action_cycles_theme(self):
        _pygame_event_stub.get.return_value = [_evt(_hardware_stub.HW_EVENT, action="theme")]
        app_state = _app_state(color_theme=1, themes=[{"id": 1}, {"id": 2}])

        keep_running = game_loop.process_input(app_state)

        self.assertTrue(keep_running)
        self.assertEqual(app_state.color_theme, 0)
        self.apply_theme_mock.assert_called_once_with({"id": 1})


if __name__ == "__main__":
    unittest.main()