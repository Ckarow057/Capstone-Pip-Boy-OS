import pygame
import sys
import math
from datetime import datetime

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pip-Boy 3000 Mark IV")

# Pip-Boy color palette (green monochrome CRT style)
PIP_GREEN = (51, 255, 51)
PIP_GREEN_DARK = (20, 100, 20)
PIP_GREEN_BRIGHT = (102, 255, 102)
PIP_GREEN_DIM = (30, 180, 30)
BACKGROUND = (10, 20, 10)
SCANLINE_COLOR = (0, 0, 0, 30)

# Fonts
try:
    font_large = pygame.font.Font(None, 48)
    font_medium = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 24)
    font_tiny = pygame.font.Font(None, 18)
except:
    font_large = pygame.font.SysFont('courier', 48)
    font_medium = pygame.font.SysFont('courier', 36)
    font_small = pygame.font.SysFont('courier', 24)
    font_tiny = pygame.font.SysFont('courier', 18)

# Clock for FPS
clock = pygame.time.Clock()
FPS = 30

# Animation variables
scan_line_offset = 0
flicker_timer = 0
glitch_timer = 0

# Player stats (example data)
player_stats = {
    "name": "VAULT DWELLER",
    "level": 1,
    "hp": 200,
    "max_hp": 200,
    "ap": 80,
    "max_ap": 80,
    "rads": 12,
    "xp": 10,
    "next_level": 200,
    "caps": 542,
    "condition": 85,
    "effects": 0
}

# Inventory items
inventory = [
    {"name": "Stimpak", "count": 5, "hotkey": "S"},
    {"name": "Doctor's Bag", "count": 3, "hotkey": "E"}
]

# SPECIAL stats
special_stats = {
    "S": 7,  # Strength
    "P": 6,  # Perception
    "E": 5,  # Endurance
    "C": 4,  # Charisma
    "I": 8,  # Intelligence
    "A": 6,  # Agility
    "L": 5   # Luck
}

# Body part health (0-100 for each limb)
body_parts = {
    "head": 100,
    "torso": 85,
    "left_arm": 90,
    "right_arm": 100,
    "left_leg": 75,
    "right_leg": 80
}

def draw_scanlines(surface):
    """Draw CRT scanlines effect"""
    scanline_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    for y in range(0, SCREEN_HEIGHT, 4):
        pygame.draw.line(scanline_surface, SCANLINE_COLOR, (0, y), (SCREEN_WIDTH, y), 2)
    surface.blit(scanline_surface, (0, 0))

def draw_crt_effect(surface, flicker_intensity=0):
    """Add CRT flicker and vignette effect"""
    if flicker_intensity > 0:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, int(flicker_intensity * 10)))
        surface.blit(overlay, (0, 0))

def draw_border(surface):
    """Draw the main Pip-Boy border"""
    # Outer border
    pygame.draw.rect(surface, PIP_GREEN, (10, 10, SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20), 3)
    pygame.draw.rect(surface, PIP_GREEN_DARK, (15, 15, SCREEN_WIDTH - 30, SCREEN_HEIGHT - 30), 2)
    
    # Corner decorations
def draw_text_with_glow(surface, text, pos, font, color=PIP_GREEN, glow=True):
    """Draw text with optional glow effect"""
    if glow:
        # Draw glow
        glow_text = font.render(text, True, PIP_GREEN_DARK)
        for offset_x in [-2, -1, 0, 1, 2]:
            for offset_y in [-2, -1, 0, 1, 2]:
                if offset_x != 0 or offset_y != 0:
                    surface.blit(glow_text, (pos[0] + offset_x, pos[1] + offset_y))
    
    # Draw main text
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)
    return text_surface.get_width()

def draw_header(surface):
    """Draw the top header section with stats boxes"""
    # STATS label on the left
    draw_text_with_glow(surface, "STATS", (60, 25), font_medium, PIP_GREEN_BRIGHT, False)
    
    # Stats boxes across the top
    box_y = 20
    box_height = 40
    
    # LVL box
    lvl_x = 220
    pygame.draw.rect(surface, PIP_GREEN, (lvl_x, box_y, 120, box_height), 2)
    draw_text_with_glow(surface, f"LVL  {player_stats['level']}", (lvl_x + 10, box_y + 10), font_small, PIP_GREEN, False)
    
    # HP box
    hp_x = 360
    pygame.draw.rect(surface, PIP_GREEN, (hp_x, box_y, 180, box_height), 2)
    draw_text_with_glow(surface, f"HP  {player_stats['hp']}/{player_stats['max_hp']}", (hp_x + 10, box_y + 10), font_small, PIP_GREEN, False)
    
    # AP box
    ap_x = 560
    pygame.draw.rect(surface, PIP_GREEN, (ap_x, box_y, 150, box_height), 2)
    draw_text_with_glow(surface, f"AP  {player_stats['ap']}/{player_stats['max_ap']}", (ap_x + 10, box_y + 10), font_small, PIP_GREEN, False)
    
    # XP box
    xp_x = 730
    pygame.draw.rect(surface, PIP_GREEN, (xp_x, box_y, 180, box_height), 2)
    draw_text_with_glow(surface, f"XP  {player_stats['xp']}/{player_stats['next_level']}", (xp_x + 10, box_y + 10), font_small, PIP_GREEN, False)
    
    # Separator line
    pygame.draw.line(surface, PIP_GREEN, (30, 75), (SCREEN_WIDTH - 30, 75), 2)

def draw_vault_boy(surface):
    """Draw the Vault Boy figure in the center with body part indicators"""
    center_x = SCREEN_WIDTH // 2
    center_y = 350
    
    # Head
    head_radius = 45
    head_y = center_y - 150
    head_color = PIP_GREEN if body_parts["head"] > 50 else (255, 255, 51)
    pygame.draw.circle(surface, head_color, (center_x, head_y), head_radius, 3)
    # Face details
    pygame.draw.circle(surface, head_color, (center_x - 15, head_y - 5), 5, 2)  # Left eye
    pygame.draw.circle(surface, head_color, (center_x + 15, head_y - 5), 5, 2)  # Right eye
    pygame.draw.arc(surface, head_color, (center_x - 15, head_y + 10, 30, 15), 3.14, 0, 2)  # Smile
    
    # Neck
    pygame.draw.line(surface, PIP_GREEN, (center_x, head_y + head_radius), (center_x, center_y - 80), 3)
    
    # Torso
    torso_width = 80
    torso_height = 100
    torso_color = PIP_GREEN if body_parts["torso"] > 50 else (255, 255, 51)
    pygame.draw.rect(surface, torso_color, (center_x - torso_width//2, center_y - 80, torso_width, torso_height), 3)
    
    # Left arm
    left_arm_color = PIP_GREEN if body_parts["left_arm"] > 50 else (255, 255, 51)
    arm_start_y = center_y - 60
    # Upper arm
    pygame.draw.line(surface, left_arm_color, (center_x - torso_width//2, arm_start_y), 
                     (center_x - torso_width//2 - 60, arm_start_y + 40), 5)
    # Lower arm
    pygame.draw.line(surface, left_arm_color, (center_x - torso_width//2 - 60, arm_start_y + 40),
                     (center_x - torso_width//2 - 80, arm_start_y + 100), 5)
    # Hand
    pygame.draw.circle(surface, left_arm_color, (center_x - torso_width//2 - 80, arm_start_y + 100), 10, 3)
    
    # Right arm
    right_arm_color = PIP_GREEN if body_parts["right_arm"] > 50 else (255, 255, 51)
    # Upper arm
    pygame.draw.line(surface, right_arm_color, (center_x + torso_width//2, arm_start_y),
                     (center_x + torso_width//2 + 60, arm_start_y + 40), 5)
    # Lower arm
    pygame.draw.line(surface, right_arm_color, (center_x + torso_width//2 + 60, arm_start_y + 40),
                     (center_x + torso_width//2 + 80, arm_start_y + 100), 5)
    # Hand
    pygame.draw.circle(surface, right_arm_color, (center_x + torso_width//2 + 80, arm_start_y + 100), 10, 3)
    
    # Left leg
    left_leg_color = PIP_GREEN if body_parts["left_leg"] > 50 else (255, 255, 51)
    leg_start_y = center_y + 20
    # Upper leg
    pygame.draw.line(surface, left_leg_color, (center_x - 20, leg_start_y),
                     (center_x - 25, leg_start_y + 70), 6)
    # Lower leg
    pygame.draw.line(surface, left_leg_color, (center_x - 25, leg_start_y + 70),
                     (center_x - 20, leg_start_y + 140), 6)
    # Foot
    pygame.draw.line(surface, left_leg_color, (center_x - 20, leg_start_y + 140),
                     (center_x - 5, leg_start_y + 140), 6)
    
    # Right leg
    right_leg_color = PIP_GREEN if body_parts["right_leg"] > 50 else (255, 255, 51)
    # Upper leg
    pygame.draw.line(surface, right_leg_color, (center_x + 20, leg_start_y),
                     (center_x + 25, leg_start_y + 70), 6)
    # Lower leg
    pygame.draw.line(surface, right_leg_color, (center_x + 25, leg_start_y + 70),
                     (center_x + 20, leg_start_y + 140), 6)
    # Foot
    pygame.draw.line(surface, right_leg_color, (center_x + 20, leg_start_y + 140),
                     (center_x + 35, leg_start_y + 140), 6)
    
    # Body part health bars pointing to limbs
    bar_width = 80
    bar_height = 12
    
    # Head bar (above)
    head_bar_x = center_x - bar_width // 2
    head_bar_y = head_y - 80
    pygame.draw.rect(surface, PIP_GREEN_DARK, (head_bar_x, head_bar_y, bar_width, bar_height), 0)
    pygame.draw.rect(surface, head_color, (head_bar_x, head_bar_y, bar_width, bar_height), 2)
    fill = int((body_parts['head'] / 100) * bar_width)
    pygame.draw.rect(surface, head_color, (head_bar_x, head_bar_y, fill, bar_height), 0)
    # Line to head
    pygame.draw.line(surface, head_color, (center_x, head_bar_y + bar_height), (center_x, head_y - head_radius), 2)
    
    # Torso bar (on torso)
    torso_bar_x = center_x - bar_width // 2
    torso_bar_y = center_y - 30
    pygame.draw.rect(surface, PIP_GREEN_DARK, (torso_bar_x, torso_bar_y, bar_width, bar_height), 0)
    pygame.draw.rect(surface, torso_color, (torso_bar_x, torso_bar_y, bar_width, bar_height), 2)
    fill = int((body_parts['torso'] / 100) * bar_width)
    pygame.draw.rect(surface, torso_color, (torso_bar_x, torso_bar_y, fill, bar_height), 0)
    
    # Left arm bar
    left_arm_bar_x = center_x - torso_width//2 - 150
    left_arm_bar_y = arm_start_y + 20
    pygame.draw.rect(surface, PIP_GREEN_DARK, (left_arm_bar_x, left_arm_bar_y, bar_width, bar_height), 0)
    pygame.draw.rect(surface, left_arm_color, (left_arm_bar_x, left_arm_bar_y, bar_width, bar_height), 2)
    fill = int((body_parts['left_arm'] / 100) * bar_width)
    pygame.draw.rect(surface, left_arm_color, (left_arm_bar_x, left_arm_bar_y, fill, bar_height), 0)
    # Line to arm
    pygame.draw.line(surface, left_arm_color, (left_arm_bar_x + bar_width, left_arm_bar_y + bar_height//2),
                     (center_x - torso_width//2 - 40, arm_start_y + 20), 2)
    
    # Right arm bar
    right_arm_bar_x = center_x + torso_width//2 + 70
    right_arm_bar_y = arm_start_y + 20
    pygame.draw.rect(surface, PIP_GREEN_DARK, (right_arm_bar_x, right_arm_bar_y, bar_width, bar_height), 0)
    pygame.draw.rect(surface, right_arm_color, (right_arm_bar_x, right_arm_bar_y, bar_width, bar_height), 2)
    fill = int((body_parts['right_arm'] / 100) * bar_width)
    pygame.draw.rect(surface, right_arm_color, (right_arm_bar_x, right_arm_bar_y, fill, bar_height), 0)
    # Line to arm
    pygame.draw.line(surface, right_arm_color, (right_arm_bar_x, right_arm_bar_y + bar_height//2),
                     (center_x + torso_width//2 + 40, arm_start_y + 20), 2)
    
    # Left leg bar
    left_leg_bar_x = center_x - 150
    left_leg_bar_y = leg_start_y + 70
    pygame.draw.rect(surface, PIP_GREEN_DARK, (left_leg_bar_x, left_leg_bar_y, bar_width, bar_height), 0)
    pygame.draw.rect(surface, left_leg_color, (left_leg_bar_x, left_leg_bar_y, bar_width, bar_height), 2)
    fill = int((body_parts['left_leg'] / 100) * bar_width)
    pygame.draw.rect(surface, left_leg_color, (left_leg_bar_x, left_leg_bar_y, fill, bar_height), 0)
    # Line to leg
    pygame.draw.line(surface, left_leg_color, (left_leg_bar_x + bar_width, left_leg_bar_y + bar_height//2),
                     (center_x - 25, leg_start_y + 40), 2)
    
    # Right leg bar
    right_leg_bar_x = center_x + 70
    right_leg_bar_y = leg_start_y + 70
    pygame.draw.rect(surface, PIP_GREEN_DARK, (right_leg_bar_x, right_leg_bar_y, bar_width, bar_height), 0)
    pygame.draw.rect(surface, right_leg_color, (right_leg_bar_x, right_leg_bar_y, bar_width, bar_height), 2)
    fill = int((body_parts['right_leg'] / 100) * bar_width)
    pygame.draw.rect(surface, right_leg_color, (right_leg_bar_x, right_leg_bar_y, fill, bar_height), 0)
    # Line to leg
    pygame.draw.line(surface, right_leg_color, (right_leg_bar_x, right_leg_bar_y + bar_height//2),
                     (center_x + 25, leg_start_y + 40), 2)
    
    # Level text below the figure
    level_text = f"Level {player_stats['level']}"
    level_surface = font_medium.render(level_text, True, PIP_GREEN)
    level_x = (SCREEN_WIDTH - level_surface.get_width()) // 2
    draw_text_with_glow(surface, level_text, (level_x, center_y + 180), font_medium, PIP_GREEN, False)

def draw_left_labels(surface):
    """Draw CND, RAD, EFF labels on the left side"""
    start_x = 60
    start_y = 110
    
    # CND (Condition) box
    pygame.draw.rect(surface, PIP_GREEN, (start_x, start_y, 80, 40), 2)
    draw_text_with_glow(surface, "CND", (start_x + 15, start_y + 10), font_small, PIP_GREEN, False)
    
    # RAD (Radiation)
    draw_text_with_glow(surface, "RAD", (start_x + 5, start_y + 70), font_medium, PIP_GREEN, False)
    
    # EFF (Effects)
    draw_text_with_glow(surface, "EFF", (start_x + 5, start_y + 130), font_medium, PIP_GREEN, False)

def draw_equipment_info(surface):
    """Draw equipment/inventory items on the right side"""
    start_x = SCREEN_WIDTH - 280
    start_y = 110
    
    # Draw inventory items
    y_offset = start_y
    for item in inventory:
        item_text = f"({item['count']}) {item['name']} {item['hotkey']})"
        draw_text_with_glow(surface, item_text, (start_x, y_offset), font_small, PIP_GREEN_DIM, False)
        y_offset += 60

def draw_tabs(surface):
    """Draw navigation tabs at bottom"""
    tab_y = SCREEN_HEIGHT - 80
    tabs = ["Status", "Special", "Skills", "Perks", "General"]
    tab_width = 160
    start_x = 120
    
    for i, tab in enumerate(tabs):
        tab_x = start_x + (i * tab_width)
        
        # Tab background (selected: Status)
        if i == 0:
            pygame.draw.rect(surface, PIP_GREEN_DARK, (tab_x, tab_y, tab_width - 10, 40), 0)
        
        # Tab border
        pygame.draw.rect(surface, PIP_GREEN, (tab_x, tab_y, tab_width - 10, 40), 2)
        
        # Tab text
        text_color = PIP_GREEN_BRIGHT if i == 0 else PIP_GREEN
        text_surface = font_small.render(tab, True, text_color)
        text_rect = text_surface.get_rect(center=(tab_x + (tab_width - 10) // 2, tab_y + 20))
        surface.blit(text_surface, text_rect)

def draw_glitch_effect(surface, intensity):
    """Occasionally draw glitch effect for authenticity"""
    if intensity > 0.8:
        # Random horizontal lines
        for _ in range(3):
            y = pygame.time.get_ticks() % SCREEN_HEIGHT
            pygame.draw.line(surface, PIP_GREEN_BRIGHT, (0, y), (SCREEN_WIDTH, y), 2)

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Clear screen
    screen.fill(BACKGROUND)
    
    # Update animation timers
    scan_line_offset = (scan_line_offset + 1) % 4
    flicker_timer = (flicker_timer + 0.1) % (2 * math.pi)
    flicker_intensity = abs(math.sin(flicker_timer)) * 0.5
    
    glitch_timer = (glitch_timer + 0.05) % (2 * math.pi)
    glitch_intensity = abs(math.sin(glitch_timer))
    
    # Draw all UI elements
    draw_border(screen)
    draw_header(screen)
    draw_left_labels(screen)
    draw_vault_boy(screen)
    draw_equipment_info(screen)
    draw_tabs(screen)
    
    # Draw CRT effects
    draw_scanlines(screen)
    draw_crt_effect(screen, flicker_intensity)
    
    # Occasional glitch effect
    if pygame.time.get_ticks() % 3000 < 50:
        draw_glitch_effect(screen, glitch_intensity)
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Quit
pygame.quit()
sys.exit()

