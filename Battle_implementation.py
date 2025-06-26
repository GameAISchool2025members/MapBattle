from data_structs import UnitStat, Grid, ResultOfBattle, Action, ActionType, ActionResult
from typing import List, Tuple
import math as math
import copy as copy

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

def FindUnitIndexByID(
        AllUnits: List[UnitStat],
        UnitToFind: int
    ) -> int:

    for i, Unit in zip(range(0, len(AllUnits)), AllUnits):
        if Unit.UnitID == UnitToFind:
            return i
        
    return -1

def FindUnitIndexByPos(
        AllUnits: List[UnitStat],
        UnitPos: Tuple[int, int]
    ) -> int:

    for i, Unit in zip(range(0, len(AllUnits)), AllUnits):
        if Unit.CurrentPosition == UnitPos:
            return i
        
    return -1

def ApplyMoveAction(
        AllUnits: List[UnitStat],
        MapGrid: Grid,
        ActionToApply: Action
    ) -> Tuple[List[UnitStat], Grid, Action]:

    AllUnitsCopy = copy.deepcopy(AllUnits)
    MapGridCopy = copy.deepcopy(MapGrid)
    ActionToReturn = copy.deepcopy(ActionToApply)

    index = FindUnitIndexByID(AllUnitsCopy, ActionToApply.IDOfUnitTakingAction)

    assert(index != -1)

    NewPos = ActionToReturn.GridIndexPosition
    OldPos = AllUnitsCopy[i].CurrentPosition
    assert(MapGridCopy.Cells[NewPos[1]][NewPos[0]] == 0)
    MapGridCopy.Cells[NewPos[1]][NewPos[0]] = 1
    MapGridCopy.Cells[OldPos[1]][OldPos[0]] = 0
    AllUnitsCopy[i].CurrentPosition = NewPos

    return tuple([AllUnitsCopy, MapGridCopy, ActionToReturn])

def ApplyAttackAction(
        AllUnits: List[UnitStat],
        MapGrid: Grid,
        ActionToApply: Action
    ) -> Tuple[List[UnitStat], Grid, Action]:

    AllUnitsCopy = copy.deepcopy(AllUnits)
    MapGridCopy = copy.deepcopy(MapGrid)
    ActionToReturn = copy.deepcopy(ActionToApply)

    index = FindUnitIndexByID(AllUnitsCopy, ActionToApply.IDOfUnitTakingAction)
    assert(index != -1)
    enemyIndex = FindUnitIndexByPos(AllUnitsCopy, ActionToApply.GridIndexPosition)
    assert(enemyIndex != -1)
    
    ActionToReturn.ResultOfAction = ActionResult(enemyIndex, AllUnitsCopy[index].Damage, False)

    CurrentHealth = AllUnitsCopy[enemyIndex].CurrentHealth
    CurrentHealth = max(0, CurrentHealth - AllUnitsCopy[index].Damage)

    if CurrentHealth == 0:
        ActionToReturn.ResultOfAction.Dead = True
        EnemyPos = AllUnitsCopy[enemyIndex].CurrentPosition
        MapGridCopy.Cells[EnemyPos[1]][EnemyPos[0]] = 0
        AllUnitsCopy.remove(AllUnitsCopy[enemyIndex])
    else:
        AllUnitsCopy[enemyIndex].CurrentHealth = CurrentHealth
    
    return tuple([AllUnitsCopy, MapGridCopy, ActionToReturn])

def ApplyAction(
        AllUnits: List[UnitStat],
        MapGrid: Grid,
        ActionToApply: Action
    ) -> Tuple[List[UnitStat], Grid, Action]:

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


    return tuple([AllUnits, MapGrid, ActionToApply])



def DecideOnAction(
        UnitTakingAction: UnitStat,
        EnemyUnits: List[UnitStat],
        MapGrid: Grid
    ) -> Action:
    


    return None


def PrintGrid(MapGrid: Grid):
    for Row in MapGrid.Cells:
        print(Row)

def PrintUnits(AllUnits: List[UnitStat]):
    for Unit in AllUnits:
        print(Unit)

if __name__ == "__main__":
    print("Starting Battle_implementation.py")


    MockGrid = Grid(5, 5, [
        [
            0, 0, 0, 0, 0
        ],
        [
            0, 0, 0, 0, 0
        ],
        [
            0, 0, 0, 0, 0
        ],
        [
            0, 0, 0, 0, 0
        ],
        [
            0, 1, 1, 0, 0
        ]
    ])

    MockUnits = list(
        [
            UnitStat(2, 3, 5, 10, 10, 0, 10, [1, 4]),
            UnitStat(2, 3, 5, 10, 10, 1, 10, [2, 4])
        ]
    )

    ActionToTake = Action(
        0,
        ActionType.Attack,
        [2, 4],
        None
    )

    PrintUnits(MockUnits)
    PrintGrid(MockGrid)

    ResultAction = ApplyAttackAction(
        MockUnits,
        MockGrid,
        ActionToTake
    )

    print()
    PrintUnits(ResultAction[0])
    PrintGrid(ResultAction[1])
    


