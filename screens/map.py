"""
MAP screen (state 3)
Real map image with player position indicator overlaid.
"""

import pygame
import theme
from config import CONTENT_TOP, MAP_IMG_PATH

_map_cache: dict = {}  # keyed by (w, h) so rescaling only happens once per size


def _get_map_img(w: int, h: int) -> pygame.Surface:
    key = (w, h, theme.PIP_GREEN)
    if key not in _map_cache:
        raw = pygame.image.load(MAP_IMG_PATH).convert()
        scaled = pygame.transform.smoothscale(raw, (w, h))
        tinted = pygame.transform.grayscale(scaled)
        tinted.fill(theme.PIP_GREEN, special_flags=pygame.BLEND_RGB_MULT)
        _map_cache[key] = tinted
    return _map_cache[key]


def _map_rect(ui):
    margin_left = 40
    margin_right = 40
    margin_top = CONTENT_TOP + 40
    margin_bottom = ui.height - 80
    return pygame.Rect(margin_left, margin_top,
                       ui.width - margin_left - margin_right,
                       margin_bottom - margin_top)


def draw(surface, ui, app_state):
    player_pos = app_state.map_data["player_pos"]

    # ----- Title -----
    title = ui.fonts.medium.render("MAP", True, theme.PIP_GREEN_BRIGHT)
    surface.blit(title, (40, CONTENT_TOP))
    pygame.draw.line(surface, theme.PIP_GREEN, (40, CONTENT_TOP + 30), (ui.width - 40, CONTENT_TOP + 30), 1)

    mr = _map_rect(ui)

    # Map image
    map_img = _get_map_img(mr.width, mr.height)
    surface.blit(map_img, (mr.left, mr.top))
    pygame.draw.rect(surface, theme.PIP_GREEN, mr, 2)

    # Player position (blinking crosshair)
    ppx = mr.left + int(player_pos[0] * mr.width)
    ppy = mr.top + int(player_pos[1] * mr.height)
    blink = (pygame.time.get_ticks() // 500) % 2 == 0
    player_color = theme.PIP_GREEN_BRIGHT if blink else theme.PIP_GREEN
    arrow = [
        (ppx,      ppy - 12),  # tip
        (ppx + 6,  ppy + 6),
        (ppx,      ppy + 2),
        (ppx - 6,  ppy + 6),
    ]
    pygame.draw.polygon(surface, player_color, arrow)

