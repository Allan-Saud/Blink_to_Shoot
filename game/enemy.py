import pygame
import random
from config import *

class Enemy:
    def __init__(self):
        self.size = ENEMY_SIZE
        self.x = random.randint(self.size, SCREEN_WIDTH - self.size)
        self.y = -self.size
        self.speed = ENEMY_SPEED
        
    def update(self):
        self.y += self.speed
        
    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.size // 2)