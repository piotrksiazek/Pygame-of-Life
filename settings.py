import pygame
from random import randint

class Settings:
    def __init__(self):
        self.colors_of_life = [(100,0,40), (255,0,0), (0,255,0), (0,0,255)]
        self.colors_of_death = [(0,0,0), (20,20,20), (150,150,150), (255,0,0)]
        self.max_color_of_life = len(self.colors_of_life) - 1
        self.max_color_of_death = len(self.colors_of_death) - 1
        self.alive_color = self.colors_of_life[0]
        self.dead_color = self.colors_of_death[0]
        self.alive_intro_color = (100,0,40)
        self.dead_intro_color = (0,0,0)
        self.scr_width = 700
        self.scr_height = 700
        self.cell_size = 5
