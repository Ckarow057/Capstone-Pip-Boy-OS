"""
RADIO screen (state 4)
Station list with signal-strength bars and currently-playing indicator.
"""

import math

import pygame
import theme
from config import CONTENT_TOP


def _draw_signal_bar(surface, x, y, strength, width=120, height=16):
    """Draw a segmented signal-strength bar (0.0 – 1.0)."""
    segments = 10
    seg_w = (width - segments) // segments
    for i in range(segments):
        threshold = (i + 1) / segments
        if strength >= threshold:
            color = theme.PIP_GREEN_BRIGHT if strength > 0.7 else (theme.PIP_GREEN if strength > 0.4 else (200, 200, 50))
        else:
            color = theme.PIP_GREEN_DARK
        sx = x + i * (seg_w + 1)
        pygame.draw.rect(surface, color, (sx, y, seg_w, height))
        pygame.draw.rect(surface, theme.PIP_GREEN_DARK, (sx, y, seg_w, height), 1)


def _draw_waveform(surface, cx, cy, width, amplitude, color):
    """Animated sine-wave decorations around the active station."""
    points = []
    steps = width
    t = pygame.time.get_ticks() / 300.0
    for i in range(steps):
        x = cx - width // 2 + i
        y = cy + int(amplitude * math.sin((i / steps) * 4 * math.pi + t))
        points.append((x, y))
    if len(points) > 1:
        pygame.draw.lines(surface, color, False, points, 2)


def draw(surface, ui, app_state):
    radio_data = app_state.radio_data
    stations = radio_data["stations"]
    active_idx = app_state.selected_station

    # ----- Title -----
    title = ui.fonts.medium.render("RADIO", True, theme.PIP_GREEN_BRIGHT)
    surface.blit(title, (40, CONTENT_TOP))
    pygame.draw.line(surface, theme.PIP_GREEN, (40, CONTENT_TOP + 30), (ui.width - 40, CONTENT_TOP + 30), 1)

    # ----- Station list -----
    list_x = 40
    list_y = CONTENT_TOP + 50
    card_h = 90
    card_gap = 12
    card_w = ui.width - 80

    for i, station in enumerate(stations):
        active = (i == active_idx)
        is_on = station["status"] == "ON AIR"

        # Card background
        bg_color = theme.CARD_ACTIVE_BG if active else theme.CARD_BG
        pygame.draw.rect(surface, bg_color, (list_x, list_y, card_w, card_h), 0, border_radius=5)
        border_color = theme.PIP_GREEN_BRIGHT if active else theme.PIP_GREEN_DARK
        pygame.draw.rect(surface, border_color, (list_x, list_y, card_w, card_h), 2, border_radius=5)

        # Station name + frequency
        name_color = theme.PIP_GREEN_BRIGHT if active else theme.PIP_GREEN
        name_surf = ui.fonts.small.render(station["name"], True, name_color)
        surface.blit(name_surf, (list_x + 12, list_y + 8))

        freq_surf = ui.fonts.tiny.render(station["frequency"], True, theme.PIP_GREEN_DIM)
        surface.blit(freq_surf, (list_x + 12, list_y + 30))

        # Status badge
        status_text = station["status"]
        status_color = theme.RADIO_STATUS_COLORS.get(status_text, theme.PIP_GREEN_DIM)
        status_surf = ui.fonts.small.render(status_text, True, status_color)
        surface.blit(status_surf, (list_x + 12, list_y + 52))

        # Signal bar (right side)
        signal_x = list_x + card_w - 160
        signal_label = ui.fonts.tiny.render("SIGNAL", True, theme.PIP_GREEN_DIM)
        surface.blit(signal_label, (signal_x, list_y + 8))
        _draw_signal_bar(surface, signal_x, list_y + 26, station["signal"] if is_on else 0.0)

        pct = int(station["signal"] * 100) if is_on else 0
        pct_surf = ui.fonts.tiny.render(f"{pct}%", True, theme.PIP_GREEN_DIM)
        surface.blit(pct_surf, (signal_x + 128, list_y + 26))

        # DJ name
        dj_surf = ui.fonts.tiny.render(f"DJ: {station['dj']}", True, theme.PIP_GREEN_DIM)
        surface.blit(dj_surf, (signal_x, list_y + 52))

        # Animated waveform on active station
        if active and is_on:
            wave_cx = list_x + card_w - 300
            wave_cy = list_y + card_h // 2
            _draw_waveform(surface, wave_cx, wave_cy, 120, 4, theme.PIP_GREEN_DARK)
            _draw_waveform(surface, wave_cx, wave_cy, 120, 16, theme.PIP_GREEN)

        list_y += card_h + card_gap

    # ----- Now Playing footer -----
    active_station = stations[active_idx]
    footer_y = ui.height - 80
    playing_text = (
        f"NOW TUNED: {active_station['name']}  |  {active_station['frequency']}"
        if active_station["status"] == "ON AIR"
        else f"NO SIGNAL  |  {active_station['name']}"
    )
    footer_surf = ui.fonts.small.render(playing_text, True, theme.PIP_GREEN_BRIGHT)
    footer_rect = footer_surf.get_rect(centerx=ui.width // 2, top=footer_y - 18)
    surface.blit(footer_surf, footer_rect)
