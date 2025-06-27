import battle
import game_state_manager
import game_init
import copy
from data_structs import UnitStat, Grid, Action, ActionType, Owner
from typing import List, Tuple
from collections import deque

def FindUnitIndexByPos(
        AllUnits: List[UnitStat],
        UnitPos: Tuple[int, int]
    ) -> int:

    for i, Unit in zip(range(0, len(AllUnits)), AllUnits):
        if Unit.CurrentPosition == UnitPos:
            return i
        
    return -1

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

def FindUnitByID(UnitID: int, AllUnits: List[UnitStat]) -> int:
    for Unit in AllUnits:
        if UnitID == Unit.UnitID:
            return Unit
    return None

def ManhattanDistanceBetweenPoints(
        PosA: Tuple[int, int],
        PosB: Tuple[int, int]
    ) -> int:

    return abs(PosA[0] - PosB[0]) + abs(PosA[1] - PosB[1])

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

def run(gameStateManager: game_state_manager, init_data: game_init.BattleState):
    battle_result = battle.Battle(init_data.UnitsAgentA,
                                  init_data.UnitsAgentB,
                                  init_data.GameGrid)
    
    UnitsForA = copy.deepcopy(init_data.UnitsAgentA)
    UnitsForB = copy.deepcopy(init_data.UnitsAgentB)
    MapCopy = copy.deepcopy(init_data.GameGrid)

    for ActionTaken in battle_result.ActionsTaken:
        if ActionTaken.Type == ActionType.NoneOP:
            continue
    
        AllUnits = UnitsForA + UnitsForB
        Unit = FindUnitByID(ActionTaken.IDOfUnitTakingAction, AllUnits)
        if ActionTaken.Type == ActionType.Attack:
            assert(Unit != None)
            if Unit.OwningAgent == Owner.AgentA:
                ApplyAttackAction(Unit, UnitsForB, MapCopy, ActionTaken)
            elif Unit.OwningAgent == Owner.AgentB:
                ApplyAttackAction(Unit, UnitsForA, MapCopy, ActionTaken)
        else:
            Path = FindPathToTarget(Unit.CurrentPosition, ActionTaken.GridIndexPosition, MapCopy)
            



    gameStateManager.set_state(game_state_manager.GameState.END_PHASE)
