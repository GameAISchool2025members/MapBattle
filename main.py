import pygame
import pygame_gui

import battle
import game_state_manager
import menu
import game_init
import pre_phase
import battle_phase
import end_phase
from battle_session import BattleStats

# pygame setup
pygame.init()
pygame.display.set_caption("Map Battle")
resolution = (480, 720)
screen = pygame.display.set_mode(resolution, pygame.SCALED)
clock = pygame.time.Clock()
running = True
dt = 0
timeBetweenMoves = 0.5

battleSession = BattleStats()
init_data = game_init.setup_battle(8, 12, 3)
run_counter: int = 0

gameStateManager = game_state_manager.GameStateManager()
uiManager = pygame_gui.UIManager(resolution)
menu = menu.Menu(uiManager, screen)
pre_phase = pre_phase.PrePhase(uiManager, screen, init_data)

while running:
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == menu.get_play_button():
                menu.hide_menu()
                gameStateManager.set_state(game_state_manager.GameState.PRE_PHASE)
            elif event.ui_element == menu.get_quit_button():
                gameStateManager.set_state(game_state_manager.GameState.QUIT)

        uiManager.process_events(event)

    match gameStateManager.get_state():
        case game_state_manager.GameState.MENU:
            menu.show_menu()
            menu.display_menu()
        case game_state_manager.GameState.PRE_PHASE:
            pre_phase.display_map()
            pre_phase.run(gameStateManager, init_data, run_counter)
        case game_state_manager.GameState.BATTLE_PHASE:
            if gameStateManager.GetBattleGenerator() == None:
                timeSinceLastMove = 0
                gameStateManager.SetBattleGenerator(battle_phase.run(
                    gameStateManager,
                    init_data,
                    battleSession
                ))
            if timeSinceLastMove >= timeBetweenMoves:
                result = next(gameStateManager.GetBattleGenerator())
                if result[0] == True:
                    gameStateManager.SetBattleGenerator(None)
                # HANDLE UPDATE FOR RENDERING HERE!!!!!
                print("Action Taken")

                timeSinceLastMove = 0
            else:
                timeSinceLastMove += dt
        case game_state_manager.GameState.END_PHASE:
            end_phase.run(gameStateManager, battleSession)
        case game_state_manager.GameState.QUIT:
            running = False

    uiManager.update(dt)
    uiManager.draw_ui(screen)
    pygame.display.update()

pygame.quit()