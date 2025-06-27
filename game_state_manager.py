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
        self.generator = None

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def SetGenerator(self, generator):
        self.generator = generator
    
    def GetGenerator(self):
        return self.generator