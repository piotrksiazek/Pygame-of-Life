import pygame
import numpy as np
import sys
import copy
from random import randint

class Cell:
    """Class that stores state of each individual cell"""
    def __init__(self):
        self.status = 0
        self.number_of_neighbours = 0

    def change_status(self):
        if self.status == 1:
            if self.number_of_neighbours < 2 or self.number_of_neighbours > 3:
                self.status = 0
        else:
            if self.number_of_neighbours == 3:
                self.status = 1

    def set_alive(self):
        self.status = 1

    def set_dead(self):
        self.status = 0

class Population:
    """Class that manages and draws the grid, animates the intro"""
    def __init__(self, gol):
        self.screen = pygame.display.set_mode((gol.settings.scr_width, gol.settings.scr_height))
        self.cell_size = gol.settings.cell_size
        self.width = gol.settings.scr_width
        self.height = gol.settings.scr_height
        self.rows = int(self.height / self.cell_size)
        self.columns = int(self.width / self.cell_size)
        self.grid = np.array([[Cell() for column in range(self.columns)] for row in range(self.rows)])
        self.game_speed = 100
        self.ready = False

        # Attributes used by intro.
        self.snake_grid = np.array([[Cell() for column in range(self.columns)] for row in range(self.rows)])
        self.intro = True
        self.intro_speed = 420

        # Used only to display "Pygame of life" at the beginnging.
        self.text_intro_color = (255, 0, 0)
        self.text_fade_speed = 400

        self.title_font = pygame.font.Font('assets/FFFFORWA.TTF', 32)
        self.title_text = self.title_font.render('Pygame of Life', True, self.text_intro_color)
        self.title_rect = self.title_text.get_rect()
        self.title_rect.center = (gol.settings.scr_width // 2, gol.settings.scr_height // 2)

        self.continue_font = pygame.font.Font('assets/FFFFORWA.TTF', 10)
        self.continue_text = self.continue_font.render('PRESS ANYTHING TO CONTINUE', True, self.text_intro_color)
        self.continue_rect = self.title_text.get_rect()
        self.continue_rect.center = (0.57*gol.settings.scr_width, gol.settings.scr_height)

    def create_snake_grid(self):
        snake_grid_list = []
        with open('assets/banner4.txt', 'r') as logo:
            for line in logo:
                line = list(line)
                snake_grid_list.append(line)

        for cell_line, ascii_line in zip(self.snake_grid, snake_grid_list):
            for cell_object, ascii_char in zip(cell_line, ascii_line):
                if ascii_char != ' ':
                    cell_object.set_alive()

    def exit_or_continue_intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # In case one wants to skip the intro
                if event.key == pygame.K_SPACE:
                    self.intro = False
                    pygame.mixer_music.fadeout(400)

    def animate_snake_grid(self, population, gol):
        # Loading and playing music for intro
        pygame.mixer_music.load('assets/Rick and Morty  Snake Jazz.mp3')
        pygame.mixer_music.play()

        self.create_snake_grid()
        # colors_of_life_intro index pointer
        i = 0
        while self.intro:
            pygame.time.delay(self.intro_speed)
            self.exit_or_continue_intro()
            alive_cell_color = gol.settings.colors_of_life_intro[i]
            pygame.time.delay(i)
            next_gen = population.draw_grid(self.screen, alive_cell_color, gol.settings.dead_intro_color, population.snake_grid)
            population.snake_grid = next_gen
            pygame.display.flip()
            i += 1
            # Animation speeds up every loop untill it reaches minimal speed.
            if self.intro_speed >= 20:
                self.intro_speed -= 100

            # Once i reaches length of list of intro animation colors, "Pygame of life" displays.
            if i >= len(gol.settings.colors_of_life_intro):
                pygame.mixer_music.fadeout(400)
                while self.intro:
                    self.intro_speed = 1200
                    self.exit_or_continue_intro()
                    self.screen.blit(self.title_text, self.title_rect)
                    self.screen.blit(self.continue_text, self.continue_rect)
                    pygame.display.flip()


    def pre_populate_events(self, grid):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Getting x and y coordinate of coursor and translating it into individual cell position
                x, y = pygame.mouse.get_pos()
                pos_x, pos_y = int(x/self.cell_size), int(y/self.cell_size)
                # If cell is alive then it's status will become dead
                if grid[pos_y][pos_x].status == 1:
                    grid[pos_y][pos_x].status = 0
                # If cell is dead then it's status will become alive
                else:
                    grid[pos_y][pos_x].status = 1
            elif event.type == pygame.KEYDOWN:
                # Press space to start the game
                if event.key == pygame.K_SPACE:
                    self.ready = True

    def pre_game(self, grid, alive_color, dead_color):
        while not self.ready:
            self.pre_populate_events(grid)
            for y in range(len(grid)):
                for x in range(len(grid[0])):
                    cell_rect = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                    if grid[y][x].status == 1:
                        pygame.draw.rect(self.screen, alive_color, cell_rect)
                    else:
                        pygame.draw.rect(self.screen, dead_color, cell_rect)
            pygame.display.flip()


    def draw_grid(self, screen, alive_color, dead_color, grid):
        #(left,top,width,height)
        alive = 1
        dead = 0
        next_generation = copy.deepcopy(grid)
        # Iterating over rows
        for y in range(len(grid)):
            # Iterating over columns
            for x in range(len(grid[0])):

                cell = next_generation[y][x]

                #upper left
                if y == 0 and x == 0:
                    cell.number_of_neighbours = grid[0][1].status + grid[1][0].status + grid[1][1].status
                    cell.change_status()

                #upper right
                elif y == 0 and x == len(grid[0]) - 1:
                    cell.number_of_neighbours = grid[0][-2].status + grid[1][-1].status + grid[1][-2].status
                    cell.change_status()

                #bottom left
                elif y == len(grid) - 1 and x == 0:
                    cell.number_of_neighbours = grid[-1][1].status + grid[-2][0].status + grid[-2][1].status
                    cell.change_status()

                #bottom right
                elif y == len(grid) - 1 and x == len(grid[0]) - 1:
                    cell.number_of_neighbours = grid[-1][-2].status + grid[-2][-1].status + grid[-2][-2].status
                    cell.change_status()

                #left
                elif 0 < y < len(grid) - 1 and x == 0:
                    cell.number_of_neighbours = (
                        grid[y-1][x].status + grid[y-1][x+1].status + grid[y][x+1].status +
                        grid[y+1][x].status + grid[y+1][x+1].status
                    )
                    cell.change_status()
                #right
                elif 0 < y < len(grid) - 1 and x == len(grid) - 1:
                    cell.number_of_neighbours = (
                        grid[y-1][x].status + grid[y-1][x-1].status + grid[y][x-1].status +
                        grid[y+1][x-1].status + grid[y+1][x].status
                    )
                    cell.change_status()
                #upper
                elif y == 0 and 0 < x < len(grid) - 1:
                    cell.number_of_neighbours = (
                        grid[y][x-1].status + grid[y][x+1].status + grid[y+1][x-1].status +
                        grid[y+1][x].status + grid[y+1][x+1].status
                    )
                    cell.change_status()
                #bottom
                elif y == len(grid) - 1 and 0 < x < len(grid) - 1:
                    cell.number_of_neighbours = (
                            grid[y][x-1].status + grid[y][x+1].status + grid[y-1][x-1].status +
                            grid[y-1][x].status + grid[y-1][x+1].status
                    )
                    cell.change_status()
                #inner
                elif 0 < y < len(grid) - 1 and 0 < x < len(grid[0]) - 1:
                    cell.number_of_neighbours = (
                            grid[y][x-1].status + grid[y][x+1].status + grid[y-1][x-1].status +
                            grid[y-1][x].status + grid[y-1][x+1].status + grid[y+1][x-1].status +
                            grid[y+1][x].status + grid[y+1][x+1].status
                    )
                    cell.change_status()

                cell_rect = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                if cell.status == 1:
                    pygame.draw.rect(screen, alive_color, cell_rect)
                else:
                    pygame.draw.rect(screen, dead_color, cell_rect)

        return next_generation