from dataclasses import dataclass

import pygame

from config import WINDOW_SIZE, WINDOW_TITLE


@dataclass
class UIFonts:
    large: pygame.font.Font
    medium: pygame.font.Font
    small: pygame.font.Font
    tiny: pygame.font.Font


@dataclass
class UIContext:
    screen: pygame.Surface
    width: int
    height: int
    fonts: UIFonts
    clock: pygame.time.Clock
    fps: int


def create_ui_context():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption(WINDOW_TITLE)

    try:
        fonts = UIFonts(
            large=pygame.font.Font(None, 48),
            medium=pygame.font.Font(None, 36),
            small=pygame.font.Font(None, 24),
            tiny=pygame.font.Font(None, 18)
        )
    except:
        fonts = UIFonts(
            large=pygame.font.SysFont('courier', 48),
            medium=pygame.font.SysFont('courier', 36),
            small=pygame.font.SysFont('courier', 24),
            tiny=pygame.font.SysFont('courier', 18)
        )

    return UIContext(
        screen=screen,
        width=WINDOW_SIZE[0],
        height=WINDOW_SIZE[1],
        fonts=fonts,
        clock=pygame.time.Clock(),
        fps=30
    )