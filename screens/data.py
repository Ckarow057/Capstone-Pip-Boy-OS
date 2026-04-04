"""
DATA screen (state 2)
Quest log with objectives. Active quests listed on the left, objectives on the right.
"""

import pygame
import theme
from config import CONTENT_TOP


def draw(surface, ui, app_state):
    quests = app_state.quests

    # Clamp in case quest list shrank
    if app_state.selected_quest >= len(quests):
        app_state.selected_quest = 0

    # ----- Title -----
    title = ui.fonts.medium.render("DATA  /  QUESTS", True, theme.PIP_GREEN_BRIGHT)
    surface.blit(title, (40, CONTENT_TOP))
    pygame.draw.line(surface, theme.PIP_GREEN, (40, CONTENT_TOP + 30), (ui.width - 40, CONTENT_TOP + 30), 1)

    # ----- Quest list (left panel) -----
    list_x = 40
    list_y = CONTENT_TOP + 45
    list_w = 420
    row_h = 42

    for i, quest in enumerate(quests):
        active = (i == app_state.selected_quest)
        row_color = theme.PIP_GREEN_DARK if active else theme.ROW_INACTIVE_BG
        pygame.draw.rect(surface, row_color, (list_x, list_y, list_w, row_h - 2), 0)
        border_color = theme.PIP_GREEN_BRIGHT if active else theme.PIP_GREEN_DARK
        pygame.draw.rect(surface, border_color, (list_x, list_y, list_w, row_h - 2), 1)

        name_surf = ui.fonts.small.render(quest["name"], True, theme.PIP_GREEN_BRIGHT if active else theme.PIP_GREEN)
        surface.blit(name_surf, (list_x + 8, list_y + 4))

        status_color = theme.QUEST_STATUS_COLORS.get(quest["status"], theme.PIP_GREEN_DIM)
        status_surf = ui.fonts.tiny.render(quest["status"].upper(), True, status_color)
        surface.blit(status_surf, (list_x + 8, list_y + 24))

        list_y += row_h

    # Vertical divider
    div_x = list_x + list_w + 20
    pygame.draw.line(surface, theme.PIP_GREEN, (div_x, CONTENT_TOP + 40), (div_x, ui.height - 80), 1)

    # ----- Objectives panel (right panel) -----
    detail_x = div_x + 20
    detail_y = CONTENT_TOP + 45

    selected = quests[app_state.selected_quest]

    name_surf = ui.fonts.medium.render(selected["name"], True, theme.PIP_GREEN_BRIGHT)
    surface.blit(name_surf, (detail_x, detail_y))
    detail_y += 36

    desc_surf = ui.fonts.small.render(selected["description"], True, theme.PIP_GREEN_DIM)
    surface.blit(desc_surf, (detail_x, detail_y))
    detail_y += 30

    pygame.draw.line(surface, theme.PIP_GREEN_DARK, (detail_x, detail_y), (ui.width - 40, detail_y), 1)
    detail_y += 12

    obj_label = ui.fonts.tiny.render("OBJECTIVES", True, theme.PIP_GREEN_DIM)
    surface.blit(obj_label, (detail_x, detail_y))
    detail_y += 22

    for obj in selected["objectives"]:
        checkmark = "[X]" if obj["done"] else "[ ]"
        color = theme.PIP_GREEN if obj["done"] else theme.PIP_GREEN_DIM
        obj_surf = ui.fonts.small.render(f"  {checkmark}  {obj['text']}", True, color)
        surface.blit(obj_surf, (detail_x, detail_y))
        detail_y += 30


