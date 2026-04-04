import pygame
import theme
from state import ScreenState

# Screen modules are imported lazily to avoid circular imports at module level
from screens import data as screen_data
from screens import items as screen_items
from screens import map as screen_map
from screens import radio as screen_radio
from screens import stat as screen_stat

_SCREEN_DRAW = {
    ScreenState.STAT:  screen_stat.draw,
    ScreenState.ITEMS: screen_items.draw,
    ScreenState.DATA:  screen_data.draw,
    ScreenState.MAP:   screen_map.draw,
    ScreenState.RADIO: screen_radio.draw,
}


# ---------------------------------------------------------------------------
# Shared / persistent UI primitives
# ---------------------------------------------------------------------------

def draw_scanlines(surface, ui, scan_line_offset):
    scanline_surface = pygame.Surface((ui.width, ui.height), pygame.SRCALPHA)
    for y in range(scan_line_offset, ui.height, 4):
        pygame.draw.line(scanline_surface, theme.SCANLINE_COLOR, (0, y), (ui.width, y), 2)
    surface.blit(scanline_surface, (0, 0))


def draw_crt_effect(surface, ui, flicker_intensity=0):
    if flicker_intensity > 0:
        overlay = pygame.Surface((ui.width, ui.height), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, int(flicker_intensity * 10)))
        surface.blit(overlay, (0, 0))


def draw_border(surface, ui):
    pygame.draw.rect(surface, theme.PIP_GREEN, (10, 10, ui.width - 20, ui.height - 20), 3)
    pygame.draw.rect(surface, theme.PIP_GREEN_DARK, (15, 15, ui.width - 30, ui.height - 30), 2)


def draw_text_with_glow(surface, text, pos, font, color=None, glow=True):
    if color is None:
        color = theme.PIP_GREEN
    if glow:
        glow_text = font.render(text, True, theme.PIP_GREEN_DARK)
        for offset_x in [-2, -1, 0, 1, 2]:
            for offset_y in [-2, -1, 0, 1, 2]:
                if offset_x != 0 or offset_y != 0:
                    surface.blit(glow_text, (pos[0] + offset_x, pos[1] + offset_y))
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)
    return text_surface.get_width()


def draw_header(surface, ui, player_stats):
    """Persistent top bar: player stat boxes."""
    box_y = 20
    box_height = 40

    lvl_x = 30
    pygame.draw.rect(surface, theme.PIP_GREEN, (lvl_x, box_y, 120, box_height), 2)
    draw_text_with_glow(surface, f"LVL  {player_stats['level']}", (lvl_x + 10, box_y + 10), ui.fonts.small, theme.PIP_GREEN, False)

    hp_x = 170
    pygame.draw.rect(surface, theme.PIP_GREEN, (hp_x, box_y, 180, box_height), 2)
    draw_text_with_glow(surface, f"HP   {player_stats['hp']}/{player_stats['max_hp']}", (hp_x + 10, box_y + 10), ui.fonts.small, theme.PIP_GREEN, False)

    ap_x = 370
    pygame.draw.rect(surface, theme.PIP_GREEN, (ap_x, box_y, 150, box_height), 2)
    draw_text_with_glow(surface, f"AP   {player_stats['ap']}/{player_stats['max_ap']}", (ap_x + 10, box_y + 10), ui.fonts.small, theme.PIP_GREEN, False)

    xp_x = 540
    pygame.draw.rect(surface, theme.PIP_GREEN, (xp_x, box_y, 200, box_height), 2)
    draw_text_with_glow(surface, f"XP   {player_stats['xp']}/{player_stats['next_level']}", (xp_x + 10, box_y + 10), ui.fonts.small, theme.PIP_GREEN, False)

    rads_x = 760
    pygame.draw.rect(surface, theme.PIP_GREEN, (rads_x, box_y, 160, box_height), 2)
    draw_text_with_glow(surface, f"RADS {player_stats['rads']}", (rads_x + 10, box_y + 10), ui.fonts.small, theme.PIP_GREEN, False)

    pygame.draw.line(surface, theme.PIP_GREEN, (30, 75), (ui.width - 30, 75), 2)


def draw_nav_tabs(surface, ui, current_screen):
    """Bottom navigation bar: 3 main tabs. DATA tab highlights for MAP/RADIO sub-screens."""
    _NAV_LABELS = ["STAT", "ITEMS", "DATA"]
    _DATA_GROUP = {ScreenState.DATA, ScreenState.MAP, ScreenState.RADIO}
    _DATA_SUB_LABELS = {
        ScreenState.DATA:  "QUESTS",
        ScreenState.MAP:   "MAP",
        ScreenState.RADIO: "RADIO",
    }

    tab_y = ui.height - 65
    tab_count = 3
    tab_width = (ui.width - 60) // tab_count
    start_x = 30

    pygame.draw.line(surface, theme.PIP_GREEN, (30, tab_y - 5), (ui.width - 30, tab_y - 5), 2)

    for i, label in enumerate(_NAV_LABELS):
        tab_x = start_x + i * tab_width
        if i == 2:  # DATA tab group
            active = current_screen in _DATA_GROUP
        else:
            active = (i == int(current_screen))

        if active:
            pygame.draw.rect(surface, theme.PIP_GREEN_DARK, (tab_x, tab_y, tab_width - 8, 45), 0)

        pygame.draw.rect(surface, theme.PIP_GREEN, (tab_x, tab_y, tab_width - 8, 45), 2)

        text_color = theme.PIP_GREEN_BRIGHT if active else theme.PIP_GREEN_DIM
        center_x = tab_x + (tab_width - 8) // 2

        if active and i == 2:
            # Main label shifted up; sub-screen name shown below
            main_surf = ui.fonts.small.render(label, True, text_color)
            surface.blit(main_surf, main_surf.get_rect(center=(center_x, tab_y + 13)))
            sub_label = _DATA_SUB_LABELS.get(current_screen, "")
            sub_surf = ui.fonts.tiny.render(sub_label, True, theme.PIP_GREEN_BRIGHT)
            surface.blit(sub_surf, sub_surf.get_rect(center=(center_x, tab_y + 32)))
        else:
            main_surf = ui.fonts.small.render(label, True, text_color)
            surface.blit(main_surf, main_surf.get_rect(center=(center_x, tab_y + 22)))

        hint = ui.fonts.tiny.render(str(i + 1), True, theme.PIP_GREEN_DARK)
        surface.blit(hint, (tab_x + 6, tab_y + 4))


def draw_glitch_effect(surface, ui, intensity):
    if intensity > 0.8:
        for _ in range(3):
            y = pygame.time.get_ticks() % ui.height
            pygame.draw.line(surface, theme.PIP_GREEN_BRIGHT, (0, y), (ui.width, y), 2)


# ---------------------------------------------------------------------------
# Main redraw dispatcher
# ---------------------------------------------------------------------------

def redraw(surface, ui, app_state):
    surface.fill(theme.BACKGROUND)
    draw_border(surface, ui)
    draw_header(surface, ui, app_state.player_stats)

    # Delegate content area to the active screen module
    draw_fn = _SCREEN_DRAW.get(app_state.current_screen)
    if draw_fn:
        draw_fn(surface, ui, app_state)

    draw_nav_tabs(surface, ui, app_state.current_screen)
    draw_scanlines(surface, ui, app_state.animation.scan_line_offset)
    draw_crt_effect(surface, ui, app_state.animation.flicker_intensity)

    if app_state.animation.glitch_active:
        draw_glitch_effect(surface, ui, app_state.animation.glitch_intensity)

    pygame.display.flip()

