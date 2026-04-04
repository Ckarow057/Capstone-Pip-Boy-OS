"""
ITEMS screen (state 1)
Categorised inventory list. Left column = category selector, right = item list.
"""

import pygame

from config import PIP_GREEN, PIP_GREEN_BRIGHT, PIP_GREEN_DARK, PIP_GREEN_DIM

_CONTENT_TOP = 85
_CATEGORIES = ["All", "Weapons", "Apparel", "Aid", "Misc", "Ammo"]


def draw(surface, ui, app_state):
    inventory = app_state.inventory

    # ----- Section title -----
    title = ui.fonts.medium.render("ITEMS", True, PIP_GREEN_BRIGHT)
    surface.blit(title, (40, _CONTENT_TOP))
    pygame.draw.line(surface, PIP_GREEN, (40, _CONTENT_TOP + 30), (ui.width - 40, _CONTENT_TOP + 30), 1)

    # ----- Category sidebar -----
    cat_x = 40
    cat_y = _CONTENT_TOP + 45
    cat_w = 150
    cat_h = 34

    for cat in _CATEGORIES:
        pygame.draw.rect(surface, PIP_GREEN_DARK, (cat_x, cat_y, cat_w, cat_h), 0)
        pygame.draw.rect(surface, PIP_GREEN, (cat_x, cat_y, cat_w, cat_h), 1)
        cat_surf = ui.fonts.small.render(cat, True, PIP_GREEN)
        cat_rect = cat_surf.get_rect(midleft=(cat_x + 10, cat_y + cat_h // 2))
        surface.blit(cat_surf, cat_rect)
        cat_y += cat_h + 4

    # Vertical divider
    pygame.draw.line(surface, PIP_GREEN, (210, _CONTENT_TOP + 40), (210, ui.height - 80), 1)

    # ----- Item list (all items for now) -----
    list_x = 230
    col_headers_y = _CONTENT_TOP + 45
    col_name_x = list_x
    col_wt_x = list_x + 320
    col_val_x = list_x + 410
    col_qty_x = list_x + 500

    for label, x in [("NAME", col_name_x), ("WT", col_wt_x), ("VAL", col_val_x), ("QTY", col_qty_x)]:
        h_surf = ui.fonts.tiny.render(label, True, PIP_GREEN_DIM)
        surface.blit(h_surf, (x, col_headers_y))

    pygame.draw.line(surface, PIP_GREEN_DARK, (list_x, col_headers_y + 16), (ui.width - 40, col_headers_y + 16), 1)

    row_y = col_headers_y + 22
    row_h = 30
    max_visible = (ui.height - 80 - row_y) // row_h

    for i, item in enumerate(inventory[:max_visible]):
        # Alternating row tint
        if i % 2 == 0:
            pygame.draw.rect(surface, (15, 40, 15), (list_x - 4, row_y - 2, ui.width - list_x - 30, row_h - 2), 0)

        name_surf = ui.fonts.small.render(item["name"], True, PIP_GREEN)
        surface.blit(name_surf, (col_name_x, row_y))

        wt_surf = ui.fonts.small.render(f"{item['weight']:.1f}", True, PIP_GREEN_DIM)
        surface.blit(wt_surf, (col_wt_x, row_y))

        val_surf = ui.fonts.small.render(str(item["value"]), True, PIP_GREEN_DIM)
        surface.blit(val_surf, (col_val_x, row_y))

        qty_surf = ui.fonts.small.render(str(item["count"]), True, PIP_GREEN_BRIGHT)
        surface.blit(qty_surf, (col_qty_x, row_y))

        row_y += row_h

    # ----- Footer: total weight / caps -----
    total_weight = sum(i["weight"] * i["count"] for i in inventory)
    caps = app_state.player_stats.get("caps", 0)
    footer_y = ui.height - 80
    footer = ui.fonts.small.render(
        f"TOTAL WT: {total_weight:.1f}  |  CAPS: {caps}", True, PIP_GREEN_DIM
    )
    surface.blit(footer, (list_x, footer_y - 18))
