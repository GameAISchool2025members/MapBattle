from data_structs import UnitStat, Grid, ResultOfBattle
from typing import List
from Battle_implementation import Internal_Battle

def Battle( 
    UnitsForAgentA: List[UnitStat],
    UnitsForAgentB: List[UnitStat],
    MapGrid: Grid
        ) -> ResultOfBattle:
    
    return Internal_Battle(
        UnitsForAgentA,
        UnitsForAgentB, 
        MapGrid
    )

