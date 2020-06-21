import os, sys
import pygame
from pygame.locals import *
from settings import Settings

class GameOfLife:
    """General class control game behaviour"""
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Pygame of Life')
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.scr_width, self.settings.scr_height))

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def draw_grid(self):
        pass

    def main_loop(self):
        while True:
            self.check_events()

gol = GameOfLife()
gol.main_loop()


