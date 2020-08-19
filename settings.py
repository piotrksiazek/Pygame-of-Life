from random import randint

class Settings:
    def __init__(self):
        self.colors_of_life = [(255, 79, 51), (255,255,255), (163,5,0), (255,123,0), (200,0,0)]
        self.colors_of_life_intro = [(randint(1,255), randint(1,255), randint(1,255)) for x in range(10)]

        self.colors_of_death = [(219, 179, 123), (0,0,0), (0,241,84), (0,191,241), (255,255,255)]
        self.max_color_of_life = len(self.colors_of_life) - 1
        self.max_color_of_death = len(self.colors_of_death) - 1
        self.alive_color = self.colors_of_life[0]
        self.dead_color = self.colors_of_death[0]

        self.alive_intro_color = self.colors_of_life[0]
        self.dead_intro_color = (0,0,0)

        self.scr_width = 1000
        self.scr_height = 700

        self.menu_cell_size_list = ['size', '20', '10', '5', '2', '1']
        self.cell_size_list = [20, 10, 1]
        self.cell_size = self.cell_size_list[0]
        self.intro_cell_size = 5
