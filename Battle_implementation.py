from data_structs import UnitStat, Grid, ResultOfBattle, Action
from typing import List, Tuple
import math as math

def Internal_Battle( 
        UnitsForAgentA: List[UnitStat],
        UnitsForAgentB: List[UnitStat],
        MapGrid: Grid
    ) -> ResultOfBattle:
    


    
    return None

def ManhattanDistanceBetweenPoints(
        PosA: Tuple[int, int],
        PosB: Tuple[int, int]
    ) -> int:

    return abs(PosA[0] - PosB[0]) + abs(PosA[1] - PosB[1])

def ApplyAction(
        AllUnits: List[UnitStat],
        MapGrid: Grid,
        ActionToApply: Action
    ) -> Tuple[List[UnitStat], Grid]:

    if ActionToApply.Type == ActionToApply.Type.Move:
        return ApplyMoveAction(
            AllUnits,
            MapGrid,
            ActionToApply
        )
    elif ActionToApply.Type == ActionToApply.Type.Attack:
        return ApplyAttackAction(
            AllUnits,
            MapGrid,
            ActionToApply
        )


    return Tuple(AllUnits, MapGrid)



def DecideOnAction(
        UnitTakingAction: UnitStat,
        EnemyUnits: List[UnitStat],
        MapGrid: Grid
    ) -> Action:
    


    return None


if __name__ == "__main__":
    print("Starting Battle_implementation.py")