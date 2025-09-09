"""
Algorithm Tutor - Structured pattern-based interview preparation.

A Python-based algorithm study system focused on the 15-20 core patterns
that cover 80%+ of technical interview questions. Emphasizes quality over
quantity and uses spaced repetition for optimal learning.
"""

__version__ = "0.1.0"

from .pattern import Difficulty, Pattern, PatternCategory, Problem
from .patterns_db import get_core_patterns, get_pattern_by_name
from .study_session import StudyRecord, StudySession
from .tutor import AlgorithmTutor

__all__ = [
    "AlgorithmTutor",
    "Pattern",
    "PatternCategory",
    "Problem",
    "Difficulty",
    "StudySession",
    "StudyRecord",
    "get_core_patterns",
    "get_pattern_by_name",
]
