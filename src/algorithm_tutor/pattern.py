"""
Core pattern model for algorithm study.
"""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class Difficulty(Enum):
    """Difficulty levels for patterns and problems."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class PatternCategory(Enum):
    """Core algorithmic pattern categories."""

    ARRAYS = "arrays"
    STRINGS = "strings"
    TWO_POINTERS = "two_pointers"
    SLIDING_WINDOW = "sliding_window"
    LINKED_LISTS = "linked_lists"
    TREES = "trees"
    GRAPHS = "graphs"
    DYNAMIC_PROGRAMMING = "dynamic_programming"
    BACKTRACKING = "backtracking"
    BINARY_SEARCH = "binary_search"
    HEAP = "heap"
    STACK = "stack"
    INTERVALS = "intervals"
    GREEDY = "greedy"
    TRIE = "trie"


class Problem(BaseModel):
    """Individual algorithm problem within a pattern."""

    name: str
    description: str
    difficulty: Difficulty
    leetcode_url: Optional[str] = None
    solution_template: Optional[str] = None
    key_insights: List[str] = []


class Pattern(BaseModel):
    """Core algorithmic pattern for structured learning."""

    name: str
    category: PatternCategory
    description: str
    key_concepts: List[str]
    problems: List[Problem] = []
    time_complexity_notes: str = ""
    space_complexity_notes: str = ""
    when_to_use: str = ""

    def get_problems_by_difficulty(self, difficulty: Difficulty) -> List[Problem]:
        """Get problems filtered by difficulty level."""
        return [p for p in self.problems if p.difficulty == difficulty]

    def get_progression_problems(self) -> List[Problem]:
        """Get problems in difficulty progression order."""
        easy = self.get_problems_by_difficulty(Difficulty.EASY)
        medium = self.get_problems_by_difficulty(Difficulty.MEDIUM)
        hard = self.get_problems_by_difficulty(Difficulty.HARD)
        return easy + medium + hard
