import pygame
import pygame_gui

class Menu:
    def __init__(self, manager, screen):
        if not pygame.font:
            print("Warning, fonts disabled")

        self.screen = screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((170, 238, 187)) # Green
        self.button_dim = pygame.Vector2(100, 50)
        play_button_pos = pygame.Vector2(self.background.get_width()/2 - self.button_dim.x/2, self.background.get_height()/2 - self.button_dim.y/2)
        self.play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(play_button_pos, self.button_dim),
                                                    text='Play',
                                                    manager=manager)
        self.quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((play_button_pos.x, play_button_pos.y + self.button_dim.y * 2), self.button_dim),
                                                    text='Quit',
                                                    manager=manager)

    def display_menu(self):
        self.display_title_text()
        self.screen.blit(self.background, (0, 0))

    def display_title_text(self):
        if pygame.font:
            font = pygame.font.Font(None, 64)
            text = font.render("Map Battle", True, (0, 0, 0)) # Black
            text_pos = text.get_rect(centerx=self.background.get_width()/2, y=10)
            self.background.blit(text, text_pos)

    def get_play_button(self):
        return self.play_button

    def get_quit_button(self):
        return self.quit_button
