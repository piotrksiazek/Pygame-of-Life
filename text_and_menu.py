import pygame
import sys
import tkinter
from tkinter import filedialog
from PIL import Image, ImageEnhance, UnidentifiedImageError
import numpy as np



class Interface:
    def __init__(self, gol, population):
        # General counter attributes
        self.counter_color = (219, 179, 123)
        self.counter_font = pygame.font.Font('assets/FFFFORWA.TTF', 20)
        self.counter_text = self.counter_font.render('0', True, self.counter_color)
        self.counter_rect = self.counter_text.get_rect()

        # Generation counter specific
        self.generation_counter_y = 105

        # Population counter specific
        self.population_counter_y = 40

        # Pause counter specific
        self.pause_counter_y = 200

        # Interface board attributes
        self.interface_img = pygame.image.load('assets/interface_bg.png')
        self.interface_rect = self.interface_img.get_rect()
        self.vertical_center = gol.settings.scr_width - self.interface_rect.size[0] / 2
        self.interface_img_y = 0
        self.interface_img_x = gol.settings.scr_height

    def draw_bg(self, gol):
        # pygame.draw.rect(gol.screen, self.interface_bg_color, self.interface_rect)
        gol.screen.blit(self.interface_img, (self.interface_img_x, self.interface_img_y))

    def draw_and_update_counter(self, gol, things_to_count, center_x, y):
        self.counter_rect.centerx = center_x
        self.counter_rect.y = y
        self.counter_text = self.counter_font.render(f'{things_to_count}', True, self.counter_color)
        gol.screen.blit(self.counter_text, self.counter_rect)

    def draw_and_update_counters(self, interface, population, gol):
        # Generation counter
        interface.draw_and_update_counter(gol, population.number_of_generations, interface.vertical_center, interface.generation_counter_y)
        # Population counter
        interface.draw_and_update_counter(gol, population.count_living_cells(), interface.vertical_center, interface.population_counter_y)






class Button:
    def __init__(self, left, top, width, height, text, color, text_color, color_clicked, is_arrow):
        self.width = width
        self.left = left
        self.height = height
        self.top = top
        self.bottom = self.top + self.height
        self.text = text
        self.color = color
        self.text_color = text_color
        self.color_clicked = color_clicked
        self.is_arrow = is_arrow

    def is_over(self):
        # x and y are mouse coordinates
        x, y = pygame.mouse.get_pos()
        if x >= self.left and x < self.left + self.width and y >= self.top and y <= self.top + self.height:
            return True


    def draw_button(self, gol, interface, font_size, color, color_when_over):
        font = pygame.font.Font('assets/FFFFORWA.TTF', font_size)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect()

        # arrow and regular buttons have different centering
        if self.is_arrow:
            text_rect.center = (self.left + self.width / 2, self.top + self.height / 2)
        else:
            text_rect.center = (interface.vertical_center, self.top + self.height/2)
        pygame.draw.rect(gol.screen, self.color, (self.left, self.top, self.width, self.height), 5)

        if self.is_over():
            self.color = color
        else:
            self.color = color_when_over
        gol.screen.blit(text, text_rect)


            

class MainMenu:
    """Class MainMenu stores attributes of all buttons and arrows, draws menu and checks events that may happen while in menu"""
    def __init__(self, gol, interface):
        self.screen = gol.screen

        self.color_button = Button(left=interface.vertical_center-75, top=180, width=150, height=50, text='color', color=(219, 179, 123), text_color=(0,0,0), color_clicked=(0,0,0 ), is_arrow=False)
        self.color_l_arrow = Button(left=interface.vertical_center-125, top=180, width=50, height=50, text='<', color=(219, 179, 123), text_color=(0,0,0), color_clicked=(0,0,0 ), is_arrow=True)
        self.color_r_arrow = Button(left=interface.vertical_center+75, top=180, width=50, height=50, text='>', color=(219, 179, 123), text_color=(0,0,0), color_clicked=(0,0,0 ), is_arrow=True)


        self.reset_button = Button(left=interface.vertical_center-75, top=260, width=150, height=50, text='reset', color=(219, 179, 123), text_color=(0,0,0), color_clicked=(0,0,0 ), is_arrow=False)

        self.randomize_button = Button(left=interface.vertical_center-75, top=340, width=150, height=50, text='randomize', color=(219, 179, 123), text_color=(0,0,0), color_clicked=(0,255,0), is_arrow=False)

        self.pause_button = Button(left=interface.vertical_center-75, top=420, width=150, height=50, text='pause', color=(219, 179, 123), text_color=(0,0,0), color_clicked=(0,255,0), is_arrow=False)
        
        self.size_button = Button(left=interface.vertical_center-75, top=500, width=150, height=50, text='size', color=(219, 179, 123), text_color=(0,0,0), color_clicked=(0,255,0), is_arrow=False)
        self.size_l_arrow = Button(left=interface.vertical_center-125, top=500, width=50, height=50, text='<', color=(219, 179, 123), text_color=(0,0,0), color_clicked=(0,255,0), is_arrow=True)
        self.size_r_arrow = Button(left=interface.vertical_center+75, top=500, width=50, height=50, text='>', color=(219, 179, 123), text_color=(0,0,0), color_clicked=(0,255,0), is_arrow=True)

        self.seed_from_image = Button(left=interface.vertical_center-75, top=580, width=150, height=50, text='from image', color=(219, 179, 123), text_color=(0,0,0), color_clicked=(0,255,0), is_arrow=False)

        self.hoffmans_dream_button = Button(left=interface.vertical_center-75, top=650, width=150, height=30, text="hoffman's dream", color=(219, 179, 123), text_color=(0,0,0), color_clicked=(0,255,0), is_arrow=False)

        self.image_path = ""

        self.image_open_success = False
        self.is_error = False
        self.error_message = ""
    # functions related to 
    def get_str_of_img_path(self):
        root = tkinter.Tk()
        # Hide tkinter window from sight
        root.withdraw()
        file_path = filedialog.askopenfilename()
        # We don't need tkinter app instance anymore
        root.destroy()
        self.image_path = file_path
        return file_path

    def display_error(self, font_size, error_message, text_color, gol, interface):
        font = pygame.font.Font('assets/FFFFORWA.TTF', font_size)
        text = font.render(error_message, True, text_color)
        text_rect = text.get_rect()
        text_rect.center = (interface.vertical_center, 165)
        gol.screen.blit(text, text_rect)

    def b_and_w_resized(self, gol, image_path, interface):
        gol.grid_from_image = True
        try:
            img = Image.open(image_path).convert('L')
            enhancer = ImageEnhance.Contrast(img)
            b_and_w = enhancer.enhance(100)
            resized_im = b_and_w.resize((700, 700))
            gol.grid_image = resized_im.transpose(Image.ROTATE_90)
            self.image_open_success = True
            return resized_im.transpose(Image.ROTATE_90)

        except AttributeError:
            self.error_message = "You need to choose a file"
            self.is_error = True
            self.image_open_success = False
        except UnidentifiedImageError:
            self.error_message = "This is not an image"
            self.is_error = True
            self.image_open_success = False



    def create_ascii_art(self, b_and_w_resized, gol):
        try:
            ascii_chars = [' ', 'o']
            im = np.array(b_and_w_resized).reshape(700, 700)
            lista = []
            for i in range(0, 700, gol.settings.cell_size):
                for j in range(0, 700, gol.settings.cell_size):
                    lista.append(np.mean(im[j:j + gol.settings.cell_size, i:i + gol.settings.cell_size], dtype=int))
            ascii_art = [ascii_chars[pixel // 128] for pixel in lista]
            im = np.array(ascii_art).reshape(int(700/gol.settings.cell_size), int(700/gol.settings.cell_size))
            with open('ascii_art.txt', 'w') as file:
                for i in im:
                    file.write(''.join(char for char in i))
                    file.write('\n')
        except ValueError:
            self.image_open_success = False

    def check_menu_events_(self, gol, interface):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                        sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.seed_from_image.is_over():
                    self.create_ascii_art(self.b_and_w_resized(gol, self.get_str_of_img_path()), gol, interface)
            elif event.type == pygame.KEYDOWN:
                # Press space to start the game
                if event.key == pygame.K_SPACE:
                    gol.paused = False


    def draw_menu_(self, gol, interface):
        if self.is_error:
            self.display_error(12, self.error_message, (0,0,0), gol, interface)

        self.color_button.draw_button(gol, interface, 16, (219, 179, 123), (219, 179, 123))
        self.color_l_arrow.draw_button(gol, interface, 16, (0,0,0), (219, 179, 123))
        self.color_r_arrow.draw_button(gol, interface, 16, (0,0,0), (219, 179, 123))

        self.reset_button.draw_button(gol, interface, 16, (0,0,0), (219, 179, 123))
        
        self.randomize_button.draw_button(gol, interface, 16, (0,0,0), (219, 179, 123))

        self.pause_button.draw_button(gol, interface, 16, (0,0,0), (219, 179, 123))
        
        self.size_button.draw_button(gol, interface, 16, (219, 179, 123), (219, 179, 123))
        self.size_l_arrow.draw_button(gol, interface, 16, (0,0,0), (219, 179, 123))
        self.size_r_arrow.draw_button(gol, interface, 16, (0,0,0), (219, 179, 123))

        self.seed_from_image.draw_button(gol, interface, 16, (0,0,0), (219, 179, 123))
        
        self.hoffmans_dream_button.draw_button(gol, interface, 12, (0,0,0), (219, 179, 123))