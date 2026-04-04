"""Active colour theme — module-level variables mutated at runtime via apply_theme().

All rendering code must use  `import theme`  and reference  `theme.PIP_GREEN`  etc.
Using  `from theme import PIP_GREEN`  takes a snapshot at import time and will NOT
reflect subsequent theme switches, so it is intentionally avoided in rendering modules.
"""

# Initial values: Pip-Boy Green (matches the first theme in pip_boy_data.json).
PIP_GREEN        = (51, 255, 51)
PIP_GREEN_DARK   = (20, 100, 20)
PIP_GREEN_BRIGHT = (102, 255, 102)
PIP_GREEN_DIM    = (30, 180, 30)
BACKGROUND       = (10, 20, 10)
SCANLINE_COLOR   = (0, 0, 0, 30)

QUEST_STATUS_COLORS = {
    "Active":    (51, 255, 51),
    "Completed": (80, 200, 80),
    "Failed":    (200, 80, 80),
}

RADIO_STATUS_COLORS = {
    "ON AIR":   (102, 255, 102),
    "OFFLINE":  (120, 120, 120),
    "DISTRESS": (255, 200, 50),
}

# Background tints used in list/card views.
ROW_ALT_BG      = (15, 40, 15)
ROW_INACTIVE_BG = (10, 30, 10)
CARD_ACTIVE_BG  = (12, 35, 12)
CARD_BG         = (8, 20, 8)


def apply_theme(palette: dict) -> None:
    """Update all module-level colour variables from a theme palette dict loaded from JSON."""
    global PIP_GREEN, PIP_GREEN_DARK, PIP_GREEN_BRIGHT, PIP_GREEN_DIM
    global BACKGROUND, SCANLINE_COLOR
    global QUEST_STATUS_COLORS, RADIO_STATUS_COLORS
    global ROW_ALT_BG, ROW_INACTIVE_BG, CARD_ACTIVE_BG, CARD_BG

    PIP_GREEN        = tuple(palette["main"])
    PIP_GREEN_DARK   = tuple(palette["dark"])
    PIP_GREEN_BRIGHT = tuple(palette["bright"])
    PIP_GREEN_DIM    = tuple(palette["dim"])
    BACKGROUND       = tuple(palette["background"])
    SCANLINE_COLOR   = tuple(palette["scanline"])

    QUEST_STATUS_COLORS = {
        "Active":    PIP_GREEN,
        "Completed": tuple(palette["quest_completed"]),
        "Failed":    tuple(palette["quest_failed"]),
    }

    RADIO_STATUS_COLORS = {
        "ON AIR":   PIP_GREEN_BRIGHT,
        "OFFLINE":  tuple(palette["radio_offline"]),
        "DISTRESS": tuple(palette["radio_distress"]),
    }

    ROW_ALT_BG      = tuple(palette["row_alt_bg"])
    ROW_INACTIVE_BG = tuple(palette["row_inactive_bg"])
    CARD_ACTIVE_BG  = tuple(palette["card_active_bg"])
    CARD_BG         = tuple(palette["card_bg"])
