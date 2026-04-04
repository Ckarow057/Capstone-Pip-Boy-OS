import os

WINDOW_SIZE = (1200, 800)
WINDOW_TITLE = "Pip-Boy 3000 Mark IV"

PIP_GREEN = (51, 255, 51)
PIP_GREEN_DARK = (20, 100, 20)
PIP_GREEN_BRIGHT = (102, 255, 102)
PIP_GREEN_DIM = (30, 180, 30)
BACKGROUND = (10, 20, 10)
SCANLINE_COLOR = (0, 0, 0, 30)

# Screen labels for the 3 main nav tabs.
# MAP and RADIO are sub-screens cycled under DATA (button 3).
SCREEN_LABELS = ["STAT", "ITEMS", "DATA"]

# Raspberry Pi GPIO pin numbers (BCM numbering) — used when hardware buttons are wired up.
# Connect button between GPIO pin and GND; internal pull-up is enabled.
GPIO_NEXT_BUTTON_PIN = 17
GPIO_PREV_BUTTON_PIN = 27
GPIO_BUTTON_BOUNCETIME_MS = 200

# ---------------------------------------------------------------------------
# Shared layout / display constants
# ---------------------------------------------------------------------------
CONTENT_TOP = 85              # y-coordinate where screen content begins (below header)
CONTENT_BOTTOM_OFFSET = 75   # subtracted from window height to get content bottom

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