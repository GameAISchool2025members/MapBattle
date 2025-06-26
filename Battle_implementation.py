from data_structs import UnitStat, Grid, ResultOfBattle, Action, ActionType, ActionResult, Owner
from typing import List, Tuple, assert_never
import math as math
import copy as copy


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
        UnitTakingAction: UnitStat,
        EnemyUnits: List[UnitStat],
        MapGrid: Grid,
        ActionToApply: Action
    ) -> Tuple[List[UnitStat], Grid, Action]:

    MapGridCopy = copy.deepcopy(MapGrid)
    ActionToReturn = copy.deepcopy(ActionToApply)

    NewPos = ActionToReturn.GridIndexPosition
    OldPos = UnitTakingAction.CurrentPosition

    assert(MapGridCopy.Cells[NewPos[1]][NewPos[0]] == 0)
    MapGridCopy.Cells[NewPos[1]][NewPos[0]] = 1
    MapGridCopy.Cells[OldPos[1]][OldPos[0]] = 0

    UnitTakingAction.CurrentPosition = NewPos

    return tuple([EnemyUnits, MapGridCopy, ActionToReturn])

def ApplyAttackAction(
        UnitTakingAction: UnitStat,
        EnemyUnits: List[UnitStat],
        MapGrid: Grid,
        ActionToApply: Action
    ) -> Tuple[List[UnitStat], Grid, Action]:

    EnemyUnitsCopy = copy.deepcopy(EnemyUnits)
    MapGridCopy = copy.deepcopy(MapGrid)
    ActionToReturn = copy.deepcopy(ActionToApply)

    enemyIndex = FindUnitIndexByPos(EnemyUnitsCopy, ActionToApply.GridIndexPosition)
    assert(enemyIndex != -1)
    
    ActionToReturn.ResultOfAction = ActionResult(enemyIndex, UnitTakingAction.Damage, False)

    CurrentHealth = EnemyUnitsCopy[enemyIndex].CurrentHealth
    CurrentHealth = max(0, CurrentHealth - UnitTakingAction.Damage)

    if CurrentHealth == 0:
        ActionToReturn.ResultOfAction.Dead = True
        EnemyPos = EnemyUnitsCopy[enemyIndex].CurrentPosition
        MapGridCopy.Cells[EnemyPos[1]][EnemyPos[0]] = 0
        EnemyUnitsCopy.remove(EnemyUnitsCopy[enemyIndex])
    else:
        EnemyUnitsCopy[enemyIndex].CurrentHealth = CurrentHealth
    
    return tuple([EnemyUnitsCopy, MapGridCopy, ActionToReturn])

def ApplyAction(
        UnitTakingAction: UnitStat,
        EnemyUnits: List[UnitStat],
        MapGrid: Grid,
        ActionToApply: Action
    ) -> Tuple[List[UnitStat], Grid, Action]:

    if ActionToApply.Type == ActionToApply.Type.Move:
        return ApplyMoveAction(
            UnitTakingAction,
            EnemyUnits,
            MapGrid,
            ActionToApply
        )
    
    elif ActionToApply.Type == ActionToApply.Type.Attack:
        return ApplyAttackAction(
            UnitTakingAction,
            EnemyUnits,
            MapGrid,
            ActionToApply
        )


    return tuple([EnemyUnits, MapGrid, ActionToApply])

def DecideAction(
        UnitTakingAction: UnitStat,
        EnemyUnits: List[UnitStat],
        MapGrid: Grid
    ) -> Action:
    


    assert_never(UnitTakingAction)


def PrintGrid(MapGrid: Grid):
    for Row in MapGrid.Cells:
        print(Row)

def PrintUnits(AllUnits: List[UnitStat]):
    for Unit in AllUnits:
        print(Unit)


def Internal_Battle( 
        UnitsForAgentA: List[UnitStat],
        UnitsForAgentB: List[UnitStat],
        MapGrid: Grid
    ) -> ResultOfBattle:
    
    UnitsForACopy = copy.deepcopy(UnitsForAgentA)
    UnitsForBCopy = copy.deepcopy(UnitsForAgentB)
    MapCopy = copy.deepcopy(MapGrid)
    AllUnits = copy.deepcopy(UnitsForACopy)
    AllUnits.extend(copy.deepcopy(UnitsForBCopy))

    ToReturn = ResultOfBattle([], Owner.NoOwner)

    def UnitSort(UnitA: UnitStat) -> int:
        return UnitA.TurnOrderSpeed
 
    AllUnits.sort(key=UnitSort, reverse=True)

    for Unit in AllUnits:
        if Unit.OwningAgent == Owner.AgentA:
            EnemyList = UnitsForBCopy
        else:
            EnemyList = UnitsForACopy

        ActionToTake = DecideAction(Unit, EnemyList, MapCopy)
        Result = ApplyAction(Unit, EnemyList, MapCopy, ActionToTake)
        
        if Unit.OwningAgent == Owner.AgentA:
            UnitsForBCopy = Result[0]
        else:
            UnitsForACopy = Result[0]

        MapCopy = Result[1]
        ToReturn.ActionsTaken.append(Result[2])

    return None



if __name__ == "__main__":
    print("Starting Battle_implementation.py")


    MockGrid = Grid(5, 5, [
        [
            0, 1, 1, 0, 0
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

    MockUnitsA = list(
        [
            UnitStat(2, 5, 5, 10, 10, 0, 10, [1, 4], Owner.AgentA),
            UnitStat(2, 1, 5, 10, 10, 1, 10, [2, 4], Owner.AgentA)
        ]
    )

    MockUnitsB = list(
        [
            UnitStat(2, 5, 5, 10, 10, 2, 10, [1, 0], Owner.AgentB),
            UnitStat(2, 3, 5, 10, 10, 3, 10, [2, 0], Owner.AgentB)
        ]
    )
    
    results = Internal_Battle(MockUnitsA, MockUnitsB, MockGrid)

    PrintUnits(MockUnitsA)
    print()
    PrintUnits(MockUnitsB)
    


