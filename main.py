import sys
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
        self.playing = True
        self.after_game = True
        self.grid_from_image = False
        self.grid_image = 0
        self.b_and_w_resized = 0
        self.number_of_pauses = 3
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
                    # Each pause decreases number of possible pauses
                    if self.number_of_pauses > 0:
                        self.number_of_pauses -= 1
                    else:
                        self.playing = False

    def gameplay(self, interface, population, gol):
        # self.playing brakes once player spends all pause points.
        while self.playing:
            pygame.time.delay(100)
            interface.draw_bg(gol)
            # When game is paused and player has more pause points than 0
            while self.number_of_pauses > 0 and self.paused:
                if self.grid_from_image:
                    population.create_grid_from_ascii('obrazek.txt', population.grid)
                    self.grid_from_image = False
                population.pre_game(population.grid, gol.settings.alive_color, gol.settings.dead_color, gol, interface, population)
                interface.draw_bg(gol)
                interface.draw_and_update_counter(population, gol, population.number_of_generations)
                interface.draw_and_update_pop_counter(population, gol, population.count_living_cells())
                interface.display_number_of_pauses(gol, str(self.number_of_pauses))
                pygame.display.flip()
            self.check_events(population)
            next_gen = population.draw_grid(self.screen, gol.settings.alive_color, gol.settings.dead_color, population.grid, gol.settings.cell_size, 1)
            population.grid = next_gen
            interface.display_number_of_pauses(gol, str(self.number_of_pauses))
            interface.draw_and_update_counter(population, gol, population.number_of_generations)
            interface.draw_and_update_pop_counter(population, gol, population.number_of_living_cells)
            pygame.display.flip()
        
    def main(self):
        intro = population_and_intro.Population(gol)
        intro.create_grid_from_ascii('assets/banner4.txt', intro.snake_grid)
        menu = text_and_menu.MainMenu(gol)

        # intro.animate_snake_grid(intro, gol)
        menu.draw_menu(gol)

        population = population_and_intro.Population(gol)
        interface = text_and_menu.Interface(gol, population)

        # After intro and menus are over.
        self.gameplay(interface, population, gol)

        while self.after_game:
            pass

gol = GameOfLife()
gol.main()


