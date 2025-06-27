import game_state_manager
from battle_session import BattleStats


def run(gameStateManager: game_state_manager, battle_session: BattleStats):
    print()
    print("End Phase")
    print(battle_session.get_summary())

    if battle_session.total_battles >= 4:
        print("Game end!")
        gameStateManager.set_state(game_state_manager.GameState.MENU)
    else:
        print("Next Battle...")
        gameStateManager.set_state(game_state_manager.GameState.PRE_PHASE)