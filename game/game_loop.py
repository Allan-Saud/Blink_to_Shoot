import os
import pygame
import cv2
import time
import random
import numpy as np
from config import *
from game.player import Player
from game.enemy import Enemy
from game.bullet import Bullet
from detection.face_tracker import FaceTracker
from detection.blink_detector import BlinkDetector

class GameLoop:
    def __init__(self):
        # Force game window top-left
        os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
        pygame.init()

        # Game window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Blink to Shoot")
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.start_time = time.time()

        # Game objects
        self.player = Player()
        self.enemies = []
        self.bullets = []
        self.face_tracker = FaceTracker()
        self.blink_detector = BlinkDetector()
        self.last_enemy_spawn = 0

        # Webcam
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, SCREEN_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, SCREEN_HEIGHT)
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            self.running = False

    def run(self):
        try:
            while self.running:
                self.handle_events()
                self.update()
                self.render()
                self.clock.tick(FPS)
        finally:
            self.cap.release()
            pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # Flip frame for mirror effect
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.frame = frame  # store for render

        # Face tracking & blink detection
        face_results = self.face_tracker.process_frame(frame)
        blink_results = self.blink_detector.process_frame(frame)

        if face_results:
            nose_x = face_results['nose_x']
            screen_x = int(nose_x * SCREEN_WIDTH)
            self.player.update(screen_x)

        if blink_results and blink_results['blink_detected']:
            self.bullets.append(Bullet(self.player.x, self.player.y))

        # Spawn enemies
        current_time = time.time()
        if current_time - self.last_enemy_spawn > ENEMY_SPAWN_RATE:
            self.enemies.append(Enemy())
            self.last_enemy_spawn = current_time

        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.y > SCREEN_HEIGHT:
                self.enemies.remove(enemy)

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y < 0:
                self.bullets.remove(bullet)

        # Check collisions
        self.check_collisions()

        # Check game over
        if time.time() - self.start_time > GAME_DURATION:
            self.running = False

    def check_collisions(self):
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if (abs(bullet.x - enemy.x) < (BULLET_SIZE + ENEMY_SIZE) // 2 and
                    abs(bullet.y - enemy.y) < (BULLET_SIZE + ENEMY_SIZE) // 2):
                    self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    self.score += 1
                    break

    def render(self):
        # Draw webcam frame as background
        if hasattr(self, 'frame'):
            frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            frame_rgb = np.rot90(frame_rgb)  # match Pygame coordinates
            frame_surface = pygame.surfarray.make_surface(frame_rgb)
            self.screen.blit(frame_surface, (0, 0))

        # Draw player, enemies, bullets
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)

        # Draw score and timer
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        elapsed = int(time.time() - self.start_time)
        remaining = max(0, GAME_DURATION - elapsed)
        timer_text = font.render(f"Time: {remaining}s", True, (255, 255, 255))
        self.screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))

        pygame.display.flip()