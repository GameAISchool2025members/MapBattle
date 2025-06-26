import battle
import game_state_manager
import game_init


def run(gameStateManager: game_state_manager, init_data: game_init.BattleState):
    battle_result = battle.Battle(init_data.UnitsAgentA,
                                  init_data.UnitsAgentB,
                                  init_data.GameGrid)
    gameStateManager.set_state(game_state_manager.GameState.END_PHASE)
