import pygame
import pygame_gui
import evolution
import game_init
import game_state_manager

class PrePhase:
    def __init__(self, manager, screen):
        if not pygame.font:
            print("Warning, fonts disabled")

        self.screen = screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((170, 238, 187)) # Green

    def display_map(self):
        self.screen.blit(self.background, (0, 0))

    def run(self, gameStateManager: game_state_manager, init_data: game_init.BattleState, run_counter: int):
        if run_counter:
            evolution.RunEvolution(init_data.UnitsAgentA,
                                   init_data.UnitsAgentB,
                                   31 + run_counter,
                                   init_data.GameGrid,
                                   69,
                                   5,
                                   0
                                   )
        gameStateManager.set_state(game_state_manager.GameState.BATTLE_PHASE)