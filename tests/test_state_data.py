"""Unit tests for state.py and data_loader.py."""

import math
import unittest
from unittest.mock import MagicMock, mock_open, patch

import data_loader
import state


class TestAnimationState(unittest.TestCase):
    def test_update_advances_and_bounds_values(self):
        anim = state.AnimationState()

        anim.update(current_ticks=0)

        self.assertEqual(anim.scan_line_offset, 1)
        self.assertGreaterEqual(anim.flicker_intensity, 0.0)
        self.assertLessEqual(anim.flicker_intensity, 0.5)
        self.assertGreaterEqual(anim.glitch_intensity, 0.0)
        self.assertLessEqual(anim.glitch_intensity, 1.0)
        self.assertTrue(anim.glitch_active)

    def test_update_sets_glitch_inactive_outside_window(self):
        anim = state.AnimationState(glitch_interval_ms=3000, glitch_window_ms=50)
        anim.update(current_ticks=100)
        self.assertFalse(anim.glitch_active)

    def test_timer_wrap_around(self):
        anim = state.AnimationState(
            flicker_timer=(2 * math.pi) - 0.01,
            glitch_timer=(2 * math.pi) - 0.01,
            flicker_speed=0.1,
            glitch_speed=0.1,
        )

        anim.update(current_ticks=10)

        self.assertGreaterEqual(anim.flicker_timer, 0.0)
        self.assertLess(anim.flicker_timer, 2 * math.pi)
        self.assertGreaterEqual(anim.glitch_timer, 0.0)
        self.assertLess(anim.glitch_timer, 2 * math.pi)


class TestCreateInitialState(unittest.TestCase):
    @patch("state.theme.apply_theme")
    def test_create_initial_state_loads_sections_and_applies_first_theme(self, apply_theme_mock):
        fake_themes = [{"name": "green"}, {"name": "amber"}]

        with patch("state.get_themes_data", return_value=fake_themes), patch(
            "state.get_player_stats_data", return_value={"level": 1}
        ), patch("state.get_inventory_data", return_value=[{"name": "item"}]), patch(
            "state.get_special_stats_data", return_value={"S": 5}
        ), patch("state.get_body_parts_data", return_value={"head": 100}), patch(
            "state.get_quests_data", return_value=[{"name": "quest"}]
        ), patch("state.get_map_data", return_value={"player_pos": [0.5, 0.5]}), patch(
            "state.get_radio_data", return_value={"stations": []}
        ):
            app_state = state.create_initial_state()

        apply_theme_mock.assert_called_once_with(fake_themes[0])
        self.assertEqual(app_state.player_stats, {"level": 1})
        self.assertEqual(app_state.inventory, [{"name": "item"}])
        self.assertEqual(app_state.special_stats, {"S": 5})
        self.assertEqual(app_state.body_parts, {"head": 100})
        self.assertEqual(app_state.quests, [{"name": "quest"}])
        self.assertEqual(app_state.map_data, {"player_pos": [0.5, 0.5]})
        self.assertEqual(app_state.radio_data, {"stations": []})
        self.assertEqual(app_state.themes, fake_themes)
        self.assertIsInstance(app_state.animation, state.AnimationState)


class TestDataLoaderCaching(unittest.TestCase):
    def setUp(self):
        self._original_cache = data_loader._cache
        data_loader._cache = None

    def tearDown(self):
        data_loader._cache = self._original_cache

    def test_load_uses_disk_once_across_multiple_getters(self):
        fake_payload = {
            "player_stats": {"level": 1},
            "inventory": [{"name": "x"}],
            "special": {"S": 1},
            "body_parts": {"head": 100},
            "quests": [{"name": "q"}],
            "map": {"player_pos": [0.1, 0.2]},
            "radio": {"stations": []},
            "themes": [{"name": "green"}],
        }

        with patch("builtins.open", mock_open(read_data="{}")) as open_mock, patch(
            "data_loader.json.load", MagicMock(return_value=fake_payload)
        ) as json_load_mock:
            self.assertEqual(data_loader.get_player_stats_data(), fake_payload["player_stats"])
            self.assertEqual(data_loader.get_inventory_data(), fake_payload["inventory"])
            self.assertEqual(data_loader.get_radio_data(), fake_payload["radio"])
            self.assertEqual(data_loader.get_themes_data(), fake_payload["themes"])

        open_mock.assert_called_once()
        json_load_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()