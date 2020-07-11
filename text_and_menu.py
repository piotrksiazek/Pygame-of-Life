import pygame
import sys
import tkinter
from tkinter import filedialog
from PIL import Image, ImageEnhance
import numpy as np



class Interface:
    def __init__(self, gol, population):
        # Generation counter attributes
        self.counter_color = (219, 179, 123)
        self.counter_font = pygame.font.Font('assets/FFFFORWA.TTF', 20)
        self.counter_text = self.counter_font.render('0', True, self.counter_color)
        self.counter_rect = self.counter_text.get_rect()

        # Population counter attributes
        self.pop_counter_color = (219, 179, 123)
        self.pop_counter_font = pygame.font.Font('assets/FFFFORWA.TTF', 20)
        self.pop_counter_text = self.pop_counter_font.render('0', True, self.pop_counter_color)
        self.pop_counter_rect = self.pop_counter_text.get_rect()

        # Number of pauses counter attributes
        self.number_of_pauses_color = (219, 179, 123)
        self.number_of_pauses_font = pygame.font.Font('assets/FFFFORWA.TTF', 20)
        self.number_of_pauses_text = self.pop_counter_font.render(str(gol.number_of_pauses), True, self.pop_counter_color)
        self.number_of_pauses_rect = self.pop_counter_text.get_rect()

        # Interface board attributes
        self.interface_img = pygame.image.load('assets/projekt interfejsu.png')
        self.interface_rect = self.interface_img.get_rect()
        self.interface_img_y = 0
        self.interface_img_x = gol.settings.scr_height



    def draw_bg(self, gol):
        # pygame.draw.rect(gol.screen, self.interface_bg_color, self.interface_rect)
        gol.screen.blit(self.interface_img, (self.interface_img_x, self.interface_img_y))

    def draw_and_update_counter(self, population, gol, things_to_count):
        # self.counter_rect.centerx = self.interface_rect.centerx
        # self.counter_rect.y = 20
        self.counter_rect.centerx = gol.settings.scr_width - self.interface_rect.size[0] / 2
        self.counter_rect.y = 105
        self.counter_text = self.counter_font.render(f'{things_to_count}', True, self.counter_color)
        gol.screen.blit(self.counter_text, self.counter_rect)
        self.counter_rect = self.counter_text.get_rect()

    def draw_and_update_pop_counter(self, population, gol, things_to_count):
        self.pop_counter_rect.centerx = gol.settings.scr_width - self.interface_rect.size[0] / 2
        self.pop_counter_rect.y = 40
        self.pop_counter_text = self.pop_counter_font.render(f'{things_to_count}', True, self.counter_color)
        gol.screen.blit(self.pop_counter_text, self.pop_counter_rect)
        self.pop_counter_rect = self.pop_counter_text.get_rect()

    def display_number_of_pauses(self, gol, things_to_count):
        self.pop_counter_rect.centerx = gol.settings.scr_width - self.interface_rect.size[0] / 2
        self.pop_counter_rect.y = 200
        self.pop_counter_text = self.pop_counter_font.render(f'{things_to_count}', True, self.counter_color)
        gol.screen.blit(self.pop_counter_text, self.pop_counter_rect)




class Button:
    def __init__(self, left, top, width, height, text, color, text_color, color_clicked, gol):
        self.width = width
        self.button_left = gol.settings.scr_width / 2 - self.width / 2
        self.left = left
        self.height = height
        self.top = top
        self.bottom = self.top + self.height
        self.text = text
        self.color = color
        self.text_color = text_color
        self.color_clicked = color_clicked
        self.left_arrow = '<'
        self.right_arrow = '>'

    def is_over(self, how_far_from_right):
        # Getting mouse coordinates
        x, y = pygame.mouse.get_pos()
        if self.text == '<' or self.text == '>':
            if x >= how_far_from_right and x < how_far_from_right + self.width and y >= self.top and y <= self.top + self.height:
                return True
        else:
            if x >= self.button_left and x <= self.button_left + self.width and y >= self.top and y <= self.top + self.height:
                return True

    def draw_button(self, gol):
        font = pygame.font.Font('assets/FFFFORWA.TTF', 16)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect()
        text_rect.center = (gol.settings.scr_width/2, self.top + self.height/2)
        # pygame.draw.rect(gol.screen, self.color, (gol.settings.scr_width/2-self.width/2, self.top, self.width, self.height), 0)
        pygame.draw.rect(gol.screen, self.color, (self.button_left, self.top, self.width, self.height), 0)
        gol.screen.blit(text, text_rect)

    def draw_arrow(self, gol, how_far_from_right):
        font = pygame.font.Font('assets/FFFFORWA.TTF', 16)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect()
        text_rect.center = (how_far_from_right + self.width/2, self.top + self.height/2)
        if self.text == '<':
            # pygame.draw.rect(gol.screen, self.color, (how_far_from_right, self.top, self.width, self.height), 0)
            pygame.draw.rect(gol.screen, self.color, (how_far_from_right, self.top, self.width, self.height), 0)
            gol.screen.blit(text, text_rect)
        elif self.text == '>':
            pygame.draw.rect(gol.screen, self.color, (how_far_from_right, self.top, self.width, self.height), 0)
            gol.screen.blit(text, text_rect)
            

class MainMenu:
    """Class MainMenu stores attributes of all buttons and arrows, draws menu and checks events that may happen while in menu"""
    def __init__(self, gol):
        self.screen = gol.screen
        self.menu_color = (0, 0, 0)
        self.in_menu = True

        self.mode_button = Button(left=150, top=150, width=200, height=50, text=gol.mode, color=(255,0,0), text_color=(0,0,0), color_clicked=(0,255,0), gol=gol)
        self.mode_l_arrow = Button(left=150, top=150, width=50, height=50, text='<', color=(255,0,0), text_color=(0,0,0), color_clicked=(0,255,0), gol=gol)
        self.mode_r_arrow = Button(left=150, top=150, width=50, height=50, text='>', color=(255,0,0), text_color=(0,0,0), color_clicked=(0,255,0), gol=gol)

        self.color_button = Button(left=150, top=300, width=200, height=50, text='color', color=(255,0,0), text_color=(0,0,0), color_clicked=(0,255,0), gol=gol)
        self.color_l_arrow = Button(left=150, top=300, width=50, height=50, text='<', color=(255,0,0), text_color=(0,0,0), color_clicked=(0,255,0), gol=gol)
        self.color_r_arrow = Button(left=150, top=300, width=50, height=50, text='>', color=(255,0,0), text_color=(0,0,0), color_clicked=(0,255,0), gol=gol)

        self.size_button = Button(left=150, top=450, width=200, height=50, text='size', color=(255,0,0), text_color=(0,0,0), color_clicked=(0,255,0), gol=gol)
        self.size_l_arrow = Button(left=150, top=450, width=50, height=50, text='<', color=(255,0,0), text_color=(0,0,0), color_clicked=(0,255,0), gol=gol)
        self.size_r_arrow = Button(left=150, top=450, width=50, height=50, text='>', color=(255,0,0), text_color=(0,0,0), color_clicked=(0,255,0), gol=gol)
        
        self.seed_from_image = Button(left=150, top=600, width=200, height=50, text='seed from image', color=(255,0,0), text_color=(0,0,0), color_clicked=(0,255,0), gol=gol)

    # functions related to 
    def get_str_of_img_path(self):
        root = tkinter.Tk()
        # Hide tkinter window from sight
        root.withdraw()
        file_path = filedialog.askopenfilename()
        # We don't need tkinter app instance anymore
        root.destroy()
        return file_path

    def b_and_w_resized(self):
        img = Image.open(self.get_str_of_img_path()).convert('L')
        enhancer = ImageEnhance.Contrast(img)
        b_and_w = enhancer.enhance(100)
        resized_im = b_and_w.resize((700, 700))
        return resized_im


    def create_ascii_art(self, b_and_w_resized, gol):
        gol.grid_from_image = True
        ascii_chars = [' ', 'o']
        im = np.array(b_and_w_resized).reshape(700, 700)
        lista = []
        for i in range(0, 700, 5):
            for j in range(0, 700, 5):
                lista.append(np.mean(im[j:j + 5, i:i + 5], dtype=int))
        ascii_art = [ascii_chars[pixel // 128] for pixel in lista]
        im = np.array(ascii_art).reshape(140, 140)
        with open('obrazek.txt', 'w') as file:
            for i in im:
                file.write(''.join(char for char in i))
                file.write('\n')

    def check_menu_events(self, gol):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.in_menu = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Don't want to exceed max index.
                if self.mode_r_arrow.is_over(650) and self.mode_button.text != gol.mode_list[-1]:
                    self.mode_button.text = gol.mode_list[gol.mode_list.index(self.mode_button.text)+1]
                    gol.mode = self.mode_button.text
                # Don't want to go below 0 index.
                elif self.mode_l_arrow.is_over(300) and self.mode_button.text != gol.mode_list[0]:
                    self.mode_button.text = gol.mode_list[gol.mode_list.index(self.mode_button.text)-1]
                    gol.mode = self.mode_button.text

                elif self.size_r_arrow.is_over(650) and self.size_button.text != gol.settings.menu_cell_size_list[-1]:
                    self.size_button.text = str(gol.settings.menu_cell_size_list[gol.settings.menu_cell_size_list.index(self.size_button.text)+1])
                    # Don't want to cast types if self.size_button.text is literally text.
                    if self.size_button.text != 'size':
                        gol.settings.cell_size = int(self.size_button.text)
                elif self.size_l_arrow.is_over(300) and self.size_button.text != gol.settings.menu_cell_size_list[0]:
                    self.size_button.text = str(gol.settings.menu_cell_size_list[gol.settings.menu_cell_size_list.index(self.size_button.text)-1])
                    if self.size_button.text != 'size':
                        gol.settings.cell_size = int(self.size_button.text)
                elif self.seed_from_image.is_over(650):
                    self.create_ascii_art(self.b_and_w_resized(), gol)


    def draw_menu(self, gol):
        while self.in_menu:
            self.check_menu_events(gol)
            self.screen.fill(self.menu_color)

            self.mode_button.draw_button(gol)
            self.mode_l_arrow.draw_arrow(gol, 300)
            self.mode_r_arrow.draw_arrow(gol, 650)

            self.color_button.draw_button(gol)
            self.color_l_arrow.draw_arrow(gol, 300)
            self.color_r_arrow.draw_arrow(gol, 650)
            
            self.size_button.draw_button(gol)
            self.size_l_arrow.draw_arrow(gol, 300)
            self.size_r_arrow.draw_arrow(gol, 650)
            
            self.seed_from_image.draw_button(gol)


            pygame.display.flip()

        # self.randomize_button = Button()
        # self.colors_button = Button()
# class MainMenu:
#     """Takes care of color menu and user settings"""
#     def __init__(self, gol):
#         self.color_ready = False
#         self.color_menu_img = pygame.image.load('assets/color_menu_2.png')
#         self.color_menu_img_scaled = pygame.transform.scale(self.color_menu_img, (gol.settings.scr_height, gol.settings.scr_width))
#
    # def check_color_events(self, gol):
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             sys.exit()
    #         elif event.type == pygame.KEYDOWN:
    #             # We don't want to exceed max index of color array. gol.settings.max_color_of_life is the last index.
    #             if event.key == pygame.K_RIGHT and gol.settings.colors_of_life.index(gol.settings.alive_color) < gol.settings.max_color_of_life:
    #                 gol.settings.alive_color = gol.settings.colors_of_life[gol.settings.colors_of_life.index(gol.settings.alive_color)+1]
    #             elif event.key == pygame.K_LEFT and gol.settings.colors_of_life.index(gol.settings.alive_color) > 0:
    #                 gol.settings.alive_color = gol.settings.colors_of_life[gol.settings.colors_of_life.index(gol.settings.alive_color)-1]
    #
    #             # The same thing but for colors of death.
    #             elif event.key == pygame.K_UP and gol.settings.colors_of_death.index(gol.settings.dead_color) < gol.settings.max_color_of_death:
    #                 gol.settings.dead_color = gol.settings.colors_of_death[gol.settings.colors_of_death.index(gol.settings.dead_color)+1]
    #             elif event.key == pygame.K_DOWN and gol.settings.colors_of_death.index(gol.settings.dead_color) > 0:
    #                 gol.settings.dead_color = gol.settings.colors_of_death[gol.settings.colors_of_death.index(gol.settings.dead_color)-1]
    #
    #             # Pressing space breakes the choose_color loop.
    #             elif event.key == pygame.K_SPACE:
    #                 self.color_ready = True
    #
    # def choose_color(self, gol):
    #     while not self.color_ready:
    #         self.check_color_events(gol)
    #         gol.screen.fill(gol.settings.alive_color)
    #
    #         # death_rect is drawn right behind transparent japaneese death symbol so we see only colorful sign.
    #         death_rect = pygame.Rect(
    #             gol.settings.scr_width - 0.20*gol.settings.scr_width, gol.settings.scr_height * 0.3,
    #             0.3*gol.settings.scr_width, 0.3*gol.settings.scr_width
    #         )
    #         pygame.draw.rect(gol.screen, gol.settings.dead_color, death_rect)
    #         gol.screen.blit(self.color_menu_img_scaled, (0,0))
    #         pygame.display.flip()