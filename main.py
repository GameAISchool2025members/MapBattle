import pygame
import pygame_gui
import game_state_manager
import menu
import game_init
import pre_phase
import battle_phase
import end_phase

# pygame setup
pygame.init()
pygame.display.set_caption("Map Battle")
resolution = (1280, 720)
screen = pygame.display.set_mode(resolution, pygame.SCALED)
clock = pygame.time.Clock()
running = True
dt = 0

gameStateManager = game_state_manager.GameStateManager()
uiManager = pygame_gui.UIManager(resolution)
menu = menu.Menu(screen)

init_data = game_init.setup_battle(8, 12, 3)
run_counter: int = 0

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

        uiManager.process_events(event)

    match gameStateManager.get_state():
        case game_state_manager.GameState.MENU:
            menu.display_menu()
        case game_state_manager.GameState.PRE_PHASE:
            pre_phase.run(init_data, run_counter)
        case game_state_manager.GameState.BATTLE_PHASE:
            battle_phase.run()
        case game_state_manager.GameState.END_PHASE:
            end_phase.run()
        case game_state_manager.GameState.QUIT:
            running = False

    uiManager.update(dt)
    uiManager.draw_ui(screen)
    pygame.display.update()

pygame.quit()