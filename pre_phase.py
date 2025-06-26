import battle

import evolution
import game_init
import game_state_manager
def run(init_data: game_init.BattleState, run_counter: int):
    if run_counter:
        evolution.RunEvolution(init_data.UnitsAgentA,
                               init_data.UnitsAgentB,
                               31 + run_counter,
                               init_data.GameGrid,
                               69,
                               5,
                               0
                               )
    game_state_manager.set