import pygame
from config import *

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 50
        self.size = CROSSHAIR_SIZE
        
    def update(self, x):
        # Keep crosshair within screen bounds
        self.x = max(self.size // 2, min(x, SCREEN_WIDTH - self.size // 2))
        
    def draw(self, screen):
        # Draw crosshair
        pygame.draw.circle(screen, GREEN, (self.x, self.y), self.size // 2, 2)
        pygame.draw.line(screen, GREEN, (self.x - self.size, self.y), (self.x + self.size, self.y), 2)
        pygame.draw.line(screen, GREEN, (self.x, self.y - self.size), (self.x, self.y + self.size), 2)