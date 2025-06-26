from data_structs import UnitStat, Grid, Owner
from typing import List, Dict, Any
from starting_positions import get_agent_starting_positions
import random

def create_random_units(num_units: int, owner: Owner, start_positions: List[tuple], id_offset: int = 0) -> List[UnitStat]:
    """Create random units for an agent"""
    units = []

    for i in range(num_units):
        max_health = random.randint(30, 80)
        unit = UnitStat(
            Range=random.randint(1, 4),           # Random range 1-4
            TurnOrderSpeed=random.randint(3, 8),  # Random speed 3-8
            MoveRange=random.randint(2, 5),       # Random move range 2-5
            Damage=random.randint(8, 20),         # Random damage 8-20
            MaxHealth=max_health,                 # Random health 30-80
            UnitID=i + id_offset,                 # Unique IDs
            CurrentHealth=max_health,             # Set to max health
            CurrentPosition=start_positions[i] if i < len(start_positions) else (0, 0),
            OwningAgent=owner                     # Set the owner
        )
        units.append(unit)

    return units

def game_init() -> Dict[str, Any]:
    """Initialize the game state and return all necessary data"""

    # Set board size
    board_width = 12
    board_height = 10

    # Initialize the grid (0 = empty, 1 = occupied)
    cells = [[0 for _ in range(board_width)] for _ in range(board_height)]

    # Create the Grid object
    game_grid = Grid(
        Width=board_width,
        Height=board_height,
        Cells=cells
    )

    # Get starting positions from positioning module
    num_units_per_agent = 4
    agent_a_positions, agent_b_positions = get_agent_starting_positions(
        board_width,
        board_height,
        num_units_per_agent
    )

    # Create random units for both agents
    units_agent_a = create_random_units(
        num_units_per_agent,
        Owner.AgentA,
        agent_a_positions,
        id_offset=0
    )
    units_agent_b = create_random_units(
        num_units_per_agent,
        Owner.AgentB,
        agent_b_positions,
        id_offset=100  # Different ID range for Agent B
    )

    # Mark occupied positions on the grid
    for unit in units_agent_a + units_agent_b:
        x, y = unit.CurrentPosition
        game_grid.Cells[y][x] = 1  # Mark as occupied

    # Return all game initialization data
    return {
        'units_agent_a': units_agent_a,
        'units_agent_b': units_agent_b,
        'game_grid': game_grid,
        'board_width': board_width,
        'board_height': board_height
    }

# Test function to see the initialized units
def print_game_state(game_data: Dict[str, Any]):
    """Helper function to print the game state for debugging"""
    print("=== AGENT A UNITS (Bottom) ===")
    for unit in game_data['units_agent_a']:
        print(f"ID: {unit.UnitID}, Health: {unit.CurrentHealth}/{unit.MaxHealth}, "
              f"Pos: {unit.CurrentPosition}, Owner: {unit.OwningAgent}")

    print("\n=== AGENT B UNITS (Top) ===")
    for unit in game_data['units_agent_b']:
        print(f"ID: {unit.UnitID}, Health: {unit.CurrentHealth}/{unit.MaxHealth}, "
              f"Pos: {unit.CurrentPosition}, Owner: {unit.OwningAgent}")

    print(f"\n=== GRID ({game_data['board_width']}x{game_data['board_height']}) ===")
    # Print grid with Y-axis flipped (since [0,0] is bottom-left)
    for y in range(game_data['board_height']-1, -1, -1):
        row_display = []
        for x in range(game_data['board_width']):
            if game_data['game_grid'].Cells[y][x] == 1:
                # Check which agent owns this position
                is_agent_a = any(unit.CurrentPosition == (x, y) for unit in game_data['units_agent_a'])
                row_display.append('A' if is_agent_a else 'B')
            else:
                row_display.append('.')
        print(''.join(row_display) + f" <- y={y}")

# Test the initialization if run directly
if __name__ == "__main__":
    print("Testing game initialization...")
    test_data = game_init()
    print_game_state(test_data)