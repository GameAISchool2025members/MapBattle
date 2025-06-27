
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
        
    usedResources = [0]

    def handle_press(x, y, init_data, usedResources):
        usedResources[0] = usedResources[0] + 1
        if init_data.GameGrid.Cells[y][x] == 0:
            init_data.GameGrid.Cells[y][x] = 1
        else:
            init_data.GameGrid.Cells[y][x] = 0

    all_functions = []

    for x in range(0, Visual.map.Width):
        for y in range(2, Visual.map.Height - 0):
            
            Visual.set_callback_function_pressed([x, y], 
            lambda button: handle_press(x, y, init_data, usedResources))


    while usedResources[0] != MaxResources:
        yield False

    for x in range(0, Visual.map.Width):
        for y in range(2, Visual.map.Height - 0):
            Visual.set_callback_function_pressed([x, y], None)

    gameStateManager.set_state(game_state_manager.GameState.BATTLE_PHASE)
    yield True
