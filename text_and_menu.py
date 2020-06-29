import pygame
import sys


class Interface:
    def __init__(self, gol, population):
        # Generation counter attributes
        self.counter_color = (255, 0, 0)
        self.counter_font = pygame.font.Font('assets/FFFFORWA.TTF', 32)
        self.counter_text = self.counter_font.render('0', True, self.counter_color)
        self.counter_rect = self.counter_text.get_rect()

        # Interface board attributes
        self.interface_bg_color = (50, 0, 0)
        self.interface_rect = pygame.Rect(gol.settings.scr_height, 0, gol.settings.scr_width-gol.settings.scr_height, gol.settings.scr_height)


    def draw_bg(self, gol):
        pygame.draw.rect(gol.screen, self.interface_bg_color, self.interface_rect)

    def draw_and_update_counter(self, population, gol):
        self.counter_rect.center = (150, 150)
        gol.screen.blit(self.counter_text, self.counter_rect)
        self.counter_text = self.counter_font.render(f'{population.number_of_generations}', True, self.counter_color)
        self.counter_rect = self.counter_text.get_rect()

class Button:
    def __init__(self, left, top, width, height, text, color, text_color, color_clicked, gol):
        self.left = left
        self.top = top
        self.width = width
        self.right = gol.settings.scr_width / 2 + self.width / 2
        self.height = height
        self.text = text
        self.color = color
        self.text_color = text_color
        self.color_clicked = color_clicked
        self.space_between_button_and_arrow = 10
        self.left_arrow = '<'
        self.right_arrow = '>'

    def button_events(self):
        pass

    def arrow_events(self):
        pass

    def draw_button(self, gol):
        font = pygame.font.Font('assets/FFFFORWA.TTF', 16)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect()
        text_rect.center = (gol.settings.scr_width/2, self.top + self.height/2)
        pygame.draw.rect(gol.screen, self.color, (gol.settings.scr_width/2-self.width/2, self.top, self.width, self.height), 0)
        gol.screen.blit(text, text_rect)
    
    def draw_arrow(self, gol, how_far_from_right):
        font = pygame.font.Font('assets/FFFFORWA.TTF', 16)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect()
        text_rect.center = (how_far_from_right + self.width/2, self.top + self.height/2)
        if self.text == '<':
            pygame.draw.rect(gol.screen, self.color, (how_far_from_right, self.top, self.width, self.height), 0)
            gol.screen.blit(text, text_rect)
        elif self.text == '>':
            pygame.draw.rect(gol.screen, self.color, (how_far_from_right, self.top, self.width, self.height), 0)
            gol.screen.blit(text, text_rect)
            

class MainMenu:
    def __init__(self, gol):
        self.screen = gol.screen
        self.menu_color = (0,0,0)
        self.in_menu = True

        self.mode_button = Button(left=150, top=150, width=200, height=50, text='pies', color=(255,0,0), text_color=(0,0,0), color_clicked=(0,255,0), gol=gol)
        self.mode_l_arrow = Button(left=150, top=150, width=50, height=50, text='<', color=(255,0,0), text_color=(0,0,0), color_clicked=(0,255,0), gol=gol)
        self.mode_r_arrow = Button(left=150, top=150, width=50, height=50, text='>', color=(255,0,0), text_color=(0,0,0), color_clicked=(0,255,0), gol=gol)

        self.color_button = Button(left=150, top=300, width=200, height=50, text='color', color=(255,0,0), text_color=(0,0,0), color_clicked=(0,255,0), gol=gol)
        self.color_l_arrow = Button(left=150, top=300, width=50, height=50, text='<', color=(255,0,0), text_color=(0,0,0), color_clicked=(0,255,0), gol=gol)
        self.color_r_arrow = Button(left=150, top=300, width=50, height=50, text='>', color=(255,0,0), text_color=(0,0,0), color_clicked=(0,255,0), gol=gol)
        

    def check_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.in_menu = False

    def draw_menu(self, gol):
        while self.in_menu:
            self.check_menu_events()
            self.screen.fill(self.menu_color)

            self.mode_button.draw_button(gol)
            self.mode_l_arrow.draw_arrow(gol, 300)
            self.mode_r_arrow.draw_arrow(gol, 650)
            
            self.color_button.draw_button(gol)
            self.color_l_arrow.draw_arrow(gol, 300)
            self.color_r_arrow.draw_arrow(gol, 650)



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