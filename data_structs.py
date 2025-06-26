from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum

class ActionType(Enum):
    NoneOP = 0,
    Move = 1,
    Attack = 2

@dataclass
class UnitStat:
    Range: int
    TurnOrderSpeed: int
    MoveRange: int
    Damage: int
    MaxHealth: int

    UnitID: int
    CurrentHealth: int
    CurrentPosition: Tuple[int, int]

@dataclass
class Grid:
    Width: int
    Height: int
    Cells: List[List[int]]

@dataclass
class ActionResult:
    IDOfUnitAffected: int
    HealthLost: int
    Dead: bool

@dataclass
class Action:
    IDOfUnitTakingAction: int
    Type: ActionType
    GridIndexPosition: Tuple[int, int]
    ResultOfAction: ActionResult


@dataclass
class ResultOfBattle:
    ActionsTaken: List[Action]
    Winner: int