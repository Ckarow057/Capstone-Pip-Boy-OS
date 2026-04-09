"""Raspberry Pi GPIO hardware input driver.

Sets up callbacks for 3 navigation buttons and a rotary encoder (CLK/DT/SW).
Each physical event is translated into a pygame custom event posted to the main
event queue, so game_loop.py handles hardware and keyboard input identically.

Silently skips GPIO initialisation when RPi.GPIO is not available (e.g. dev
machines), so the application runs normally without hardware attached.
"""

import pygame

try:
    import RPi.GPIO as GPIO
    _GPIO_AVAILABLE = True
except ImportError:
    _GPIO_AVAILABLE = False

from config import (
    GPIO_BTN_STAT_PIN,
    GPIO_BTN_ITEMS_PIN,
    GPIO_BTN_DATA_PIN,
    GPIO_ENC_CLK_PIN,
    GPIO_ENC_DT_PIN,
    GPIO_ENC_SW_PIN,
    GPIO_BUTTON_BOUNCETIME_MS,
    GPIO_ENCODER_BOUNCETIME_MS,
)

# Custom pygame event type shared with game_loop.py
HW_EVENT = pygame.USEREVENT + 1


def _post(action: str) -> None:
    """Post a hardware event onto the pygame event queue (thread-safe)."""
    pygame.event.post(pygame.event.Event(HW_EVENT, action=action))


# ---------------------------------------------------------------------------
# Button callbacks
# ---------------------------------------------------------------------------

def _btn_stat_cb(channel):
    _post("stat")


def _btn_items_cb(channel):
    _post("items")


def _btn_data_cb(channel):
    _post("data")


# ---------------------------------------------------------------------------
# Encoder callbacks
# ---------------------------------------------------------------------------

# Tracks the previous CLK state so we can detect a clean LOW→HIGH transition.
# Initialized to HIGH (rest state) in setup().
_enc_last_clk = None


def _enc_clk_cb(channel):
    """Called on any CLK edge (BOTH).

    Fires a scroll event exactly once per physical detent by only acting on
    the CLK LOW→HIGH (rising) transition.  Checking DT at the rising edge:
        DT HIGH → clockwise       → scroll down
        DT LOW  → counter-clockwise → scroll up
    This correctly handles encoders that emit 2 or 4 pulses per detent.
    """
    global _enc_last_clk
    clk = GPIO.input(GPIO_ENC_CLK_PIN)
    if _enc_last_clk == GPIO.LOW and clk == GPIO.HIGH:
        dt_state = GPIO.input(GPIO_ENC_DT_PIN)
        if dt_state == GPIO.HIGH:
            _post("scroll_down")
        else:
            _post("scroll_up")
    _enc_last_clk = clk


def _enc_sw_cb(channel):
    """Encoder push-click → cycle colour theme."""
    _post("theme")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def setup() -> None:
    """Initialise GPIO and register event callbacks.

    Safe to call on non-Pi hardware — does nothing if RPi.GPIO is absent.
    Must be called *after* pygame.init() so that pygame.event.post() works.
    """
    if not _GPIO_AVAILABLE:
        return

    GPIO.setmode(GPIO.BCM)

    # Push buttons and encoder SW: active-low with internal pull-up
    for pin in (GPIO_BTN_STAT_PIN, GPIO_BTN_ITEMS_PIN, GPIO_BTN_DATA_PIN, GPIO_ENC_SW_PIN):
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
    # Encoder CLK and DT
    for pin in (GPIO_ENC_CLK_PIN, GPIO_ENC_DT_PIN):
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    global _enc_last_clk
    _enc_last_clk = GPIO.HIGH  # encoders rest with CLK high

    # Register callbacks
    GPIO.add_event_detect(
        GPIO_BTN_STAT_PIN, GPIO.FALLING,
        callback=_btn_stat_cb,
        bouncetime=GPIO_BUTTON_BOUNCETIME_MS,
    )
    GPIO.add_event_detect(
        GPIO_BTN_ITEMS_PIN, GPIO.FALLING,
        callback=_btn_items_cb,
        bouncetime=GPIO_BUTTON_BOUNCETIME_MS,
    )
    GPIO.add_event_detect(
        GPIO_BTN_DATA_PIN, GPIO.FALLING,
        callback=_btn_data_cb,
        bouncetime=GPIO_BUTTON_BOUNCETIME_MS,
    )
    GPIO.add_event_detect(
        GPIO_ENC_SW_PIN, GPIO.FALLING,
        callback=_enc_sw_cb,
        bouncetime=GPIO_BUTTON_BOUNCETIME_MS,
    )
    GPIO.add_event_detect(
        GPIO_ENC_CLK_PIN, GPIO.BOTH,
        callback=_enc_clk_cb,
        bouncetime=GPIO_ENCODER_BOUNCETIME_MS,
    )


def cleanup() -> None:
    """Release GPIO resources.  Safe to call on non-Pi hardware."""
    if _GPIO_AVAILABLE:
        GPIO.cleanup()
