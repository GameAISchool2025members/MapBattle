import os
import pygame
import pygame_gui
from pygame_gui.elements import UIButton
from typing import Tuple
from data_structs import Map
from collections.abc import Callable

class VisualGrid:
    def __init__(self, manager, screen, init_data):
        if not pygame.font:
            print("Warning, fonts disabled")

        self.screen = screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((170, 238, 187)) # Green

        self.init_data = init_data
        self.map = Map(
            Width=self.init_data.BoardWidth,
            Height=self.init_data.BoardHeight,
            Cells = []
        )

        for h in range(self.map.Height):
            self.map.Cells.append([])

        button_width = (self.screen.get_width() // self.map.Width) - 5
        button_height = (self.screen.get_height() // self.map.Height) - 5
        self.button_dim = pygame.Vector2(button_width, button_height)
        self.width_gap = int(self.map.Width * 2.5)
        self.height_gap = int(self.map.Height * 2.5)

        for h in range(self.map.Height):
            height = self.height_gap + (h * self.button_dim.y)
            for w in range(self.map.Width):
                width = self.width_gap + (w * self.button_dim.x)

                self.map.Cells[h].append(pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((width, height), self.button_dim),
                    text='',
                    manager=manager))

    def display_map(self):
        self.screen.blit(self.background, (0, 0))

    def set_image(self, index: Tuple[int, int], image_path: str):
        button = self.map.Cells[index[1]][index[0]]
        button_image = pygame.image.load(image_path)
        self.background.convert_alpha()
        self.background.blit(button_image, button.relative_rect)
    
    def set_hover_image(self, index: Tuple[int, int], image_path: str):
        button = self.map.Cells[index[1]][index[0]]
        button_image = pygame.image.load(image_path)
        self.background.convert_alpha()
        self.background.blit(button_image, button.relative_rect)
    
    def set_selected_image(self, index: Tuple[int, int], image_path: str):
        button = self.map.Cells[index[1]][index[0]]
        button_image = pygame.image.load(image_path)
        self.background.convert_alpha()
        self.background.blit(button_image, button.relative_rect)
    
    def set_disable_image(self, index: Tuple[int, int], image_path: str):
        button = self.map.Cells[index[1]][index[0]]
        clear_surface = pygame.Surface(button.relative_rect)
        clear_surface = clear_surface.convert()
        clear_surface.fill((170, 238, 187)) # Green
        self.background.blit(clear_surface, button.relative_rect)

    def set_callback_function_pressed(self, index: Tuple[int, int], func: Callable):
        button = self.map.Cells[index[1]][index[0]]
        button.bind(pygame_gui.UI_BUTTON_PRESSED, func)
