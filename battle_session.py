from dataclasses import dataclass
from typing import List
from data_structs import ResultOfBattle, Owner


@dataclass
class BattleStats:
    agent_a_wins: int = 0
    agent_b_wins: int = 0
    total_battles: int = 0
    battle_results: List[ResultOfBattle] = None

    def __post_init__(self):
        if self.battle_results is None:
            self.battle_results = []

    def add_battle_result(self, result: ResultOfBattle):
        """Add a battle result and update win counters"""
        self.battle_results.append(result)
        self.total_battles += 1

        if result.Winner == Owner.AgentA:
            self.agent_a_wins += 1
        elif result.Winner == Owner.AgentB:
            self.agent_b_wins += 1

    def get_win_rate_a(self) -> float:
        """Get Agent A's win rate as percentage"""
        if self.total_battles == 0:
            return 0.0
        return (self.agent_a_wins / self.total_battles) * 100

    def get_win_rate_b(self) -> float:
        """Get Agent B's win rate as percentage"""
        if self.total_battles == 0:
            return 0.0
        return (self.agent_b_wins / self.total_battles) * 100

    def get_summary(self) -> str:
        """Get a formatted summary of the battle session"""
        return (f"Battle Session Summary:\n"
                f"Total Battles: {self.total_battles}\n"
                f"Agent A Wins: {self.agent_a_wins} ({self.get_win_rate_a():.1f}%)\n"
                f"Agent B Wins: {self.agent_b_wins} ({self.get_win_rate_b():.1f}%)")

    def reset(self):
        """Reset all statistics"""
        self.agent_a_wins = 0
        self.agent_b_wins = 0
        self.total_battles = 0
        self.battle_results.clear()