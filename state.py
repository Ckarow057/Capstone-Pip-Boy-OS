import math
from dataclasses import dataclass

from data_loader import (
    get_body_parts_data,
    get_inventory_data,
    get_player_stats_data,
    get_special_stats_data,
)


@dataclass
class AnimationState:
    scanline_step: int = 4
    flicker_speed: float = 0.1
    glitch_speed: float = 0.05
    glitch_interval_ms: int = 3000
    glitch_window_ms: int = 50
    scan_line_offset: int = 0
    flicker_timer: float = 0.0
    glitch_timer: float = 0.0
    flicker_intensity: float = 0.0
    glitch_intensity: float = 0.0
    glitch_active: bool = False

    def update(self, current_ticks):
        self.scan_line_offset = (self.scan_line_offset + 1) % self.scanline_step
        self.flicker_timer = (self.flicker_timer + self.flicker_speed) % (2 * math.pi)
        self.flicker_intensity = abs(math.sin(self.flicker_timer)) * 0.5

        self.glitch_timer = (self.glitch_timer + self.glitch_speed) % (2 * math.pi)
        self.glitch_intensity = abs(math.sin(self.glitch_timer))
        self.glitch_active = (current_ticks % self.glitch_interval_ms) < self.glitch_window_ms


@dataclass
class AppState:
    player_stats: dict
    inventory: list
    special_stats: dict
    body_parts: dict
    animation: AnimationState


def create_initial_state():
    return AppState(
        player_stats=get_player_stats_data(),
        inventory=get_inventory_data(),
        special_stats=get_special_stats_data(),
        body_parts=get_body_parts_data(),
        animation=AnimationState()
    )