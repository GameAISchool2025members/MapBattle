import pygame

class Menu:
    def __init__(self):
        if not pygame.font:
            print("Warning, fonts disabled")

        self.screen = pygame.display.set_mode((1280, 720), pygame.SCALED)
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((170, 238, 187))

    def display_menu(self, dt):
        # fill the screen with a color to wipe away anything from last frame
        self.display_title_text()
        self.screen.blit(self.background, (0, 0))

        # flip() the display to put your work on screen
        pygame.display.flip()

    def display_title_text(self):
        if pygame.font:
            font = pygame.font.Font(None, 64)
            text = font.render("Map Battle", True, (0, 0, 0))
            text_pos = text.get_rect(centerx=self.background.get_width()/2, y=10)
            self.background.blit(text, text_pos)
