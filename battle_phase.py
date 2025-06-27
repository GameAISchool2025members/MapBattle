import battle
import game_state_manager
import game_init
from battle_session import BattleStats
from data_structs import ResultOfBattle, Owner


def run(gameStateManager: game_state_manager, init_data: game_init.BattleState, battle_session: BattleStats):
    battle_result = battle.Battle(init_data.UnitsAgentA,
                                  init_data.UnitsAgentB,
                                  init_data.GameGrid)
    print("Battle Result:")
    print(battle_result.Winner)
    print()
    print("battle session summary:")
    battle_session.add_battle_result(battle_result)
    print(battle_session.get_summary())
    print()
    gameStateManager.set_state(game_state_manager.GameState.END_PHASE)
