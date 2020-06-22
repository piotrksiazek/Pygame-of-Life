import os, sys
import copy
from random import randint
import pygame
from pygame.locals import *
from settings import Settings

class Cell:
    """Class that stores state of each individual cell"""
    def __init__(self):
        self.status = randint(0,1)
        self.number_of_neighbours = 0

    def change_status(self):
        global alive
        global dead
        alive = 1
        dead = 0
        if self.status == alive:
            if self.number_of_neighbours < 2 or self.number_of_neighbours > 3:
                self.status = dead
        else:
            if self.number_of_neighbours == 3:
                self.status = alive

class Population:
    """Class that takes care of grid, cells and rules of life and death"""
    def __init__(self):
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.scr_width, self.settings.scr_height))
        self.cell_size = self.settings.cell_size
        self.width = self.settings.scr_width
        self.height = self.settings.scr_height
        self.rows = int(self.height / self.cell_size)
        self.columns = int(self.width / self.cell_size)
        self.grid = [[Cell() for column in range(self.columns)] for row in range(self.rows)]
        self.not_ready = True

    def pre_populate_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                pos_x, pos_y = int(x/self.cell_size), int(y/self.cell_size)
                if self.grid[pos_y][pos_x].status == 1:
                    self.grid[pos_y][pos_x].status = 0
                else:
                    self.grid[pos_y][pos_x].status = 1

    def pre_game(self):
        while self.not_ready:
            self.pre_populate_events()
            for y in range(len(self.grid)):
                for x in range(len(self.grid[0])):
                    cell_rect = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                    if self.grid[y][x].status == 1:
                        pygame.draw.rect(self.screen, self.settings.alive_color, cell_rect)
                    else:
                        pygame.draw.rect(self.screen, self.settings.dead_color, cell_rect)
                    pygame.display.flip()

    def draw_grid(self, screen):
        #(left,top,width,height)
        alive = 1
        dead = 0
        
        dead_color = self.settings.dead_color
        alive_color = self.settings.alive_color
        
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
                #tutaj jest gdzieś bug
                elif 0 < y < len(self.grid) - 1 and 0 < x < len(self.grid[0]) - 1:
                    cell.number_of_neighbours = (
                            self.grid[y][x-1].status + self.grid[y][x+1].status + self.grid[y-1][x-1].status +
                            self.grid[y-1][x].status + self.grid[y-1][x+1].status + self.grid[y+1][x-1].status +
                            self.grid[y+1][x].status + self.grid[y+1][x+1].status
                    )
                    cell.change_status()

                cell_rect = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                if cell.status == 1:
                    pygame.draw.rect(screen, self.settings.alive_color, cell_rect)
                else:
                    pygame.draw.rect(screen, self.settings.dead_color, cell_rect)

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
        # population.pre_game()
        while True:
            self.check_events()
            # population.pre_game()
            next_gen = population.draw_grid(self.screen)
            population.grid = next_gen
            pygame.display.flip()

gol = GameOfLife()
gol.main()


