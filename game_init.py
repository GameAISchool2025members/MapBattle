from dataclasses import dataclass

from data_structs import UnitStat, Grid, Owner
from typing import List
from starting_positions import get_agent_random_starting_positions
import random


@dataclass
class BattleState:
    UnitsAgentA: List[UnitStat]
    UnitsAgentB: List[UnitStat]
    GameGrid: Grid
    BoardWidth: int
    BoardHeight: int


def create_random_units(num_units: int, owner: Owner, start_positions: List[tuple], game_grid: Grid) -> List[UnitStat]:
    """Create random units for an agent"""

    units = []

    for i in range(num_units):
        max_health = random.randint(30, 80)

        """unit = UnitStat(
            Range=random.randint(1, 4),
            TurnOrderSpeed=random.randint(3, 8),
            MoveRange=random.randint(2, 5),
            Damage=random.randint(8, 20),
            MaxHealth=max_health,
            UnitID=i,
            CurrentHealth=max_health,
            CurrentPosition=start_positions[i] if i < len(start_positions) else (0, 0),
            OwningAgent=owner
        )
        """
        unit = UnitStat.generate_unit(32, owner, game_grid)
        units.append(unit)

    return units

def setup_battle(in_board_width: int, in_board_height, in_num_units_per_agent) -> BattleState:
    """Initialize the game state and return all necessary data"""

    # Set board size
    board_width = in_board_width
    board_height = in_board_height

    # Initialize the grid (0 = empty, 1 = occupied)
    cells = [[0 for _ in range(board_width)] for _ in range(board_height)]

    # Create the Grid object
    game_grid = Grid(
        Width=board_width,
        Height=board_height,
        Cells=cells
    )

    # Get starting positions from positioning module
    num_units_per_agent = in_num_units_per_agent
    agent_a_positions, agent_b_positions = get_agent_random_starting_positions(
        board_width,
        board_height,
        num_units_per_agent
    )

    # Create random units for both agents
    units_agent_a = create_random_units(
        num_units_per_agent,
        Owner.AgentA,
        agent_a_positions,
        game_grid
    )
    units_agent_b = create_random_units(
        num_units_per_agent,
        Owner.AgentB,
        agent_b_positions,
        game_grid
    )

    # Mark occupied positions on the grid
    for unit in units_agent_a + units_agent_b:
        x, y = unit.CurrentPosition
        game_grid.Cells[y][x] = 1  # Mark as occupied

    # Return all game initialization data
    return BattleState(
        UnitsAgentA=units_agent_a,
        UnitsAgentB=units_agent_b,
        GameGrid=game_grid,
        BoardWidth=board_width,
        BoardHeight=board_height
    )