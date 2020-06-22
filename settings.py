import pygame
from random import randint

class Settings:
    def __init__(self):
        self.scr_width = 500
        self.scr_height = 500
        self.cell_size = 10
        self.alive_color = (255,0,255)
        self.dead_color = (0,255,0)