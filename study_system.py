"""
Algorithm Tutor Study System

A minimal implementation of a study system for tracking student progress
in learning algorithms and data structures.
"""

import json
import datetime
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class StudySession:
    """Represents a single study session."""
    session_id: str
    start_time: str
    end_time: Optional[str] = None
    topics_covered: List[str] = None
    problems_attempted: int = 0
    problems_completed: int = 0
    performance_score: float = 0.0
    
    def __post_init__(self):
        if self.topics_covered is None:
            self.topics_covered = []


@dataclass
class StudentProgress:
    """Tracks overall student progress."""
    student_id: str
    topics_mastered: List[str] = None
    current_level: str = "beginner"
    total_study_time: int = 0  # minutes
    total_problems_solved: int = 0
    sessions: List[StudySession] = None
    last_active: Optional[str] = None
    
    def __post_init__(self):
        if self.topics_mastered is None:
            self.topics_mastered = []
        if self.sessions is None:
            self.sessions = []


class StudySystemManager:
    """Manages the overall study system functionality."""
    
    def __init__(self, data_dir: str = "study_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.progress_file = self.data_dir / "student_progress.json"
        self.topics_file = self.data_dir / "topics.json"
        
        # Load or initialize data
        self.student_progress = self._load_progress()
        self.topics = self._load_topics()
    
    def _load_progress(self) -> Dict[str, StudentProgress]:
        """Load student progress from storage."""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                data = json.load(f)
                return {
                    student_id: StudentProgress(**progress_data)
                    for student_id, progress_data in data.items()
                }
        return {}
    
    def _save_progress(self):
        """Save student progress to storage."""
        data = {
            student_id: asdict(progress)
            for student_id, progress in self.student_progress.items()
        }
        with open(self.progress_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_topics(self) -> Dict[str, Dict]:
        """Load topic structure from storage."""
        if self.topics_file.exists():
            with open(self.topics_file, 'r') as f:
                return json.load(f)
        return self._get_default_topics()
    
    def _get_default_topics(self) -> Dict[str, Dict]:
        """Return default topic structure for algorithms."""
        return {
            "arrays": {
                "difficulty": "beginner",
                "prerequisites": [],
                "subtopics": ["traversal", "searching", "sorting"]
            },
            "linked_lists": {
                "difficulty": "beginner", 
                "prerequisites": [],
                "subtopics": ["singly_linked", "doubly_linked", "operations"]
            },
            "stacks_queues": {
                "difficulty": "beginner",
                "prerequisites": ["arrays"],
                "subtopics": ["stack_operations", "queue_operations", "applications"]
            },
            "binary_trees": {
                "difficulty": "intermediate",
                "prerequisites": ["linked_lists"],
                "subtopics": ["traversals", "binary_search_trees", "heap"]
            },
            "graphs": {
                "difficulty": "intermediate",
                "prerequisites": ["binary_trees"],
                "subtopics": ["representations", "traversals", "shortest_path"]
            },
            "dynamic_programming": {
                "difficulty": "advanced",
                "prerequisites": ["arrays", "binary_trees"],
                "subtopics": ["memoization", "tabulation", "optimization"]
            }
        }
    
    def start_study_session(self, student_id: str) -> str:
        """Start a new study session for a student."""
        if student_id not in self.student_progress:
            self.student_progress[student_id] = StudentProgress(student_id=student_id)
        
        session_id = f"{student_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        session = StudySession(
            session_id=session_id,
            start_time=datetime.datetime.now().isoformat()
        )
        
        self.student_progress[student_id].sessions.append(session)
        return session_id
    
    def end_study_session(self, student_id: str, session_id: str, 
                         topics_covered: List[str], problems_attempted: int, 
                         problems_completed: int):
        """End a study session and update progress."""
        if student_id not in self.student_progress:
            return
        
        # Find and update the session
        for session in self.student_progress[student_id].sessions:
            if session.session_id == session_id:
                session.end_time = datetime.datetime.now().isoformat()
                session.topics_covered = topics_covered
                session.problems_attempted = problems_attempted
                session.problems_completed = problems_completed
                session.performance_score = problems_completed / max(problems_attempted, 1)
                break
        
        # Update overall progress
        progress = self.student_progress[student_id]
        progress.total_problems_solved += problems_completed
        progress.last_active = datetime.datetime.now().isoformat()
        
        # Check for topic mastery
        for topic in topics_covered:
            if (topic not in progress.topics_mastered and 
                session.performance_score >= 0.8):  # 80% threshold
                progress.topics_mastered.append(topic)
        
        self._save_progress()
    
    def get_recommended_topics(self, student_id: str) -> List[str]:
        """Get recommended topics for a student based on their progress."""
        if student_id not in self.student_progress:
            return ["arrays"]  # Start with basics
        
        progress = self.student_progress[student_id]
        mastered = set(progress.topics_mastered)
        
        recommendations = []
        for topic, info in self.topics.items():
            if topic in mastered:
                continue
            
            # Check if prerequisites are met
            prereqs = set(info.get("prerequisites", []))
            if prereqs.issubset(mastered):
                recommendations.append(topic)
        
        return recommendations
    
    def get_student_statistics(self, student_id: str) -> Dict:
        """Get comprehensive statistics for a student."""
        if student_id not in self.student_progress:
            return {}
        
        progress = self.student_progress[student_id]
        return {
            "topics_mastered": len(progress.topics_mastered),
            "total_problems_solved": progress.total_problems_solved,
            "total_sessions": len(progress.sessions),
            "current_level": progress.current_level,
            "last_active": progress.last_active,
            "mastered_topics": progress.topics_mastered,
            "recommended_topics": self.get_recommended_topics(student_id)
        }


if __name__ == "__main__":
    # Example usage
    study_system = StudySystemManager()
    
    # Start a session
    session_id = study_system.start_study_session("student_001")
    print(f"Started session: {session_id}")
    
    # End the session with some progress
    study_system.end_study_session(
        "student_001", 
        session_id,
        ["arrays"], 
        5, 
        4
    )
    
    # Get statistics
    stats = study_system.get_student_statistics("student_001")
    print("Student statistics:", stats)