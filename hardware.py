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

# Quadrature rotary encoder state machine
_START = 0
_CW1 = 1
_CW2 = 2
_CW3 = 3
_CCW1 = 4
_CCW2 = 5
_CCW3 = 6

_STATE_MASK = 0x7
_DIR_CW = 0x10
_DIR_CCW = 0x20
_DIR_MASK = 0x30

_ENC_TABLE = [
    [_START, _CW1, _CCW1, _START],
    [_CW2, _CW1, _START, _START],
    [_CW2, _CW1, _CW3, _START],
    [_CW2, _START, _CW3, _START | _DIR_CW],
    [_CCW2, _START, _CCW1, _START],
    [_CCW2, _CCW3, _CCW1, _START],
    [_CCW2, _CCW3, _START, _START | _DIR_CCW],
]

_enc_state = _START


def _post(action: str) -> None:
    """Post a hardware event onto the pygame event queue (thread-safe)."""
    pygame.event.post(pygame.event.Event(HW_EVENT, action=action))


def _btn_stat_cb(channel):
    _post("stat")


def _btn_items_cb(channel):
    _post("items")


def _btn_data_cb(channel):
    _post("data")


def _update_encoder_state(channel=None):
    """Decode quadrature transitions and post one action per detent."""
    global _enc_state

    clk_state = GPIO.input(GPIO_ENC_CLK_PIN)
    dt_state = GPIO.input(GPIO_ENC_DT_PIN)
    clk_dt = (clk_state << 1) | dt_state

    _enc_state = _ENC_TABLE[_enc_state & _STATE_MASK][clk_dt]
    direction = _enc_state & _DIR_MASK
    if direction == _DIR_CW:
        _post("scroll_down")
    elif direction == _DIR_CCW:
        _post("scroll_up")

    _enc_state &= _STATE_MASK


def _enc_clk_cb(channel):
    _update_encoder_state(channel)


def _enc_dt_cb(channel):
    _update_encoder_state(channel)


def _enc_sw_cb(channel):
    _post("theme")


def setup() -> None:
    global _enc_state
    if not _GPIO_AVAILABLE:
        return

    _enc_state = _START
    GPIO.setmode(GPIO.BCM)

    for pin in (GPIO_BTN_STAT_PIN, GPIO_BTN_ITEMS_PIN, GPIO_BTN_DATA_PIN, GPIO_ENC_SW_PIN):
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
    for pin in (GPIO_ENC_CLK_PIN, GPIO_ENC_DT_PIN):
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
        GPIO_ENC_CLK_PIN, GPIO.FALLING,
        callback=_enc_clk_cb,
        bouncetime=GPIO_ENCODER_BOUNCETIME_MS,
    )
    GPIO.add_event_detect(
        GPIO_ENC_DT_PIN, GPIO.FALLING,
        callback=_enc_dt_cb,
        bouncetime=GPIO_ENCODER_BOUNCETIME_MS,
    )
    
def cleanup() -> None:
    """Release GPIO resources.  Safe to call on non-Pi hardware."""
    if _GPIO_AVAILABLE:
        GPIO.cleanup()
