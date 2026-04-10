import os

WINDOW_SIZE = (1200, 800)
WINDOW_TITLE = "Pip-Boy 3000 Mark IV"

PIP_GREEN = (51, 255, 51)
PIP_GREEN_DARK = (20, 100, 20)
PIP_GREEN_BRIGHT = (102, 255, 102)
PIP_GREEN_DIM = (30, 180, 30)
BACKGROUND = (10, 20, 10)
SCANLINE_COLOR = (0, 0, 0, 30)


SCREEN_LABELS = ["STAT", "ITEMS", "DATA"]

# 3 navigation buttons
GPIO_BTN_STAT_PIN  = 17   # Button 1 → STAT screen
GPIO_BTN_ITEMS_PIN = 22   # Button 2 → ITEMS screen
GPIO_BTN_DATA_PIN  = 27   # Button 3 → cycle DATA / MAP / RADIO

# Rotary encoder
GPIO_ENC_CLK_PIN = 13   # CLK (A) — rotation detection
GPIO_ENC_DT_PIN  = 19   # DT  (B) — direction detection
GPIO_ENC_SW_PIN  = 26   # SW  (push-click) → cycle colour theme

GPIO_BUTTON_BOUNCETIME_MS  = 200   # debounce for push buttons (ms)
GPIO_ENCODER_BOUNCETIME_MS = 50    # debounce for encoder CLK (ms)


CONTENT_TOP = 85           
CONTENT_BOTTOM_OFFSET = 75   

INVENTORY_CATEGORIES = ["All", "Weapons", "Apparel", "Aid", "Misc", "Ammo"]

QUEST_STATUS_COLORS = {
    "Active":    PIP_GREEN,
    "Completed": (80, 200, 80),
    "Failed":    (200, 80, 80),
}

RADIO_STATUS_COLORS = {
    "ON AIR":   PIP_GREEN_BRIGHT,
    "OFFLINE":  (120, 120, 120),
    "DISTRESS": (255, 200, 50),
}

VAULT_BOY_IMG_PATH = os.path.join(os.path.dirname(__file__), "images", "vault-boy.png")
MAP_IMG_PATH = os.path.join(os.path.dirname(__file__), "images", "map.jpg")