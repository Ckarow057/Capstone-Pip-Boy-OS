"""
DATA screen (state 2)
Quest log with objectives. Active quests listed on the left, objectives on the right.
"""

import pygame

from config import PIP_GREEN, PIP_GREEN_BRIGHT, PIP_GREEN_DARK, PIP_GREEN_DIM

_CONTENT_TOP = 85

_STATUS_COLORS = {
    "Active":    PIP_GREEN,
    "Completed": (80, 200, 80),
    "Failed":    (200, 80, 80),
}

# Simple module-level selection index (no persistent state needed here)
_selected_quest = 0


def draw(surface, ui, app_state):
    global _selected_quest
    quests = app_state.quests

    # Clamp selection
    if _selected_quest >= len(quests):
        _selected_quest = 0

    # ----- Title -----
    title = ui.fonts.medium.render("DATA  /  QUESTS", True, PIP_GREEN_BRIGHT)
    surface.blit(title, (40, _CONTENT_TOP))
    pygame.draw.line(surface, PIP_GREEN, (40, _CONTENT_TOP + 30), (ui.width - 40, _CONTENT_TOP + 30), 1)

    # ----- Quest list (left panel) -----
    list_x = 40
    list_y = _CONTENT_TOP + 45
    list_w = 420
    row_h = 42

    for i, quest in enumerate(quests):
        active = (i == _selected_quest)
        row_color = PIP_GREEN_DARK if active else (10, 30, 10)
        pygame.draw.rect(surface, row_color, (list_x, list_y, list_w, row_h - 2), 0)
        border_color = PIP_GREEN_BRIGHT if active else PIP_GREEN_DARK
        pygame.draw.rect(surface, border_color, (list_x, list_y, list_w, row_h - 2), 1)

        name_surf = ui.fonts.small.render(quest["name"], True, PIP_GREEN_BRIGHT if active else PIP_GREEN)
        surface.blit(name_surf, (list_x + 8, list_y + 4))

        status_color = _STATUS_COLORS.get(quest["status"], PIP_GREEN_DIM)
        status_surf = ui.fonts.tiny.render(quest["status"].upper(), True, status_color)
        surface.blit(status_surf, (list_x + 8, list_y + 24))

        list_y += row_h

    # Vertical divider
    div_x = list_x + list_w + 20
    pygame.draw.line(surface, PIP_GREEN, (div_x, _CONTENT_TOP + 40), (div_x, ui.height - 80), 1)

    # ----- Objectives panel (right panel) -----
    detail_x = div_x + 20
    detail_y = _CONTENT_TOP + 45

    selected = quests[_selected_quest]

    name_surf = ui.fonts.medium.render(selected["name"], True, PIP_GREEN_BRIGHT)
    surface.blit(name_surf, (detail_x, detail_y))
    detail_y += 36

    desc_surf = ui.fonts.small.render(selected["description"], True, PIP_GREEN_DIM)
    surface.blit(desc_surf, (detail_x, detail_y))
    detail_y += 30

    pygame.draw.line(surface, PIP_GREEN_DARK, (detail_x, detail_y), (ui.width - 40, detail_y), 1)
    detail_y += 12

    obj_label = ui.fonts.tiny.render("OBJECTIVES", True, PIP_GREEN_DIM)
    surface.blit(obj_label, (detail_x, detail_y))
    detail_y += 22

    for obj in selected["objectives"]:
        checkmark = "[X]" if obj["done"] else "[ ]"
        color = PIP_GREEN if obj["done"] else PIP_GREEN_DIM
        obj_surf = ui.fonts.small.render(f"  {checkmark}  {obj['text']}", True, color)
        surface.blit(obj_surf, (detail_x, detail_y))
        detail_y += 30


