from scipy import stats
from data_structs import UnitStat, Grid, ResultOfBattle, StatRanges, Owner
from typing import List, Tuple
from battle import Battle 
import random
import time

#Dummy Battle Implementation
# def Battle( 
#     UnitsForAgentA: List[UnitStat],
#     UnitsForAgentB: List[UnitStat],
#     MapGrid: Grid
#         ) -> ResultOfBattle:

#     return ResultOfBattle(
#         ActionsTaken=[],
#         Winner=Owner.AgentA if random.choice([True, False]) else Owner.AgentB
#     )


def Internal_RunEvolution(  
        UnitsForAgentA: List[UnitStat],
        UnitsForAgentB: List[UnitStat],
        MaxUnitBudget: int,
        MapGrid: Grid,
        NumberOfGenerations: int,
        PopulationSize: int,
        Seed: int
            ) -> Tuple[UnitStat, UnitStat]:
    random.seed(Seed)
    print(f'Evolving units for player A')
    best_unit_a = evolution_loop(UnitsForAgentA, UnitsForAgentB, MapGrid, MaxUnitBudget, NumberOfGenerations, PopulationSize, is_agent_a=True)
    print(f'Evolving units for player B')
    best_unit_b = evolution_loop(UnitsForAgentA, UnitsForAgentB, MapGrid, MaxUnitBudget, NumberOfGenerations, PopulationSize, is_agent_a=False)

    return best_unit_a, best_unit_b

def generate_random_unit(budget: int, is_agent_a: bool, map: Grid) -> List[int]:
    # Split budget randomly
    # TODO: Not sure if this is truly uniform
    statranges = StatRanges()
    statranges.set_map_bounds(map.Width, map.Height, is_agent_a)
    ranges = statranges.get_ranges()
    genome = [min_val for (min_val, max_val) in ranges]
    remaining_budget = budget - sum(genome[:-2])
    #Randomly distribute budget (budget does not apply to position)
    for i, r in enumerate(ranges[:-2]):
        min_val, max_val = r
        if remaining_budget > 0:
            allocated = random.randint(0, max_val-min_val)
            value_change = min(allocated, remaining_budget)
            genome[i] += value_change
            remaining_budget -= value_change
    genome[-2] = random.randint(statranges.get_mins()[-2], statranges.get_maxs()[-2])  # Random X position
    genome[-1] = random.randint(statranges.get_mins()[-1], statranges.get_maxs()[-1])  # Random Y position

    # Ensure the genome does not exceed the budget
    assert sum(genome[:-2]) <= budget, "Genome exceeds budget"
    assert all(genome[i] >= statranges.get_mins()[i] for i in range(len(genome))), "Genome has values below minimum"
    assert all(genome[i] <= statranges.get_maxs()[i] for i in range(len(genome))), "Genome has values above maximum"
    return genome


def evaluate_fitness(genome: List[int], units_for_agent_a: List[UnitStat], units_for_agent_b: List[UnitStat], map_grid: Grid, is_agent_a: bool, budget: int, iterations: int = 10) -> float:
    results = 0
    unit = UnitStat.from_genome(genome, Owner.AgentA if is_agent_a else Owner.AgentB)
    for _ in range(iterations):
        new_units_for_agent_a = units_for_agent_a + [unit] if is_agent_a else units_for_agent_a + [UnitStat.from_genome(generate_random_unit(budget, is_agent_a=True, map=map_grid), Owner.AgentA)]
        new_units_for_agent_b = units_for_agent_b + [UnitStat.from_genome(generate_random_unit(budget, is_agent_a=False, map=map_grid), Owner.AgentB)] if is_agent_a else units_for_agent_b + [unit]
        # print(f'Running battle simulation...')
        result = Battle(new_units_for_agent_a, new_units_for_agent_b, map_grid)
        results += 1 if result.Winner == (Owner.AgentA if is_agent_a else Owner.AgentB) else 0

    return results / iterations

def select_parents(population: List[List[int]], fitness_scores: List[float]) -> Tuple[List[int], List[int]]:
    # Select two parents based on their fitness scores
    total_fitness = sum(fitness_scores)
    if total_fitness == 0:
        # If all fitness scores are zero, select randomly
        return random.sample(population, 2)
    selection_probs = [score / total_fitness for score in fitness_scores]
    parents = random.choices(population, weights=selection_probs, k=2)
    return parents[0], parents[1]

def generate_offspring(parents: Tuple[List[int], List[int]], budget: int, is_agent_a: bool, map: Grid) -> List[List[int]]:
    parent1, parent2 = parents
    statranges = StatRanges()
    statranges.set_map_bounds(map.Width, map.Height, is_agent_a)
    # Crossover and mutation logic to create offspring
    offspring = []

    for _ in range(2):  # Generate two offspring
        # Create a genome by averaging parent values
        child_genome = [(p1 + p2) // 2 for p1, p2 in zip(parent1, parent2)]

        # Compute remaining budget (will always be non-negative)
        remaining_budget = budget - sum(child_genome)

        # Randomly adjust the genome within the budget
        while remaining_budget > 0:
            selected_idx = random.randint(0, len(child_genome) - 1)
            new_value = min(child_genome[selected_idx] + 1, statranges.get_maxs()[-2])
            if new_value != child_genome[selected_idx]:
                remaining_budget -= 1
                child_genome[selected_idx] = new_value

        # Apply mutation
        mutation_idx = random.randint(0, len(child_genome) - 1)
        mutation_amount = random.randint(-2, 2)
        value_change = min(max(statranges.get_mins()[mutation_idx], child_genome[mutation_idx] + mutation_amount), statranges.get_maxs()[mutation_idx])
        child_genome[mutation_idx] = value_change
        #Reapply somewhere else
        if mutation_idx < len(child_genome) - 2:  
            remaining_mutation_amount = value_change - child_genome[mutation_idx]
            while remaining_mutation_amount != 0:
                reapply_idx = random.randint(0, len(child_genome) - 1)
                remaining_mutation_amount = mutation_amount
                new_value = min(max(statranges.get_mins()[reapply_idx], child_genome[reapply_idx] - remaining_mutation_amount), statranges.get_maxs()[reapply_idx])
                remaining_budget -= new_value - child_genome[reapply_idx]
                child_genome[reapply_idx] = new_value

        # Ensure stats are within bounds
        child_genome = [min(max(statranges.get_mins()[i], child_genome[i]), statranges.get_maxs()[i]) for i in range(len(child_genome))]
        offspring.append(child_genome)
        
        # Ensure the genome does not exceed the budget
        assert sum(child_genome[:-2]) <= budget, "Genome exceeds budget"
        assert all(child_genome[i] >= statranges.get_mins()[i] for i in range(len(child_genome))), "Genome has values below minimum"
        assert all(child_genome[i] <= statranges.get_maxs()[i] for i in range(len(child_genome))), "Genome has values above maximum"
    return offspring

def evolution_loop(UnitsForAgentA: List[UnitStat], UnitsForAgentB: List[UnitStat], MapGrid: Grid, MaxUnitBudget: int, NumberOfGenerations: int, PopulationSize: int, is_agent_a: bool) -> UnitStat:
    population = [generate_random_unit(MaxUnitBudget, is_agent_a=is_agent_a, map=MapGrid) for _ in range(PopulationSize)]

    for generation in range(NumberOfGenerations):
        print(f"Generation {generation + 1}/{NumberOfGenerations}")
        fitness_scores = [evaluate_fitness(unit, UnitsForAgentA, UnitsForAgentB, MapGrid, is_agent_a, budget=MaxUnitBudget) for unit in population]
        offspring = []
        for _ in range(PopulationSize//2):
            parents = select_parents(population, fitness_scores)
            children = generate_offspring(parents, MaxUnitBudget, is_agent_a=is_agent_a, map=MapGrid)
            children = [repair_positions(child, UnitsForAgentA + UnitsForAgentB, MapGrid) for child in children]
            offspring.extend(children)
        population = offspring

    return max(population, key=lambda unit: evaluate_fitness(unit, UnitsForAgentA, UnitsForAgentB, MapGrid, is_agent_a, budget=MaxUnitBudget))

def repair_positions(new_unit: List[int], existing_units: List[UnitStat], grid: Grid) -> UnitStat:
    existing_positions = [unit.CurrentPosition for unit in existing_units]
    # If the new unit's position is already occupied, find a new position
    if new_unit[-2] in existing_positions or grid.Cells[new_unit[-1]][new_unit[-2]] != 0:
        # Find a new position in expanding rings around the original position
        x, y = new_unit[-2], new_unit[-1]
        found = False
        for r in range(1, max(grid.Height, grid.Width)):
                # Check positions in a square ring around (x, y)
                for dx in range(-r, r+1):
                        for dy in [-r, r]:  # Top and bottom edges of the ring
                                new_x, new_y = x + dx, y + dy
                                if (0 <= new_x < grid.Width and 0 <= new_y < grid.Height and 
                                        grid.Cells[new_y][new_x] == 0 and 
                                        (new_x, new_y) not in existing_positions):
                                        new_unit[-2], new_unit[-1] = new_x, new_y
                                        found = True
                                        break
                        if found: break
                
                if not found:
                        for dx in [-r, r]:  # Left and right edges of the ring
                                for dy in range(-r+1, r):  # Avoid double-counting corners
                                        new_x, new_y = x + dx, y + dy
                                        if (0 <= new_x < grid.Width and 0 <= new_y < grid.Height and 
                                                grid.Cells[new_y][new_x] == 0 and 
                                                (new_x, new_y) not in existing_positions):
                                                new_unit[-2], new_unit[-1] = new_x, new_y
                                                found = True
                                                break
                                if found: break
                
                if found: break
        
        # If no position found, place randomly as a fallback
        if not found:
                while True:
                        new_x = random.randint(0, grid.Width - 1)
                        new_y = random.randint(0, grid.Height - 1)
                        if grid.Cells[new_y][new_x] == 0 and (new_x, new_y) not in existing_positions:
                                new_unit[-2], new_unit[-1] = new_x, new_y
                                break

    return new_unit

if __name__ == "__main__":
    # Example usage
    units_a = [UnitStat.from_genome([1, 2, 3, 4, 5, 1, 1], Owner.AgentA)]
    units_b = [UnitStat.from_genome([2, 3, 4, 5, 6, 2, 2], Owner.AgentB)]
    grid = Grid(12, 14, [[0]*12 for _ in range(14)])
    
    best_a, best_b = Internal_RunEvolution(
        UnitsForAgentA=units_a,
        UnitsForAgentB=units_b, 
        MaxUnitBudget=20, 
        MapGrid=grid, 
        NumberOfGenerations=10, 
        PopulationSize=5, 
        Seed=42
    )
    #We are setting global seed, which should not be a problem since the battle simulation is deterministic.
    print("Best Unit A:", best_a)
    print("Best Unit B:", best_b)