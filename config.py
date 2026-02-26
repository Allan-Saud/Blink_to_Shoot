import pygame
import os

# Initialize pygame first
pygame.init()

# Then get screen info
screen_info = pygame.display.Info()
FULL_WIDTH = screen_info.current_w
FULL_HEIGHT = screen_info.current_h

# Split into two equal halves
SCREEN_WIDTH = FULL_WIDTH // 2
SCREEN_HEIGHT = FULL_HEIGHT

# Game settings
FPS = 30
GAME_DURATION = 60  # seconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player settings
CROSSHAIR_SIZE = 30
CROSSHAIR_SPEED = 10

# Enemy settings
ENEMY_SIZE = 40
ENEMY_SPAWN_RATE = 1.5  # seconds
ENEMY_SPEED = 3

# Bullet settings
BULLET_SIZE = 10
BULLET_SPEED = 10

# Blink detection
EAR_THRESHOLD = 0.2
EAR_CONSECUTIVE_FRAMES = 2