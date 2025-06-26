from typing import List, Tuple

def get_agent_random_starting_positions(board_width: int, board_height: int, num_units: int) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    """
    Generate starting positions for both agents.
    Agent A starts at the bottom, Agent B starts at the top.
    
    Args:
        board_width: Width of the game board
        board_height: Height of the game board  
        num_units: Number of units per agent
    
    Returns:
        Tuple containing (agent_a_positions, agent_b_positions)
    """
    
    # Agent A positions (bottom rows)
    agent_a_positions = []
    
    # Place units in bottom 2-3 rows, centered horizontally
    start_x = max(0, (board_width - num_units) // 2)
    
    # First row (y=0 is bottom)
    for i in range(min(num_units, board_width)):
        if len(agent_a_positions) < num_units:
            x = (start_x + i) % board_width
            agent_a_positions.append((x, 0))
    
    # Second row if needed (y=1)
    remaining_units = num_units - len(agent_a_positions)
    for i in range(min(remaining_units, board_width)):
        if len(agent_a_positions) < num_units:
            x = (start_x + i) % board_width
            agent_a_positions.append((x, 1))
    
    # Third row if still needed (y=2)
    remaining_units = num_units - len(agent_a_positions)
    for i in range(remaining_units):
        if len(agent_a_positions) < num_units:
            x = (start_x + i) % board_width
            agent_a_positions.append((x, 2))
    
    # Agent B positions (top rows)
    agent_b_positions = []
    
    # First row from top (y=board_height-1)
    for i in range(min(num_units, board_width)):
        if len(agent_b_positions) < num_units:
            x = (start_x + i) % board_width
            agent_b_positions.append((x, board_height - 1))
    
    # Second row from top (y=board_height-2)
    remaining_units = num_units - len(agent_b_positions)
    for i in range(min(remaining_units, board_width)):
        if len(agent_b_positions) < num_units:
            x = (start_x + i) % board_width
            agent_b_positions.append((x, board_height - 2))
    
    # Third row from top if needed (y=board_height-3)
    remaining_units = num_units - len(agent_b_positions)
    for i in range(remaining_units):
        if len(agent_b_positions) < num_units:
            x = (start_x + i) % board_width
            agent_b_positions.append((x, board_height - 3))
    
    return agent_a_positions, agent_b_positions

def get_custom_starting_positions(board_width: int, board_height: int) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    """
    Alternative positioning function for custom layouts.
    You can modify this for specific positioning strategies.
    """
    
    # Agent A: Bottom-left corner formation
    agent_a_positions = [
        (0, 0), (1, 0), (2, 0),  # Bottom row
        (0, 1), (1, 1),          # Second row
        (0, 2)                   # Third row
    ]
    
    # Agent B: Top-right corner formation  
    agent_b_positions = [
        (board_width-1, board_height-1), (board_width-2, board_height-1), (board_width-3, board_height-1),  # Top row
        (board_width-1, board_height-2), (board_width-2, board_height-2),                                  # Second row
        (board_width-1, board_height-3)                                                                    # Third row
    ]
    
    return agent_a_positions, agent_b_positions

# Test function
if __name__ == "__main__":
    print("Testing positioning logic...")
    
    # Test with different board sizes
    test_configs = [
        (10, 8, 4),   # 10x8 board, 4 units each
        (12, 10, 6),  # 12x10 board, 6 units each
        (8, 6, 3)     # 8x6 board, 3 units each
    ]
    
    for width, height, units in test_configs:
        print(f"\n=== Board: {width}x{height}, Units: {units} ===")
        pos_a, pos_b = get_agent_random_starting_positions(width, height, units)
        
        print("Agent A (bottom):", pos_a)
        print("Agent B (top):", pos_b)
        
        # Visualize on grid
        grid = [['.' for _ in range(width)] for _ in range(height)]
        
        for x, y in pos_a:
            grid[y][x] = 'A'
        for x, y in pos_b:
            grid[y][x] = 'B'
        
        # Print grid (flip Y for display since [0,0] is bottom-left)
        for y in range(height-1, -1, -1):
            print(''.join(grid[y]))