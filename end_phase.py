import game_state_manager


def run(gameStateManager: game_state_manager):
    gameStateManager.set_state(game_state_manager.GameState.BATTLE_PHASE)