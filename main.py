import pygame

import battle_phase
import end_phase
import menu
import game_state_manager
import game_init
import pre_phase

# pygame setup
pygame.init()
pygame.display.set_caption("Map Battle")
clock = pygame.time.Clock()
running = True
dt = 0

gameStateManager = game_state_manager.GameStateManager()
menu = menu.Menu()
menu.__init__()

init_data = game_init.setup_battle(8, 12, 3)

first_run = True



while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    match gameStateManager.get_state():
        case game_state_manager.GameState.MENU:
            menu.display_menu(dt)
        case game_state_manager.GameState.PRE_PHASE:
            pre_phase.run(init_data, first_run)
        case game_state_manager.GameState.BATTLE_PHASE:
            battle_phase.run()
        case game_state_manager.GameState.END_PHASE:
            end_phase.run()
        case game_state_manager.GameState.QUIT:
            running = False

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()