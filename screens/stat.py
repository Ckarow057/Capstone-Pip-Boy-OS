"""
STAT screen (state 0)
Displays the Vault Boy image and S.P.E.C.I.A.L. stats.
"""

import pygame
import theme
from config import CONTENT_BOTTOM_OFFSET, CONTENT_TOP, VAULT_BOY_IMG_PATH
_vault_boy_cache: dict = {}  # keyed by target height so rescaling only happens once per size


def _part_color(hp):
    if hp > 60:
        return theme.PIP_GREEN
    if hp > 30:
        return (255, 255, 51)
    return (255, 80, 80)


# ---------------------------------------------------------------------------
# S.P.E.C.I.A.L. panel (left column)
# ---------------------------------------------------------------------------

_SPECIAL_FULL = {
    "S": "STRENGTH",
    "P": "PERCEPTION",
    "E": "ENDURANCE",
    "C": "CHARISMA",
    "I": "INTELLIGENCE",
    "A": "AGILITY",
    "L": "LUCK",
}


def _draw_special(surface, ui, special_stats):
    x = 40
    y = CONTENT_TOP + 10
    row_h = 62

    # Section label
    label = ui.fonts.medium.render("S.P.E.C.I.A.L.", True, theme.PIP_GREEN_BRIGHT)
    surface.blit(label, (x, y))
    y += 38

    for abbr, full in _SPECIAL_FULL.items():
        val = special_stats.get(abbr, 0)

        # Full name + value
        name_surf = ui.fonts.small.render(f"{full}", True, theme.PIP_GREEN_DIM)
        surface.blit(name_surf, (x, y))
        val_surf = ui.fonts.medium.render(str(val), True, theme.PIP_GREEN_BRIGHT)
        surface.blit(val_surf, (x + 190, y - 2))

        # Pip bar: 10 small rectangles
        bar_x = x
        bar_y = y + 22
        for pip in range(10):
            color = theme.PIP_GREEN if pip < val else theme.PIP_GREEN_DARK
            pygame.draw.rect(surface, color, (bar_x + pip * 21, bar_y, 17, 8), border_radius=2)
            pygame.draw.rect(surface, theme.PIP_GREEN_DARK, (bar_x + pip * 21, bar_y, 17, 8), 1, border_radius=2)

        y += row_h


# ---------------------------------------------------------------------------
# Vault Boy image (centre column)
# ---------------------------------------------------------------------------

def _get_vault_boy(target_h: int) -> pygame.Surface:
    """Return a cached, scaled, theme-tinted copy of the vault-boy image."""
    key = (target_h, theme.PIP_GREEN)
    if key not in _vault_boy_cache:
        raw = pygame.image.load(VAULT_BOY_IMG_PATH).convert()
        raw.set_colorkey((0, 0, 0))
        orig_w, orig_h = raw.get_size()
        scale = target_h / orig_h
        scaled = pygame.transform.smoothscale(raw, (int(orig_w * scale), target_h))
        tinted = pygame.transform.grayscale(scaled)
        tinted.fill(theme.PIP_GREEN, special_flags=pygame.BLEND_RGB_MULT)
        tinted.set_colorkey((0, 0, 0))
        _vault_boy_cache[key] = tinted
    return _vault_boy_cache[key]


def _draw_vault_boy(surface, ui, player_stats, body_parts):
    content_h = ui.height - CONTENT_BOTTOM_OFFSET - CONTENT_TOP
    target_h = int(content_h * 0.85)  # fill ~85% of the content column height

    img = _get_vault_boy(target_h)
    cx = ui.width // 2
    img_rect = img.get_rect(centerx=cx, top=CONTENT_TOP + (content_h - target_h) // 2)
    surface.blit(img, img_rect)

    # Level label below the image
    lv_surf = ui.fonts.medium.render(f"LEVEL  {player_stats['level']}", True, theme.PIP_GREEN)
    lv_rect = lv_surf.get_rect(centerx=cx, top=img_rect.bottom + 8)
    surface.blit(lv_surf, lv_rect)


# ---------------------------------------------------------------------------
# Body condition bars (right column)
# ---------------------------------------------------------------------------

def _draw_condition_bars(surface, ui, body_parts):
    x = ui.width - 280
    y = CONTENT_TOP + 10
    bar_w = 200
    bar_h = 14
    row_h = 52

    label = ui.fonts.medium.render("CONDITION", True, theme.PIP_GREEN_BRIGHT)
    surface.blit(label, (x, y))
    y += 38

    for part_key, display_name in [
        ("head",      "HEAD     "),
        ("torso",     "TORSO    "),
        ("left_arm",  "L. ARM   "),
        ("right_arm", "R. ARM   "),
        ("left_leg",  "L. LEG   "),
        ("right_leg", "R. LEG   "),
    ]:
        hp = body_parts[part_key]
        color = _part_color(hp)

        name_surf = ui.fonts.small.render(display_name, True, theme.PIP_GREEN_DIM)
        surface.blit(name_surf, (x, y))

        pct_surf = ui.fonts.small.render(f"{hp}%", True, color)
        surface.blit(pct_surf, (x + bar_w + 8, y))

        bar_y = y + 22
        pygame.draw.rect(surface, theme.PIP_GREEN_DARK, (x, bar_y, bar_w, bar_h), 0, border_radius=3)
        pygame.draw.rect(surface, color, (x, bar_y, int(bar_w * hp / 100), bar_h), 0, border_radius=3)
        pygame.draw.rect(surface, theme.PIP_GREEN, (x, bar_y, bar_w, bar_h), 1, border_radius=3)

        y += row_h


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def draw(surface, ui, app_state):
    _draw_special(surface, ui, app_state.special_stats)
    _draw_vault_boy(surface, ui, app_state.player_stats, app_state.body_parts)
    _draw_condition_bars(surface, ui, app_state.body_parts)
