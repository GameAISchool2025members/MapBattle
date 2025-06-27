
import evolution
import game_init
import game_state_manager


def run(self, gameStateManager: game_state_manager, init_data: game_init.BattleState, run_counter: int):
    if run_counter:
        evolution.RunEvolution(init_data.UnitsAgentA,
                                init_data.UnitsAgentB,
                                31 + run_counter,
                                init_data.GameGrid,
                                30,
                                20,
                                0
                                )
    gameStateManager.set_state(game_state_manager.GameState.BATTLE_PHASE)
