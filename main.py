import os, sys
import pygame
from settings import Settings
import population_and_intro
import text_and_menu

class GameOfLife:
    """General class control game behaviour"""
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Pygame of Life')
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.scr_width, self.settings.scr_height))
        self.paused = True
        self.mode_list = ['mode', 'death', 'life', 'classic']
        self.mode = self.mode_list[0]


    def check_events(self, population):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # This lets us pause the game and modify living and dead cells
                if event.key == pygame.K_SPACE:
                    self.paused = True
    
    # def make_love_not_war(self, gol, population):
    #     next_gen = population.draw_grid(self.screen, gol.settings.alive_color, gol.settings.dead_color, population.grid, gol.settings.cell_size, 1)
    #     population.grid = next_gen

    def main(self):

        intro = population_and_intro.Population(gol)
        intro.create_snake_grid()
        menu = text_and_menu.MainMenu(gol)

        intro.animate_snake_grid(intro, gol)
        menu.draw_menu(gol)
        population = population_and_intro.Population(gol)
        interface = text_and_menu.Interface(gol, population)
        # menu.choose_color(gol)

        # population.pre_game(population.snake_grid, gol.settings.alive_intro_color, gol.settings.dead_intro_color)
        # population.pre_game(population.grid, gol.settings.alive_color, gol.settings.dead_color)
        # After intro and menus are over.
        while True:
            pygame.time.delay(100)
            interface.draw_bg(gol)
            while self.paused:
                population.pre_game(population.grid, gol.settings.alive_color, gol.settings.dead_color, gol, interface, population)
                interface.draw_bg(gol)
                interface.draw_and_update_counter(population, gol, interface.interface_rect.centerx, 20, population.number_of_generations)
                interface.draw_and_update_pop_counter(population, gol, interface.interface_rect.centerx, 60, population.count_living_cells())
                pygame.display.flip()
            self.check_events(population)
            next_gen = population.draw_grid(self.screen, gol.settings.alive_color, gol.settings.dead_color, population.grid, gol.settings.cell_size, 1)
            population.grid = next_gen
            interface.draw_and_update_counter(population, gol, interface.interface_rect.centerx, 20, population.number_of_generations)
            interface.draw_and_update_pop_counter(population, gol, interface.interface_rect.centerx, 60, population.number_of_living_cells)
            pygame.display.flip()

gol = GameOfLife()
gol.main()


