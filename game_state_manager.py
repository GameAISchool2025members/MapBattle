from enum import Enum

class GameState(Enum):
    MENU = 1
    PRE_PHASE = 2
    BATTLE_PHASE = 3
    END_PHASE = 4
    QUIT = 5

class GameStateManager:
    def __init__(self):
        self.state = GameState.MENU
        self.battle_generator = None

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def SetBattleGenerator(self, battle_generator):
        self.battle_generator = battle_generator
    
    def GetBattleGenerator(self):
        return self.battle_generator