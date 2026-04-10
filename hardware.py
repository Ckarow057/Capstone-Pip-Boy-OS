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


def _btn_stat_cb(channel):
    _post("stat")


def _btn_items_cb(channel):
    _post("items")


def _btn_data_cb(channel):
    _post("data")


def _enc_clk_cb(channel):
    dt_state = GPIO.input(GPIO_ENC_DT_PIN)
    if dt_state == GPIO.HIGH:
        _post("scroll_down")
    else:
        _post("scroll_up")


def _enc_sw_cb(channel):
    _post("theme")


def setup() -> None:
    if not _GPIO_AVAILABLE:
        return

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
    
def cleanup() -> None:
    """Release GPIO resources.  Safe to call on non-Pi hardware."""
    if _GPIO_AVAILABLE:
        GPIO.cleanup()
