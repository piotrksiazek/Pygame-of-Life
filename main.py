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

    def check_events(self, population):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # This lets us pause the game and modify living and dead cells
                if event.key == pygame.K_SPACE:
                    population.ready = False
                    population.pre_game(population.grid, gol.settings.alive_color, gol.settings.dead_color)


    def main(self):

        population = population_and_intro.Population(gol)
        population.create_snake_grid()
        menu = text_and_menu.MainMenu(gol)

        population.animate_snake_grid(population, gol)

        menu.choose_color(gol)
        # population.pre_game(population.snake_grid, gol.settings.alive_intro_color, gol.settings.dead_intro_color)
        # population.pre_game(population.grid, gol.settings.alive_color, gol.settings.dead_color)
        # After intro and menus are over.
        while True:
            pygame.time.delay(100)
            self.check_events(population)
            next_gen = population.draw_grid(self.screen, gol.settings.alive_color, gol.settings.dead_color, population.grid)
            population.grid = next_gen
            # self.screen.blit(text.text, text.rect)
            pygame.display.flip()

gol = GameOfLife()
gol.main()


