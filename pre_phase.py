
import evolution
import game_init
import game_state_manager
import VisualGrid
from pygame_gui.elements import UIButton
import functools



def run(gameStateManager: game_state_manager, init_data: game_init.BattleState, run_counter: int, Visual: VisualGrid.VisualGrid, MaxResources: int):
    if run_counter:
        yield evolution.RunEvolution(init_data.UnitsAgentA,
                                init_data.UnitsAgentB,
                                31 + run_counter,
                                init_data.GameGrid,
                                5,
                                20,
                                0
                                )
        

    def handle_press(x, y):
        init_data.UsedResources = game_init.Resources(init_data.UsedResources.UsedResources + 1) # Safely modifies the shared counter
        if init_data.GameGrid.Cells[y][x] == 0:
            init_data.GameGrid.Cells[y][x] = 1
        else:
            init_data.GameGrid.Cells[y][x] = 0
        print(f"Clicked: ({x}, {y}) — usedResources = {init_data.UsedResources.UsedResources}")  # Debug

    def make_callback(x, y):
        # Each lambda captures its own x and y values
        return lambda button: handle_press(x, y)

    # Register buttons
    for x in range(0, Visual.map.Width):
        for y in range(2, Visual.map.Height - 2):
            Visual.set_callback_function_pressed([x, y], make_callback(x, y))

    # Wait for enough resources to be used
    while init_data.UsedResources.UsedResources != MaxResources:
        yield False

    for x in range(0, Visual.map.Width):
        for y in range(2, Visual.map.Height - 0):
            Visual.set_callback_function_pressed([x, y], None)

    gameStateManager.set_state(game_state_manager.GameState.BATTLE_PHASE)
    yield None
