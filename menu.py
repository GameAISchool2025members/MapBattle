import pygame
import pygame_gui


class Menu:
    def __init__(self, manager, screen):
        if not pygame.font:
            print("Warning, fonts disabled")

        self.manager = manager  # Aji
        self.screen = screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((170, 238, 187))  # Green
        self.button_dim = pygame.Vector2(100, 50)

        self.show_menu()

    def create_buttons(self):
        play_button_pos = pygame.Vector2(
            self.background.get_width() / 2 - self.button_dim.x / 2,
            self.background.get_height() / 2 - self.button_dim.y / 2
        )

        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(play_button_pos, self.button_dim),
            text='Play',
            manager=self.manager
        )

        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (play_button_pos.x, play_button_pos.y + self.button_dim.y * 2),
                self.button_dim
            ),
            text='Quit',
            manager=self.manager
        )

    def show_menu(self):
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((170, 238, 187))  # Green
        self.button_dim = pygame.Vector2(100, 50)
        self.display_title_text()
        if not hasattr(self, 'play_button') or not self.play_button.alive():
            self.create_buttons()

    def hide_menu(self):
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((170, 238, 187))  # Green
        self.button_dim = pygame.Vector2(100, 50)
        if hasattr(self, 'play_button') and self.play_button.alive():
            self.play_button.kill()
        if hasattr(self, 'quit_button') and self.quit_button.alive():
            self.quit_button.kill()

    def display_menu(self):
        self.screen.blit(self.background, (0, 0))

    def display_title_text(self):
        if pygame.font:
            font = pygame.font.Font(None, 64)
            text = font.render("Map Battle", True, (0, 0, 0))  # Black
            text_pos = text.get_rect(centerx=self.background.get_width() / 2, y=10)
            self.background.blit(text, text_pos)


    def get_play_button(self):
        return self.play_button if hasattr(self, 'play_button') else None

    def get_quit_button(self):
        return self.quit_button if hasattr(self, 'quit_button') else None
