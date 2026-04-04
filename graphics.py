import pygame

from config import (
    BACKGROUND,
    PIP_GREEN,
    PIP_GREEN_BRIGHT,
    PIP_GREEN_DARK,
    PIP_GREEN_DIM,
    SCANLINE_COLOR,
)


def draw_scanlines(surface, ui, scan_line_offset):
    scanline_surface = pygame.Surface((ui.width, ui.height), pygame.SRCALPHA)
    for y in range(scan_line_offset, ui.height, 4):
        pygame.draw.line(scanline_surface, SCANLINE_COLOR, (0, y), (ui.width, y), 2)
    surface.blit(scanline_surface, (0, 0))


def draw_crt_effect(surface, ui, flicker_intensity=0):
    if flicker_intensity > 0:
        overlay = pygame.Surface((ui.width, ui.height), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, int(flicker_intensity * 10)))
        surface.blit(overlay, (0, 0))


def draw_border(surface, ui):
    pygame.draw.rect(surface, PIP_GREEN, (10, 10, ui.width - 20, ui.height - 20), 3)
    pygame.draw.rect(surface, PIP_GREEN_DARK, (15, 15, ui.width - 30, ui.height - 30), 2)


def draw_text_with_glow(surface, text, pos, font, color=PIP_GREEN, glow=True):
    if glow:
        glow_text = font.render(text, True, PIP_GREEN_DARK)
        for offset_x in [-2, -1, 0, 1, 2]:
            for offset_y in [-2, -1, 0, 1, 2]:
                if offset_x != 0 or offset_y != 0:
                    surface.blit(glow_text, (pos[0] + offset_x, pos[1] + offset_y))

    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)
    return text_surface.get_width()


def draw_header(surface, ui, player_stats):
    draw_text_with_glow(surface, "STATS", (60, 25), ui.fonts.medium, PIP_GREEN_BRIGHT, False)

    box_y = 20
    box_height = 40

    lvl_x = 220
    pygame.draw.rect(surface, PIP_GREEN, (lvl_x, box_y, 120, box_height), 2)
    draw_text_with_glow(surface, f"LVL  {player_stats['level']}", (lvl_x + 10, box_y + 10), ui.fonts.small, PIP_GREEN, False)

    hp_x = 360
    pygame.draw.rect(surface, PIP_GREEN, (hp_x, box_y, 180, box_height), 2)
    draw_text_with_glow(surface, f"HP  {player_stats['hp']}/{player_stats['max_hp']}", (hp_x + 10, box_y + 10), ui.fonts.small, PIP_GREEN, False)

    ap_x = 560
    pygame.draw.rect(surface, PIP_GREEN, (ap_x, box_y, 150, box_height), 2)
    draw_text_with_glow(surface, f"AP  {player_stats['ap']}/{player_stats['max_ap']}", (ap_x + 10, box_y + 10), ui.fonts.small, PIP_GREEN, False)

    xp_x = 730
    pygame.draw.rect(surface, PIP_GREEN, (xp_x, box_y, 180, box_height), 2)
    draw_text_with_glow(surface, f"XP  {player_stats['xp']}/{player_stats['next_level']}", (xp_x + 10, box_y + 10), ui.fonts.small, PIP_GREEN, False)

    pygame.draw.line(surface, PIP_GREEN, (30, 75), (ui.width - 30, 75), 2)


def draw_vault_boy(surface, ui, player_stats, body_parts):
    center_x = ui.width // 2
    center_y = 350

    head_radius = 45
    head_y = center_y - 150
    head_color = PIP_GREEN if body_parts["head"] > 50 else (255, 255, 51)
    pygame.draw.circle(surface, head_color, (center_x, head_y), head_radius, 3)
    pygame.draw.circle(surface, head_color, (center_x - 15, head_y - 5), 5, 2)
    pygame.draw.circle(surface, head_color, (center_x + 15, head_y - 5), 5, 2)
    pygame.draw.arc(surface, head_color, (center_x - 15, head_y + 10, 30, 15), 3.14, 0, 2)

    pygame.draw.line(surface, PIP_GREEN, (center_x, head_y + head_radius), (center_x, center_y - 80), 3)

    torso_width = 80
    torso_height = 100
    torso_color = PIP_GREEN if body_parts["torso"] > 50 else (255, 255, 51)
    pygame.draw.rect(surface, torso_color, (center_x - torso_width//2, center_y - 80, torso_width, torso_height), 3)

    left_arm_color = PIP_GREEN if body_parts["left_arm"] > 50 else (255, 255, 51)
    arm_start_y = center_y - 60
    pygame.draw.line(surface, left_arm_color, (center_x - torso_width//2, arm_start_y),
                     (center_x - torso_width//2 - 60, arm_start_y + 40), 5)
    pygame.draw.line(surface, left_arm_color, (center_x - torso_width//2 - 60, arm_start_y + 40),
                     (center_x - torso_width//2 - 80, arm_start_y + 100), 5)
    pygame.draw.circle(surface, left_arm_color, (center_x - torso_width//2 - 80, arm_start_y + 100), 10, 3)

    right_arm_color = PIP_GREEN if body_parts["right_arm"] > 50 else (255, 255, 51)
    pygame.draw.line(surface, right_arm_color, (center_x + torso_width//2, arm_start_y),
                     (center_x + torso_width//2 + 60, arm_start_y + 40), 5)
    pygame.draw.line(surface, right_arm_color, (center_x + torso_width//2 + 60, arm_start_y + 40),
                     (center_x + torso_width//2 + 80, arm_start_y + 100), 5)
    pygame.draw.circle(surface, right_arm_color, (center_x + torso_width//2 + 80, arm_start_y + 100), 10, 3)

    left_leg_color = PIP_GREEN if body_parts["left_leg"] > 50 else (255, 255, 51)
    leg_start_y = center_y + 20
    pygame.draw.line(surface, left_leg_color, (center_x - 20, leg_start_y),
                     (center_x - 25, leg_start_y + 70), 6)
    pygame.draw.line(surface, left_leg_color, (center_x - 25, leg_start_y + 70),
                     (center_x - 20, leg_start_y + 140), 6)
    pygame.draw.line(surface, left_leg_color, (center_x - 20, leg_start_y + 140),
                     (center_x - 5, leg_start_y + 140), 6)

    right_leg_color = PIP_GREEN if body_parts["right_leg"] > 50 else (255, 255, 51)
    pygame.draw.line(surface, right_leg_color, (center_x + 20, leg_start_y),
                     (center_x + 25, leg_start_y + 70), 6)
    pygame.draw.line(surface, right_leg_color, (center_x + 25, leg_start_y + 70),
                     (center_x + 20, leg_start_y + 140), 6)
    pygame.draw.line(surface, right_leg_color, (center_x + 20, leg_start_y + 140),
                     (center_x + 35, leg_start_y + 140), 6)

    bar_width = 80
    bar_height = 12

    head_bar_x = center_x - bar_width // 2
    head_bar_y = head_y - 80
    pygame.draw.rect(surface, PIP_GREEN_DARK, (head_bar_x, head_bar_y, bar_width, bar_height), 0)
    pygame.draw.rect(surface, head_color, (head_bar_x, head_bar_y, bar_width, bar_height), 2)
    fill = int((body_parts['head'] / 100) * bar_width)
    pygame.draw.rect(surface, head_color, (head_bar_x, head_bar_y, fill, bar_height), 0)
    pygame.draw.line(surface, head_color, (center_x, head_bar_y + bar_height), (center_x, head_y - head_radius), 2)

    torso_bar_x = center_x - bar_width // 2
    torso_bar_y = center_y - 30
    pygame.draw.rect(surface, PIP_GREEN_DARK, (torso_bar_x, torso_bar_y, bar_width, bar_height), 0)
    pygame.draw.rect(surface, torso_color, (torso_bar_x, torso_bar_y, bar_width, bar_height), 2)
    fill = int((body_parts['torso'] / 100) * bar_width)
    pygame.draw.rect(surface, torso_color, (torso_bar_x, torso_bar_y, fill, bar_height), 0)

    left_arm_bar_x = center_x - torso_width//2 - 150
    left_arm_bar_y = arm_start_y + 20
    pygame.draw.rect(surface, PIP_GREEN_DARK, (left_arm_bar_x, left_arm_bar_y, bar_width, bar_height), 0)
    pygame.draw.rect(surface, left_arm_color, (left_arm_bar_x, left_arm_bar_y, bar_width, bar_height), 2)
    fill = int((body_parts['left_arm'] / 100) * bar_width)
    pygame.draw.rect(surface, left_arm_color, (left_arm_bar_x, left_arm_bar_y, fill, bar_height), 0)
    pygame.draw.line(surface, left_arm_color, (left_arm_bar_x + bar_width, left_arm_bar_y + bar_height//2),
                     (center_x - torso_width//2 - 40, arm_start_y + 20), 2)

    right_arm_bar_x = center_x + torso_width//2 + 70
    right_arm_bar_y = arm_start_y + 20
    pygame.draw.rect(surface, PIP_GREEN_DARK, (right_arm_bar_x, right_arm_bar_y, bar_width, bar_height), 0)
    pygame.draw.rect(surface, right_arm_color, (right_arm_bar_x, right_arm_bar_y, bar_width, bar_height), 2)
    fill = int((body_parts['right_arm'] / 100) * bar_width)
    pygame.draw.rect(surface, right_arm_color, (right_arm_bar_x, right_arm_bar_y, fill, bar_height), 0)
    pygame.draw.line(surface, right_arm_color, (right_arm_bar_x, right_arm_bar_y + bar_height//2),
                     (center_x + torso_width//2 + 40, arm_start_y + 20), 2)

    left_leg_bar_x = center_x - 150
    left_leg_bar_y = leg_start_y + 70
    pygame.draw.rect(surface, PIP_GREEN_DARK, (left_leg_bar_x, left_leg_bar_y, bar_width, bar_height), 0)
    pygame.draw.rect(surface, left_leg_color, (left_leg_bar_x, left_leg_bar_y, bar_width, bar_height), 2)
    fill = int((body_parts['left_leg'] / 100) * bar_width)
    pygame.draw.rect(surface, left_leg_color, (left_leg_bar_x, left_leg_bar_y, fill, bar_height), 0)
    pygame.draw.line(surface, left_leg_color, (left_leg_bar_x + bar_width, left_leg_bar_y + bar_height//2),
                     (center_x - 25, leg_start_y + 40), 2)

    right_leg_bar_x = center_x + 70
    right_leg_bar_y = leg_start_y + 70
    pygame.draw.rect(surface, PIP_GREEN_DARK, (right_leg_bar_x, right_leg_bar_y, bar_width, bar_height), 0)
    pygame.draw.rect(surface, right_leg_color, (right_leg_bar_x, right_leg_bar_y, bar_width, bar_height), 2)
    fill = int((body_parts['right_leg'] / 100) * bar_width)
    pygame.draw.rect(surface, right_leg_color, (right_leg_bar_x, right_leg_bar_y, fill, bar_height), 0)
    pygame.draw.line(surface, right_leg_color, (right_leg_bar_x, right_leg_bar_y + bar_height//2),
                     (center_x + 25, leg_start_y + 40), 2)

    level_text = f"Level {player_stats['level']}"
    level_surface = ui.fonts.medium.render(level_text, True, PIP_GREEN)
    level_x = (ui.width - level_surface.get_width()) // 2
    draw_text_with_glow(surface, level_text, (level_x, center_y + 180), ui.fonts.medium, PIP_GREEN, False)


def draw_left_labels(surface, ui):
    start_x = 60
    start_y = 110

    pygame.draw.rect(surface, PIP_GREEN, (start_x, start_y, 80, 40), 2)
    draw_text_with_glow(surface, "CND", (start_x + 15, start_y + 10), ui.fonts.small, PIP_GREEN, False)
    draw_text_with_glow(surface, "RAD", (start_x + 5, start_y + 70), ui.fonts.medium, PIP_GREEN, False)
    draw_text_with_glow(surface, "EFF", (start_x + 5, start_y + 130), ui.fonts.medium, PIP_GREEN, False)


def draw_equipment_info(surface, ui, inventory):
    start_x = ui.width - 280
    start_y = 110

    y_offset = start_y
    for item in inventory:
        item_text = f"({item['count']}) {item['name']} {item['hotkey']})"
        draw_text_with_glow(surface, item_text, (start_x, y_offset), ui.fonts.small, PIP_GREEN_DIM, False)
        y_offset += 60


def draw_tabs(surface, ui):
    tab_y = ui.height - 80
    tabs = ["Status", "Special", "Skills", "Perks", "General"]
    tab_width = 160
    start_x = 120

    for i, tab in enumerate(tabs):
        tab_x = start_x + (i * tab_width)

        if i == 0:
            pygame.draw.rect(surface, PIP_GREEN_DARK, (tab_x, tab_y, tab_width - 10, 40), 0)

        pygame.draw.rect(surface, PIP_GREEN, (tab_x, tab_y, tab_width - 10, 40), 2)

        text_color = PIP_GREEN_BRIGHT if i == 0 else PIP_GREEN
        text_surface = ui.fonts.small.render(tab, True, text_color)
        text_rect = text_surface.get_rect(center=(tab_x + (tab_width - 10) // 2, tab_y + 20))
        surface.blit(text_surface, text_rect)


def draw_glitch_effect(surface, ui, intensity):
    if intensity > 0.8:
        for _ in range(3):
            y = pygame.time.get_ticks() % ui.height
            pygame.draw.line(surface, PIP_GREEN_BRIGHT, (0, y), (ui.width, y), 2)


def redraw(surface, ui, app_state):
    surface.fill(BACKGROUND)
    draw_border(surface, ui)
    draw_header(surface, ui, app_state.player_stats)
    draw_left_labels(surface, ui)
    draw_vault_boy(surface, ui, app_state.player_stats, app_state.body_parts)
    draw_equipment_info(surface, ui, app_state.inventory)
    draw_tabs(surface, ui)
    draw_scanlines(surface, ui, app_state.animation.scan_line_offset)
    draw_crt_effect(surface, ui, app_state.animation.flicker_intensity)

    if app_state.animation.glitch_active:
        draw_glitch_effect(surface, ui, app_state.animation.glitch_intensity)

    pygame.display.flip()