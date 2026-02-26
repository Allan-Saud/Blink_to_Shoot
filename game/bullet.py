import pygame
from config import *

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = BULLET_SIZE
        self.speed = BULLET_SPEED
        
    def update(self):
        self.y -= self.speed
        
    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (self.x, self.y), self.size // 2)