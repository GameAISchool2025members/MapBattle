from dataclasses import dataclass
from time import time
from typing import List, Tuple
from enum import Enum
from EA_implementation import generate_random_unit
import uuid

class ActionType(Enum):
    NoneOP = 0,
    Move = 1,
    Attack = 2

class Owner(Enum):
    NoOwner = 0,
    AgentA = 1,
    AgentB = 2,
    
@dataclass
class StatRanges:
    Range: Tuple[int, int] = (1, 5)
    TurnOrderSpeed: Tuple[int, int] = (1, 5)
    MoveRange: Tuple[int, int] = (1, 5)
    Damage: Tuple[int, int] = (1, 5)
    MaxHealth: Tuple[int, int] = (1, 15)
    PositionX: Tuple[int, int] = (0, 10)
    PositionY: Tuple[int, int] = (0, 10)
    def set_map_bounds(self, width: int, height: int, is_agent_a: bool):
        if is_agent_a:
            self.PositionX = (0, width-1)
            self.PositionY = (0, height//2-1)
        else:
            self.PositionX = (0, width-1)
            self.PositionY = (height//2, height-1)
    def get_mins(self) -> List[int]:
        return [self.Range[0], self.TurnOrderSpeed[0], self.MoveRange[0], self.Damage[0], self.MaxHealth[0], self.PositionX[0], self.PositionY[0]]
    def get_maxs(self) -> List[int]:
        return [self.Range[1], self.TurnOrderSpeed[1], self.MoveRange[1], self.Damage[1], self.MaxHealth[1], self.PositionX[1], self.PositionY[1]]
    def get_ranges(self) -> List[Tuple[int, int]]:
        return [self.Range, self.TurnOrderSpeed, self.MoveRange, self.Damage, self.MaxHealth, self.PositionX, self.PositionY]


@dataclass
class Grid:
    Width: int
    Height: int
    Cells: List[List[int]]

    # Position [0, 0] is BOTTOM LEFT

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
    Winner: Owner


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
    OwningAgent: Owner

    def from_genome(genome: List[int], owning_agent: Owner) -> 'UnitStat':
        return UnitStat(
            Range=genome[0],
            TurnOrderSpeed=genome[1],
            MoveRange=genome[2],
            Damage=genome[3],
            MaxHealth=genome[4],
            UnitID=uuid.uuid4().int,  # Generate a unique ID for the unit
            CurrentHealth=genome[4],
            CurrentPosition=(genome[5], genome[6]),
            OwningAgent=owning_agent
        )
    
    def generate_unit(budget: int, owning_agent: Owner, map: Grid):
        genome = generate_random_unit(budget, owning_agent == Owner.AgentA, map)
        return UnitStat.from_genome(genome, owning_agent)