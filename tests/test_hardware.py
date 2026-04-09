"""Unit tests for hardware.py GPIO input driver.

Mocks both RPi.GPIO and pygame so tests run on any machine without hardware.
"""

import sys
import types
import unittest
from unittest.mock import MagicMock, patch, call

_gpio_stub = types.ModuleType("RPi.GPIO")
_gpio_stub.BCM = "BCM"
_gpio_stub.IN = "IN"
_gpio_stub.HIGH = 1
_gpio_stub.LOW = 0
_gpio_stub.PUD_UP = "PUD_UP"
_gpio_stub.FALLING = "FALLING"
_gpio_stub.setmode = MagicMock()
_gpio_stub.setup = MagicMock()
_gpio_stub.input = MagicMock(return_value=_gpio_stub.HIGH)
_gpio_stub.add_event_detect = MagicMock()
_gpio_stub.cleanup = MagicMock()

_rpi_stub = types.ModuleType("RPi")
_rpi_stub.GPIO = _gpio_stub
sys.modules.setdefault("RPi", _rpi_stub)
sys.modules.setdefault("RPi.GPIO", _gpio_stub)


_pygame_event_stub = types.ModuleType("pygame.event")
_pygame_event_stub.post = MagicMock()
_pygame_event_stub.Event = MagicMock(side_effect=lambda t, **kw: {"type": t, **kw})

_pygame_stub = types.ModuleType("pygame")
_pygame_stub.USEREVENT = 24
_pygame_stub.event = _pygame_event_stub

sys.modules.setdefault("pygame", _pygame_stub)
sys.modules.setdefault("pygame.event", _pygame_event_stub)

import importlib
import hardware  

importlib.reload(hardware)


def _last_posted_action() -> str:
    args, kwargs = _pygame_event_stub.post.call_args
    event = args[0]
    return event["action"]


class TestPostHelper(unittest.TestCase):
    def setUp(self):
        _pygame_event_stub.post.reset_mock()
        _pygame_event_stub.Event.reset_mock()

    def test_post_calls_pygame_event_post(self):
        hardware._post("test_action")
        _pygame_event_stub.post.assert_called_once()

    def test_post_passes_correct_action(self):
        hardware._post("scroll_up")
        self.assertEqual(_last_posted_action(), "scroll_up")

    def test_post_uses_hw_event_type(self):
        hardware._post("stat")
        args, _ = _pygame_event_stub.post.call_args
        event = args[0]
        self.assertEqual(event["type"], hardware.HW_EVENT)


class TestButtonCallbacks(unittest.TestCase):
    def setUp(self):
        _pygame_event_stub.post.reset_mock()

    def test_stat_button_posts_stat(self):
        hardware._btn_stat_cb(channel=17)
        self.assertEqual(_last_posted_action(), "stat")

    def test_items_button_posts_items(self):
        hardware._btn_items_cb(channel=22)
        self.assertEqual(_last_posted_action(), "items")

    def test_data_button_posts_data(self):
        hardware._btn_data_cb(channel=27)
        self.assertEqual(_last_posted_action(), "data")


class TestEncoderCallbacks(unittest.TestCase):
    def setUp(self):
        _pygame_event_stub.post.reset_mock()
        _gpio_stub.input.reset_mock()

    def test_clk_dt_high_posts_scroll_down(self):
        _gpio_stub.input.return_value = _gpio_stub.HIGH
        hardware._enc_clk_cb(channel=13)
        self.assertEqual(_last_posted_action(), "scroll_down")

    def test_clk_dt_low_posts_scroll_up(self):
        _gpio_stub.input.return_value = _gpio_stub.LOW
        hardware._enc_clk_cb(channel=13)
        self.assertEqual(_last_posted_action(), "scroll_up")

    def test_clk_reads_dt_pin(self):
        from config import GPIO_ENC_DT_PIN
        hardware._enc_clk_cb(channel=13)
        _gpio_stub.input.assert_called_with(GPIO_ENC_DT_PIN)

    def test_encoder_sw_posts_theme(self):
        hardware._enc_sw_cb(channel=26)
        self.assertEqual(_last_posted_action(), "theme")


class TestSetup(unittest.TestCase):
    def setUp(self):
        _gpio_stub.setmode.reset_mock()
        _gpio_stub.setup.reset_mock()
        _gpio_stub.add_event_detect.reset_mock()

    def test_setup_sets_bcm_mode(self):
        hardware.setup()
        _gpio_stub.setmode.assert_called_once_with(_gpio_stub.BCM)

    def test_setup_configures_all_six_pins(self):
        from config import (
            GPIO_BTN_STAT_PIN, GPIO_BTN_ITEMS_PIN, GPIO_BTN_DATA_PIN,
            GPIO_ENC_CLK_PIN, GPIO_ENC_DT_PIN, GPIO_ENC_SW_PIN,
        )
        hardware.setup()
        configured_pins = {c.args[0] for c in _gpio_stub.setup.call_args_list}
        expected_pins = {
            GPIO_BTN_STAT_PIN, GPIO_BTN_ITEMS_PIN, GPIO_BTN_DATA_PIN,
            GPIO_ENC_CLK_PIN, GPIO_ENC_DT_PIN, GPIO_ENC_SW_PIN,
        }
        self.assertEqual(configured_pins, expected_pins)

    def test_setup_registers_five_event_detects(self):
        hardware.setup()
        self.assertEqual(_gpio_stub.add_event_detect.call_count, 5)

    def test_setup_skips_when_gpio_unavailable(self):
        original = hardware._GPIO_AVAILABLE
        try:
            hardware._GPIO_AVAILABLE = False
            hardware.setup()
            _gpio_stub.setmode.assert_not_called()
        finally:
            hardware._GPIO_AVAILABLE = original


class TestCleanup(unittest.TestCase):
    def setUp(self):
        _gpio_stub.cleanup.reset_mock()

    def test_cleanup_calls_gpio_cleanup(self):
        hardware.cleanup()
        _gpio_stub.cleanup.assert_called_once()

    def test_cleanup_skips_when_gpio_unavailable(self):
        original = hardware._GPIO_AVAILABLE
        try:
            hardware._GPIO_AVAILABLE = False
            hardware.cleanup()
            _gpio_stub.cleanup.assert_not_called()
        finally:
            hardware._GPIO_AVAILABLE = original


if __name__ == "__main__":
    unittest.main()
