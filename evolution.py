from data_structs import UnitStat, Grid, ResultOfBattle
from typing import List, Tuple
from EA_implementation import Internal_RunEvolution


def RunEvolution(  
        UnitsForAgentA: List[UnitStat],
        UnitsForAgentB: List[UnitStat],
        MaxUnitBudget: int,
        MapGrid: Grid,
        NumberOfGenerations: int,
        PopulationSize: int,
        Seed: int
            ) -> Tuple[UnitStat, UnitStat]:
    
    return Internal_RunEvolution(
        UnitsForAgentA,
        UnitsForAgentB,
        MaxUnitBudget,
        MapGrid,
        NumberOfGenerations,
        PopulationSize,
        Seed
    )
