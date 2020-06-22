import pygame
from random import randint

class Settings:
    def __init__(self):
        self.scr_width = 1000
        self.scr_height = 1000
        self.cell_size = 20
        self.alive_color = (randint(1,255),randint(1,255),randint(1,255))
        self.dead_color = (randint(1,255),randint(1,255),randint(1,255))