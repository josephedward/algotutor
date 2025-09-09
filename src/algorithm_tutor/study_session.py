"""
Study session management for tracking learning progress.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

from pydantic import BaseModel

from .pattern import PatternCategory


class StudyRecord(BaseModel):
    """Record of studying a specific pattern."""

    pattern_name: str
    category: PatternCategory
    studied_at: datetime
    problems_completed: int
    time_spent_minutes: int
    difficulty_reached: str  # "easy", "medium", "hard"
    notes: str = ""


class StudySession(BaseModel):
    """Manages study sessions and progress tracking."""

    user_id: str = "default"
    created_at: datetime = datetime.now()
    total_study_time: int = 0  # total minutes
    patterns_studied: Dict[str, int] = {}  # pattern_name -> times_studied
    study_records: List[StudyRecord] = []
    current_focus_patterns: List[str] = []  # patterns to focus on

    def add_study_record(self, record: StudyRecord) -> None:
        """Add a study record and update session stats."""
        self.study_records.append(record)
        self.total_study_time += record.time_spent_minutes

        # Update pattern study count
        if record.pattern_name not in self.patterns_studied:
            self.patterns_studied[record.pattern_name] = 0
        self.patterns_studied[record.pattern_name] += 1

    def get_recent_studies(self, days: int = 7) -> List[StudyRecord]:
        """Get study records from the last N days."""
        cutoff_date = datetime.now() - timedelta(days=days)
        return [r for r in self.study_records if r.studied_at >= cutoff_date]

    def get_pattern_mastery_level(self, pattern_name: str) -> int:
        """Get mastery level (0-100) for a pattern based on study frequency."""
        studies = self.patterns_studied.get(pattern_name, 0)
        # Simple mastery calculation: every 3 studies = +20 points, max 100
        return min(100, studies * 20)

    def get_weak_patterns(self, threshold: int = 40) -> List[str]:
        """Get patterns below mastery threshold that need more focus."""
        weak = []
        for pattern_name, studies in self.patterns_studied.items():
            mastery = self.get_pattern_mastery_level(pattern_name)
            if mastery < threshold:
                weak.append(pattern_name)
        return weak

    def should_review_pattern(self, pattern_name: str) -> bool:
        """Determine if pattern needs review based on spaced repetition."""
        if pattern_name not in self.patterns_studied:
            return True

        # Get last study of this pattern
        recent_studies = [
            r for r in self.study_records if r.pattern_name == pattern_name
        ]
        if not recent_studies:
            return True

        last_study = max(recent_studies, key=lambda r: r.studied_at)
        studies_count = self.patterns_studied[pattern_name]

        # Spaced repetition intervals: 1 day, 3 days, 7 days, 14 days
        intervals = [1, 3, 7, 14]
        interval_index = min(studies_count - 1, len(intervals) - 1)
        review_interval = intervals[interval_index]

        days_since_last = (datetime.now() - last_study.studied_at).days
        return days_since_last >= review_interval

    def get_suggested_next_patterns(self, limit: int = 3) -> List[str]:
        """Get suggested patterns to study next based on progress and spaced repetition."""
        suggestions = []

        # First priority: patterns that need review
        for pattern_name in self.patterns_studied:
            if self.should_review_pattern(pattern_name) and len(suggestions) < limit:
                suggestions.append(pattern_name)

        # Second priority: focus patterns not yet studied enough
        for pattern_name in self.current_focus_patterns:
            if pattern_name not in suggestions and len(suggestions) < limit:
                if self.get_pattern_mastery_level(pattern_name) < 80:
                    suggestions.append(pattern_name)

        return suggestions
