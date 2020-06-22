import os, sys
from itertools import cycle
import copy
from random import randint
import pygame
from pygame.locals import *
from settings import Settings

class MainMenu:
    """Takes care of color menu and user settings"""
    def __init__(self):
        self.color_ready = False
        self.color_menu_img = pygame.image.load('assets/color_menu_2.png')

    def check_color_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # We don't want to exceed max index of color array. gol.settings.max_color_of_life is the last index.
                if event.key == pygame.K_RIGHT and gol.settings.colors_of_life.index(gol.settings.alive_color) < gol.settings.max_color_of_life:
                    gol.settings.alive_color = gol.settings.colors_of_life[gol.settings.colors_of_life.index(gol.settings.alive_color)+1]
                elif event.key == pygame.K_LEFT and gol.settings.colors_of_life.index(gol.settings.alive_color) > 0:
                    gol.settings.alive_color = gol.settings.colors_of_life[gol.settings.colors_of_life.index(gol.settings.alive_color)-1]

                # The same thing but for colors of death.
                elif event.key == pygame.K_UP and gol.settings.colors_of_death.index(gol.settings.dead_color) < gol.settings.max_color_of_death:
                    gol.settings.dead_color = gol.settings.colors_of_death[gol.settings.colors_of_death.index(gol.settings.dead_color)+1]
                elif event.key == pygame.K_DOWN and gol.settings.colors_of_death.index(gol.settings.dead_color) > 0:
                    gol.settings.dead_color = gol.settings.colors_of_death[gol.settings.colors_of_death.index(gol.settings.dead_color)-1]

                # Pressing space breakes the choose_color loop.
                elif event.key == pygame.K_SPACE:
                    self.color_ready = True

    def choose_color(self):
        while not self.color_ready:
            self.check_color_events()
            gol.screen.fill(gol.settings.alive_color)

            # death_rect is drawn right behind transparent japaneese death symbol so we see only colorful sign.
            death_rect = pygame.Rect(
                gol.settings.scr_width - 0.20*gol.settings.scr_width, gol.settings.scr_height * 0.3,
                0.3*gol.settings.scr_width, 0.3*gol.settings.scr_width
            )
            pygame.draw.rect(gol.screen, gol.settings.dead_color, death_rect)
            gol.screen.blit(self.color_menu_img, (0,0))
            pygame.display.flip()


class Cell:
    """Class that stores state of each individual cell"""
    def __init__(self):
        self.status = randint(0,1)
        self.number_of_neighbours = 0

    def change_status(self):
        if self.status == 1:
            if self.number_of_neighbours < 2 or self.number_of_neighbours > 3:
                self.status = 0
        else:
            if self.number_of_neighbours == 3:
                self.status = 1

class Population:
    """Class that manages and draws the grid"""
    def __init__(self):
        self.screen = pygame.display.set_mode((gol.settings.scr_width, gol.settings.scr_height))
        self.cell_size = gol.settings.cell_size
        self.width = gol.settings.scr_width
        self.height = gol.settings.scr_height
        self.rows = int(self.height / self.cell_size)
        self.columns = int(self.width / self.cell_size)
        self.grid = [[Cell() for column in range(self.columns)] for row in range(self.rows)]
        self.ready = False

    def pre_populate_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Getting x and y coordinate of coursor and translating it into individual cell position
                x, y = pygame.mouse.get_pos()
                pos_x, pos_y = int(x/self.cell_size), int(y/self.cell_size)
                # If cell is alive then it's status will become dead
                if self.grid[pos_y][pos_x].status == 1:
                    self.grid[pos_y][pos_x].status = 0
                # If cell is dead then it's status will become alive
                else:
                    self.grid[pos_y][pos_x].status = 1
            elif event.type == pygame.KEYDOWN:
                # Press space to start the game
                if event.key == pygame.K_SPACE:
                    self.ready = True

    def pre_game(self):
        while not self.ready:
            self.pre_populate_events()
            for y in range(len(self.grid)):
                for x in range(len(self.grid[0])):
                    cell_rect = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                    if self.grid[y][x].status == 1:
                        pygame.draw.rect(self.screen, gol.settings.alive_color, cell_rect)
                    else:
                        pygame.draw.rect(self.screen, gol.settings.dead_color, cell_rect)
            pygame.display.flip()

    def draw_grid(self, screen):
        #(left,top,width,height)
        alive = 1
        dead = 0
        
        dead_color = gol.settings.dead_color
        alive_color = gol.settings.alive_color
        
        next_generation = copy.deepcopy(self.grid)
        # Iterating over rows
        for y in range(len(self.grid)):
            # Iterating over columns
            for x in range(len(self.grid[0])):

                cell = next_generation[y][x]

                #upper left
                if y == 0 and x == 0:
                    cell.number_of_neighbours = self.grid[0][1].status + self.grid[1][0].status + self.grid[1][1].status
                    cell.change_status()

                #upper right
                elif y == 0 and x == len(self.grid[0]) - 1:
                    cell.number_of_neighbours = self.grid[0][-2].status + self.grid[1][-1].status + self.grid[1][-2].status
                    cell.change_status()

                #bottom left
                elif y == len(self.grid) - 1 and x == 0:
                    cell.number_of_neighbours = self.grid[-1][1].status + self.grid[-2][0].status + self.grid[-2][1].status
                    cell.change_status()

                #bottom right
                elif y == len(self.grid) - 1 and x == len(self.grid[0]) - 1:
                    cell.number_of_neighbours = self.grid[-1][-2].status + self.grid[-2][-1].status + self.grid[-2][-2].status
                    cell.change_status()

                #left
                elif 0 < y < len(self.grid) - 1 and x == 0:
                    cell.number_of_neighbours = (
                        self.grid[y-1][x].status + self.grid[y-1][x+1].status + self.grid[y][x+1].status +
                        self.grid[y+1][x].status + self.grid[y+1][x+1].status
                    )
                    cell.change_status()
                #right
                elif 0 < y < len(self.grid) - 1 and x == len(self.grid) - 1:
                    cell.number_of_neighbours = (
                        self.grid[y-1][x].status + self.grid[y-1][x-1].status + self.grid[y][x-1].status +
                        self.grid[y+1][x-1].status + self.grid[y+1][x].status
                    )
                    cell.change_status()
                #upper
                elif y == 0 and 0 < x < len(self.grid) - 1:
                    cell.number_of_neighbours = (
                        self.grid[y][x-1].status + self.grid[y][x+1].status + self.grid[y+1][x-1].status +
                        self.grid[y+1][x].status + self.grid[y+1][x+1].status
                    )
                    cell.change_status()
                #bottom
                elif y == len(self.grid) - 1 and 0 < x < len(self.grid) - 1:
                    cell.number_of_neighbours = (
                            self.grid[y][x-1].status + self.grid[y][x+1].status + self.grid[y-1][x-1].status +
                            self.grid[y-1][x].status + self.grid[y-1][x+1].status
                    )
                    cell.change_status()
                #inner
                elif 0 < y < len(self.grid) - 1 and 0 < x < len(self.grid[0]) - 1:
                    cell.number_of_neighbours = (
                            self.grid[y][x-1].status + self.grid[y][x+1].status + self.grid[y-1][x-1].status +
                            self.grid[y-1][x].status + self.grid[y-1][x+1].status + self.grid[y+1][x-1].status +
                            self.grid[y+1][x].status + self.grid[y+1][x+1].status
                    )
                    cell.change_status()

                cell_rect = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                if cell.status == 1:
                    pygame.draw.rect(screen, gol.settings.alive_color, cell_rect)
                else:
                    pygame.draw.rect(screen, gol.settings.dead_color, cell_rect)

        return next_generation
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

    def main(self):
        population = Population()
        menu = MainMenu()
        menu.choose_color()
        population.pre_game()
        while True:
            pygame.time.delay(100)
            self.check_events()
            next_gen = population.draw_grid(self.screen)
            population.grid = next_gen
            pygame.display.flip()

gol = GameOfLife()
gol.main()


