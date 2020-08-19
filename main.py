import sys
import pygame
from settings import Settings
import population_and_intro
import text_and_menu
from random import randint

class GameOfLife:
    """General class control game behaviour"""
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Pygame of Life')
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.scr_width, self.settings.scr_height))
        self.paused = True
        self.grid_from_image = False
        self.is_hoffman_dreaming = False

    def check_events(self, population, menu, interface):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:

                ### Changing cell state with left clicking ###
                if pygame.mouse.get_pressed()[0]:
                    # Getting x and y coordinate of coursor and translating it into individual cell position
                    x, y = pygame.mouse.get_pos()
                    pos_x, pos_y = int(x / gol.settings.cell_size), int(y / gol.settings.cell_size)

                    #Clicking anywhere hides error message
                    menu.is_error = False
                    # Cell status can be changed only in a square plane.
                    if x < gol.settings.scr_height:
                        # If cell is alive then it's status will become dead
                        if population.grid[pos_y][pos_x].status == 1:
                            population.grid[pos_y][pos_x].status = 0
                        # If cell is dead then it's status will become alive
                        else:
                            population.grid[pos_y][pos_x].status = 1

                    # Changing color sets to right
                    elif menu.color_r_arrow.is_over() and gol.settings.alive_color != gol.settings.colors_of_life[-1]:
                        gol.settings.alive_color = gol.settings.colors_of_life[gol.settings.colors_of_life.index(gol.settings.alive_color) + 1]
                        gol.settings.dead_color = gol.settings.colors_of_death[gol.settings.colors_of_death.index(gol.settings.dead_color) + 1]

                    # Changing color sets to left
                    elif menu.color_l_arrow.is_over() and gol.settings.alive_color != gol.settings.colors_of_life[0]:
                        gol.settings.alive_color = gol.settings.colors_of_life[gol.settings.colors_of_life.index(gol.settings.alive_color) - 1]
                        gol.settings.dead_color = gol.settings.colors_of_death[gol.settings.colors_of_death.index(gol.settings.dead_color) - 1]

                    elif menu.seed_from_image.is_over() and self.paused:
                        menu.create_ascii_art(menu.b_and_w_resized(gol, menu.get_str_of_img_path(), interface), gol)
                        if menu.image_open_success:
                            population.create_grid_from_ascii('ascii_art.txt', population.grid)
                            self.grid_from_image = True

                    elif menu.hoffmans_dream_button.is_over():
                        # Start and stop Albert Hoffman's imagination. Random colors on and off.
                        if self.is_hoffman_dreaming:
                            self.is_hoffman_dreaming = False
                            gol.settings.alive_color = gol.settings.colors_of_life[0]
                        else:
                            self.is_hoffman_dreaming = True

                    # Change cell size right arrow
                    elif menu.size_r_arrow.is_over() and menu.size_button.text != gol.settings.menu_cell_size_list[-1] and self.paused:
                        menu.size_button.text = str(gol.settings.menu_cell_size_list[gol.settings.menu_cell_size_list.index(menu.size_button.text)+1])
                        # Don't want to cast types if self.size_button.text is literally text.
                        if menu.size_button.text != 'size':
                            gol.settings.cell_size = int(menu.size_button.text)
                            population.update_grid_with_cell_size(gol)
                            # We want to be able to change cell size settings for selected image.
                            if gol.grid_from_image:
                                menu.create_ascii_art(menu.b_and_w_resized(gol, menu.image_path, interface), gol)
                                population.create_grid_from_ascii('ascii_art.txt', population.grid)


                    # Change cell size left arrow
                    elif menu.size_l_arrow.is_over() and menu.size_button.text != gol.settings.menu_cell_size_list[0] and self.paused:
                        menu.size_button.text = str(gol.settings.menu_cell_size_list[gol.settings.menu_cell_size_list.index(menu.size_button.text)-1])
                        if menu.size_button.text != 'size':
                            gol.settings.cell_size = int(menu.size_button.text)
                            population.update_grid_with_cell_size(gol)
                            # We want to be able to change cell size settings for selected image.
                            if gol.grid_from_image:
                                menu.create_ascii_art(menu.b_and_w_resized(gol, menu.image_path, interface), gol)
                                population.create_grid_from_ascii('ascii_art.txt', population.grid)


                    elif menu.pause_button.is_over():
                        if self.paused:
                            self.paused = False
                        else:
                            self.paused = True

                    elif menu.randomize_button.is_over():
                        for y in population.grid:
                            for cell in y:
                                cell.status = randint(0,1)

                    elif menu.reset_button.is_over():
                        for y in population.grid:
                            for cell in y:
                                cell.status = 0
                        population.number_of_generations = 0


            # Press space to start the game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.paused:
                    self.paused = False

                # This lets us pause the game and modify living and dead cells
                elif event.key == pygame.K_SPACE and not self.paused:
                    self.paused = True


    def hoffmans_dream(self, gol):
        if self.is_hoffman_dreaming:
            gol.settings.alive_color = (randint(0,255), randint(0,255), randint(0,255))

    # Contains functions that are common between pause and play time
    def common_functions(self, population, menu, interface):
        interface.draw_bg(gol)
        if self.is_hoffman_dreaming:
            self.hoffmans_dream(gol)
        self.check_events(population, menu, interface)
        menu.draw_menu_(gol, interface)
        interface.draw_and_update_counters(interface, population, gol)
        pygame.display.flip()

    def gameplay(self, interface, population, gol, menu):
        while True:
            pygame.time.delay(100)
            while self.paused:
                population.pre_game(population.grid, gol.settings.alive_color, gol.settings.dead_color, gol, interface, population)
                self.common_functions(population, menu, interface)
                population.redraw_cells_after_size_change(population.grid, gol.screen, gol.settings.alive_color, gol.settings.dead_color, gol)
            next_gen = population.draw_grid(self.screen, gol.settings.alive_color, gol.settings.dead_color, population.grid, gol.settings.cell_size, 1)
            population.grid = next_gen
            self.common_functions(population, menu, interface)

    def main(self):
        intro = population_and_intro.Population(gol)
        intro.create_grid_from_ascii('assets/banner4.txt', intro.snake_grid)
        intro.animate_snake_grid(intro, gol)

        population = population_and_intro.Population(gol)
        interface = text_and_menu.Interface(gol)
        menu = text_and_menu.MainMenu(gol, interface)
        # After intro and menus are over.
        self.gameplay(interface, population, gol, menu)

gol = GameOfLife()
gol.main()


