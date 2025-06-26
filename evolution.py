from data_structs import UnitStat, Grid, ResultOfBattle
from typing import List
from EA_implementation import Internal_RunEvolution


def RunEvolution(  
        UnitsForAgentA: List[UnitStat],
        UnitsForAgentB: List[UnitStat],
        MapGrid: Grid,
        NumberOfGenerations: int,
        PopulationSize: int,
        Seed: int
            ) -> ResultOfBattle:
    
    return Internal_RunEvolution(
        UnitsForAgentA,
        UnitsForAgentB,
        MapGrid,
        NumberOfGenerations,
        PopulationSize,
        Seed
    )
