"""
Main AlgorithmTutor class that orchestrates the learning process.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .pattern import Pattern
from .patterns_db import get_core_patterns, get_pattern_by_name
from .study_session import StudyRecord, StudySession


class AlgorithmTutor:
    """Main class for managing algorithm study sessions and progress."""

    def __init__(self, data_dir: str = None):
        """Initialize the tutor with data directory for persistence."""
        if data_dir is None:
            data_dir = os.path.expanduser("~/.algorithm_tutor")

        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.session_file = self.data_dir / "study_session.json"

        # Load or create study session
        self.session = self._load_session()
        self.patterns = get_core_patterns()

        # Initialize focus patterns if empty (first time use)
        if not self.session.current_focus_patterns:
            self._set_initial_focus_patterns()

    def _load_session(self) -> StudySession:
        """Load study session from file or create new one."""
        if self.session_file.exists():
            try:
                with open(self.session_file, "r") as f:
                    data = json.load(f)
                # Convert datetime strings back to datetime objects
                if "created_at" in data:
                    data["created_at"] = datetime.fromisoformat(data["created_at"])
                for record in data.get("study_records", []):
                    if "studied_at" in record:
                        record["studied_at"] = datetime.fromisoformat(
                            record["studied_at"]
                        )
                    # Ensure category is enum value
                    if "category" in record and isinstance(record["category"], str):
                        from .pattern import PatternCategory

                        record["category"] = PatternCategory(record["category"])
                return StudySession(**data)
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Warning: Could not load session file: {e}")
                print("Creating new session...")

        return StudySession()

    def _save_session(self) -> None:
        """Save current study session to file."""
        # Convert datetime objects and enums to strings for JSON serialization
        data = self.session.model_dump()
        data["created_at"] = self.session.created_at.isoformat()
        for record in data["study_records"]:
            record["studied_at"] = (
                datetime.fromisoformat(record["studied_at"]).isoformat()
                if isinstance(record["studied_at"], str)
                else record["studied_at"].isoformat()
            )
            # Ensure category is string value, not enum representation
            if hasattr(record["category"], "value"):
                record["category"] = record["category"].value

        with open(self.session_file, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def _set_initial_focus_patterns(self) -> None:
        """Set initial focus patterns for new users (beginner-friendly patterns)."""
        beginner_patterns = [
            "Two Pointers",
            "Sliding Window",
            "Fast & Slow Pointers",
            "Tree Breadth First Search",
            "Modified Binary Search",
        ]
        self.session.current_focus_patterns = beginner_patterns
        self._save_session()

    def get_available_patterns(self) -> List[Pattern]:
        """Get all available patterns."""
        return self.patterns

    def get_pattern_details(self, pattern_name: str) -> Pattern:
        """Get detailed information about a specific pattern."""
        return get_pattern_by_name(pattern_name)

    def get_study_recommendations(self, limit: int = 3) -> List[str]:
        """Get recommended patterns to study next."""
        return self.session.get_suggested_next_patterns(limit)

    def start_study_session(self, pattern_name: str) -> Pattern:
        """Start studying a specific pattern."""
        pattern = get_pattern_by_name(pattern_name)
        print(f"\\n🎯 Starting study session: {pattern.name}")
        print(f"📝 {pattern.description}")
        print(f"\\n🔑 Key Concepts:")
        for concept in pattern.key_concepts:
            print(f"   • {concept}")

        if pattern.when_to_use:
            print(f"\\n🎪 When to use: {pattern.when_to_use}")

        if pattern.time_complexity_notes:
            print(f"\\n⏱️ Time Complexity: {pattern.time_complexity_notes}")

        if pattern.space_complexity_notes:
            print(f"🗂️ Space Complexity: {pattern.space_complexity_notes}")

        return pattern

    def complete_study_session(
        self,
        pattern_name: str,
        problems_completed: int,
        time_spent: int,
        difficulty_reached: str,
        notes: str = "",
    ) -> None:
        """Record completion of a study session."""
        pattern = get_pattern_by_name(pattern_name)

        record = StudyRecord(
            pattern_name=pattern_name,
            category=pattern.category,
            studied_at=datetime.now(),
            problems_completed=problems_completed,
            time_spent_minutes=time_spent,
            difficulty_reached=difficulty_reached,
            notes=notes,
        )

        self.session.add_study_record(record)
        self._save_session()

        print(f"\\n✅ Study session completed!")
        print(f"📊 Problems completed: {problems_completed}")
        print(f"⏰ Time spent: {time_spent} minutes")
        print(f"🎯 Difficulty reached: {difficulty_reached}")

        mastery = self.session.get_pattern_mastery_level(pattern_name)
        print(f"📈 Current mastery level: {mastery}%")

    def get_progress_summary(self) -> dict:
        """Get comprehensive progress summary."""
        total_patterns = len(self.patterns)
        studied_patterns = len(self.session.patterns_studied)

        mastery_levels = {}
        for pattern in self.patterns:
            mastery_levels[pattern.name] = self.session.get_pattern_mastery_level(
                pattern.name
            )

        avg_mastery = (
            sum(mastery_levels.values()) / len(mastery_levels) if mastery_levels else 0
        )

        weak_patterns = self.session.get_weak_patterns()
        recent_studies = self.session.get_recent_studies()

        return {
            "total_study_time": self.session.total_study_time,
            "total_patterns": total_patterns,
            "patterns_studied": studied_patterns,
            "average_mastery": round(avg_mastery, 1),
            "mastery_levels": mastery_levels,
            "weak_patterns": weak_patterns,
            "recent_studies_count": len(recent_studies),
            "current_focus": self.session.current_focus_patterns,
        }

    def set_focus_patterns(self, pattern_names: List[str]) -> None:
        """Set current focus patterns for concentrated study."""
        # Validate all patterns exist
        available_names = [p.name for p in self.patterns]
        invalid_patterns = [
            name for name in pattern_names if name not in available_names
        ]

        if invalid_patterns:
            raise ValueError(f"Invalid patterns: {invalid_patterns}")

        self.session.current_focus_patterns = pattern_names
        self._save_session()
        print(f"\\n🎯 Focus patterns updated: {', '.join(pattern_names)}")

    def show_pattern_problems(self, pattern_name: str, difficulty: str = None) -> None:
        """Show problems for a specific pattern, optionally filtered by difficulty."""
        pattern = get_pattern_by_name(pattern_name)

        print(f"\\n📚 Problems for {pattern.name}:")
        problems = pattern.problems

        if difficulty:
            from .pattern import Difficulty

            diff_enum = Difficulty(difficulty.lower())
            problems = pattern.get_problems_by_difficulty(diff_enum)

        if not problems:
            print("   No problems available for this pattern/difficulty.")
            return

        for i, problem in enumerate(problems, 1):
            print(f"\\n{i}. {problem.name} ({problem.difficulty.value.title()})")
            print(f"   📝 {problem.description}")

            if problem.key_insights:
                print("   💡 Key Insights:")
                for insight in problem.key_insights:
                    print(f"      • {insight}")

            if problem.leetcode_url:
                print(f"   🔗 LeetCode: {problem.leetcode_url}")

    def get_next_problem_suggestion(self, pattern_name: str) -> Optional[str]:
        """Get next recommended problem for a pattern based on mastery level."""
        pattern = get_pattern_by_name(pattern_name)
        mastery = self.session.get_pattern_mastery_level(pattern_name)

        problems = pattern.get_progression_problems()
        if not problems:
            return None

        # Suggest problems based on mastery level
        if mastery < 40:  # Beginner
            easy_problems = pattern.get_problems_by_difficulty("easy")
            return easy_problems[0].name if easy_problems else problems[0].name
        elif mastery < 80:  # Intermediate
            medium_problems = pattern.get_problems_by_difficulty("medium")
            return medium_problems[0].name if medium_problems else None
        else:  # Advanced
            hard_problems = pattern.get_problems_by_difficulty("hard")
            return hard_problems[0].name if hard_problems else None
