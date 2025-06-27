from data_structs import UnitStat, Grid, ResultOfBattle, Action, ActionType, ActionResult, Owner
from typing import List, Tuple
from collections import deque
import math as math
import copy as copy
import time as time


def ManhattanDistanceBetweenPoints(
        PosA: Tuple[int, int],
        PosB: Tuple[int, int]
    ) -> int:

    return abs(PosA[0] - PosB[0]) + abs(PosA[1] - PosB[1])

def AttackDistanceBetweenPoints(
        PosA: Tuple[int, int],
        PosB: Tuple[int, int]
    ) -> int:

    return min(abs(PosA[0] - PosB[0]), abs(PosA[1] - PosB[1]))

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

    MapGridCopy = MapGrid
    ActionToReturn = ActionToApply

    #print(UnitTakingAction.UnitID)
    NewPos = ActionToReturn.GridIndexPosition
    OldPos = UnitTakingAction.CurrentPosition

    if NewPos == OldPos:
        return tuple([EnemyUnits, MapGridCopy, ActionToReturn])

    assert(MapGridCopy.Cells[NewPos[1]][NewPos[0]] == 0)
    MapGridCopy.Cells[NewPos[1]][NewPos[0]] = 2
    MapGridCopy.Cells[OldPos[1]][OldPos[0]] = 0

    UnitTakingAction.CurrentPosition = NewPos

    return tuple([EnemyUnits, MapGridCopy, ActionToReturn])

def ApplyAttackAction(
        UnitTakingAction: UnitStat,
        EnemyUnits: List[UnitStat],
        MapGrid: Grid,
        ActionToApply: Action
    ) -> Tuple[List[UnitStat], Grid, Action]:

    EnemyUnitsCopy = EnemyUnits
    MapGridCopy = MapGrid
    ActionToReturn = ActionToApply

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

def IsEnemyInRange(UnitTakingAction: UnitStat,
                   EnemyToCheck: UnitStat) -> bool:
    UnitAPos = UnitTakingAction.CurrentPosition
    UnitBPos = EnemyToCheck.CurrentPosition

    return AttackDistanceBetweenPoints(UnitAPos, UnitBPos) <= UnitTakingAction.Range


def GetAllEnemiesInRange(
            UnitTakingAction: UnitStat,
            EnemyUnits: List[UnitStat]
        ) -> List[UnitStat]:

    ReturnList = []

    for Enemy in EnemyUnits:
        if IsEnemyInRange(UnitTakingAction, Enemy):
            ReturnList.append(Enemy)

    return ReturnList


def GetNeighbours(
            Pos: Tuple[int, int], 
            MapGrid: Grid
        ) -> List[Tuple[int, int]]:
    Directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, 1), (1, -1)]
    Neighbors = []
    Rows, Cols = MapGrid.Height, MapGrid.Width
    for dx, dy in Directions:
        nx, ny = Pos[0] + dx, Pos[1] + dy
        if 0 <= ny < Rows and 0 <= nx < Cols and MapGrid.Cells[ny][nx] == 0:
            Neighbors.append([nx, ny])
    return Neighbors

def FindPathToTarget(
            StartPos: Tuple[int, int], 
            TargetPos: Tuple[int, int], 
            MapGrid: Grid
        ) -> List[Tuple[int, int]]:
    Queue = deque([(StartPos, [StartPos])])
    Visited = list(StartPos)
    ClosestPath = []
    ClosestDistance = float('inf')

    while Queue:
        CurrentPos, Path = Queue.popleft()
        CurrentDistance = ManhattanDistanceBetweenPoints(CurrentPos, TargetPos)

        if CurrentPos == TargetPos:
            return Path

        if CurrentDistance < ClosestDistance:
            ClosestDistance = CurrentDistance
            ClosestPath = Path

        for Neighbor in GetNeighbours(CurrentPos, MapGrid):
            if Neighbor not in Visited:
                Visited.append(Neighbor)
                Queue.append((Neighbor, Path + [Neighbor]))

    return ClosestPath

def FindPositionToMoveTo(
            StartPos: Tuple[int, int],
            AllPositionsToTest: List[Tuple[int, int]],
            MapGrid: Grid,
            AvailableSteps: int
        ) -> Tuple[int, int]:

    BestPathTargetPos = tuple([-1, -1])
    BestPath = []
    ShortestDistance = float('inf')

    for Pos in AllPositionsToTest:
        Path = FindPathToTarget(StartPos, Pos, MapGrid)
        if Path:
            Distance = ManhattanDistanceBetweenPoints(Path[-1], Pos)
            if Distance < ShortestDistance or (Distance == ShortestDistance and len(Path) < len(BestPath)):
                BestPath = Path
                BestPathTargetPos = Pos
                ShortestDistance = Distance

    if len(BestPath) == 0 or BestPath == [StartPos]:
        return []

    #print(BestPath)
    if BestPath[-1][0] == BestPathTargetPos[0] and BestPath[-1][1] == BestPathTargetPos[1]:
        BestPath.pop()
    #print(BestPath)

    if len(BestPath) > AvailableSteps:
        return BestPath[AvailableSteps]
    elif BestPath:
        return BestPath[-1]
    else:
        return []


def DecideAction(
        UnitTakingAction: UnitStat,
        EnemyUnits: List[UnitStat],
        MapGrid: Grid
    ) -> Action:
    assert(len(EnemyUnits) != 0)
    ReturnAction = Action(UnitTakingAction.UnitID, ActionType.NoneOP, [-1, -1], None)

    EnemiesInRange = GetAllEnemiesInRange(UnitTakingAction, EnemyUnits)
    if len(EnemiesInRange) != 0:
        ReturnAction.Type = ActionType.Attack

        BestTarget = EnemiesInRange[0]
        for Enemy in EnemiesInRange:
            if Enemy.CurrentHealth < BestTarget.CurrentHealth:
                BestTarget = Enemy

        ReturnAction.GridIndexPosition = BestTarget.CurrentPosition

        return ReturnAction
    else:
        ReturnAction.Type = ActionType.Move
        AllEnemyPositions = []
        for Enemy in EnemyUnits:
            AllEnemyPositions.append(Enemy.CurrentPosition)

        MapGridCopy = copy.deepcopy(MapGrid)

        for Position in AllEnemyPositions:
            MapGridCopy.Cells[Position[1]][Position[0]] = 0

        PositionToMoveTo = FindPositionToMoveTo(
            UnitTakingAction.CurrentPosition,
            AllEnemyPositions,
            MapGridCopy,
            UnitTakingAction.MoveRange)
        #print(PositionToMoveTo)
        if len(PositionToMoveTo) == 0:
            ReturnAction.Type = ActionType.NoneOP
        ReturnAction.GridIndexPosition = PositionToMoveTo

        return ReturnAction
    


def PrintGrid(MapGrid: Grid):
    for Row in MapGrid.Cells:
        print(Row)

def PrintUnits(AllUnits: List[UnitStat]):
    for Unit in AllUnits:
        print(f"Unit {Unit.UnitID} is at position {Unit.CurrentPosition} with {Unit.CurrentHealth} health")


def Internal_Battle( 
        UnitsForAgentA: List[UnitStat],
        UnitsForAgentB: List[UnitStat],
        MapGrid: Grid
    ) -> ResultOfBattle:

    UnitsForACopy = copy.deepcopy(UnitsForAgentA)
    UnitsForBCopy = copy.deepcopy(UnitsForAgentB)
    MapCopy = copy.deepcopy(MapGrid)
    AllUnits = []
    AllUnits.extend(UnitsForACopy)
    AllUnits.extend(UnitsForBCopy)

    for Unit in AllUnits:
        MapCopy.Cells[Unit.CurrentPosition[1]][Unit.CurrentPosition[0]] = 2

    #print("Before Battle:")
    #PrintGrid(MapCopy)
    #PrintUnits(UnitsForACopy)
    #PrintUnits(UnitsForBCopy)
    #print()

    ToReturn = ResultOfBattle([], Owner.NoOwner)

    def UnitSort(UnitA: UnitStat) -> int:
        return UnitA.TurnOrderSpeed

    AllUnits.sort(key=UnitSort, reverse=True)

    while len(UnitsForACopy) != 0 and len(UnitsForBCopy) != 0:
        KilledUnits = []
        for Unit in AllUnits:
            if len(UnitsForACopy) == 0 or len(UnitsForBCopy) == 0:
                break

            if Unit.OwningAgent == Owner.AgentA:
                if Unit not in UnitsForACopy:
                    continue
                EnemyList = UnitsForBCopy
            else:
                if Unit not in UnitsForBCopy:
                    continue
                EnemyList = UnitsForACopy

            ActionToTake = DecideAction(Unit, EnemyList, MapCopy)
            #print(f"Unit {Unit.UnitID} is to take the {ActionToTake.Type} action, targeting position {ActionToTake.GridIndexPosition}")
            #print()
            #print("After Action Decide:")
            #PrintGrid(MapCopy)
            #PrintUnits(UnitsForACopy)
            #PrintUnits(UnitsForBCopy)
            #print()
            #print(len(EnemyList))
            Result = ApplyAction(Unit, EnemyList, MapCopy, ActionToTake)

            if Result[2].Type == ActionType.Attack and Result[2].ResultOfAction.Dead == True:
                KilledUnits.append(Result[2].ResultOfAction.IDOfUnitAffected)
            
            if Unit.OwningAgent == Owner.AgentA:
                UnitsForBCopy = Result[0]
                for UnitA, index in zip(UnitsForACopy, range(0, len(UnitsForACopy))):
                    if UnitA.UnitID == Unit.UnitID:
                        UnitsForACopy[index] = Unit
                        break
            else:
                UnitsForACopy = Result[0]
                for UnitB, index in zip(UnitsForBCopy, range(0, len(UnitsForBCopy))):
                    if UnitB.UnitID == Unit.UnitID:
                        UnitsForBCopy[index] = Unit
                        break
                        
            MapCopy = Result[1]
            ToReturn.ActionsTaken.append(Result[2])
            print(Result[2].Type)

            #print(f"Unit {Unit.UnitID} took the {Result[2].Type} action, targeting position {Result[2].GridIndexPosition}")
            #print()
            #print("After Action:")
            #PrintGrid(MapCopy)
            #PrintUnits(UnitsForACopy)
            #PrintUnits(UnitsForBCopy)
            #print()
            #input()
        
        if len(KilledUnits) != 0:
            AllUnits = []
            AllUnits.extend(UnitsForACopy)
            AllUnits.extend(UnitsForBCopy)
            AllUnits.sort(key=UnitSort, reverse=True)

    ToReturn.Winner = Owner.AgentA if len(UnitsForACopy) != 0 else Owner.AgentB

    return ToReturn



if __name__ == "__main__":
    print("Starting Battle_implementation.py")


    MockGrid = Grid(12, 14, [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
        [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
        [0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0],
        [0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0],
        [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0],
        [0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])


    MockUnitsA = list(
        [
            UnitStat(2, 5, 2, 2, 10, 0, 10, [0, 13], Owner.AgentA),
            UnitStat(2, 1, 3, 3, 10, 1, 10, [1, 13], Owner.AgentA),
            UnitStat(2, 5, 2, 2, 10, 2, 10, [2, 13], Owner.AgentA),
            UnitStat(2, 1, 3, 3, 10, 3, 10, [3, 13], Owner.AgentA),
            UnitStat(2, 5, 2, 2, 10, 4, 10, [4, 13], Owner.AgentA),
            UnitStat(2, 1, 3, 3, 10, 5, 10, [5, 13], Owner.AgentA)
        ]
    )

    MockUnitsB = list(
        [
            UnitStat(2, 5, 3, 4, 10, 6, 10, [0, 0], Owner.AgentB),
            UnitStat(2, 3, 2, 1, 10, 7, 10, [1, 0], Owner.AgentB),
            UnitStat(2, 5, 3, 4, 10, 8, 10, [2, 0], Owner.AgentB),
            UnitStat(2, 3, 2, 1, 10, 9, 10, [3, 0], Owner.AgentB),
            UnitStat(2, 5, 3, 4, 10, 10, 10, [4, 0], Owner.AgentB),
            UnitStat(2, 3, 2, 1, 10, 11, 10, [5, 0], Owner.AgentB)
        ]
    )
    
    StartTime = time.time()
    TestIterations = 1000
    for i in range(0, TestIterations):
        results = Internal_Battle(MockUnitsA, MockUnitsB, MockGrid)
    
    EndTime = time.time()

    print((EndTime-StartTime)/TestIterations)
    


