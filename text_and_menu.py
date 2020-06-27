import pygame
import sys

# class Text:
#     def __init__(self, gol):
#         self.font = pygame.font.Font('assets/FFFFORWA.TTF', 32)
#         self.text = self.font.render('Pygame of Life', True, (255,0,0))
#         self.rect = self.text.get_rect()
#         self.rect.center = (gol.settings.scr_width // 2, gol.settings.scr_height // 2)

class Button:
    def __init__(self, top, bottom, width, height, text, color, color_clicked):
        self.top = top
        self.bottom = bottom
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.color_clicked = color_clicked

    def draw_button(self):
        pass

class MainMenu:
    """Takes care of color menu and user settings"""
    def __init__(self, gol):
        self.color_ready = False
        self.color_menu_img = pygame.image.load('assets/color_menu_2.png')
        self.color_menu_img_scaled = pygame.transform.scale(self.color_menu_img, (gol.settings.scr_height, gol.settings.scr_width))

    def check_color_events(self, gol):
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

    def choose_color(self, gol):
        while not self.color_ready:
            self.check_color_events(gol)
            gol.screen.fill(gol.settings.alive_color)

            # death_rect is drawn right behind transparent japaneese death symbol so we see only colorful sign.
            death_rect = pygame.Rect(
                gol.settings.scr_width - 0.20*gol.settings.scr_width, gol.settings.scr_height * 0.3,
                0.3*gol.settings.scr_width, 0.3*gol.settings.scr_width
            )
            pygame.draw.rect(gol.screen, gol.settings.dead_color, death_rect)
            gol.screen.blit(self.color_menu_img_scaled, (0,0))
            pygame.display.flip()