import pygame
import cv2
from game.game_loop import GameLoop

def main():
    pygame.init()
    game = GameLoop()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()
    
# py -3.10 main.py