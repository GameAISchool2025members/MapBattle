import pygame
import pygame_gui

class Menu:
    def __init__(self, screen):
        if not pygame.font:
            print("Warning, fonts disabled")

        self.screen = screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((170, 238, 187)) # Green

    def display_menu(self):
        self.display_title_text()
        self.screen.blit(self.background, (0, 0))

    def display_title_text(self):
        if pygame.font:
            font = pygame.font.Font(None, 64)
            text = font.render("Map Battle", True, (0, 0, 0)) # Black
            text_pos = text.get_rect(centerx=self.background.get_width()/2, y=10)
            self.background.blit(text, text_pos)
