"""Database models for CB Algorithm Tutor."""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel

Base = declarative_base()


class User(Base):
    """User model for tracking learner progress."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    current_curriculum_id = Column(Integer)
    settings = Column(JSON, default={})


class Curriculum(Base):
    """Curriculum model for organizing learning materials."""
    
    __tablename__ = "curricula"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    topics = Column(JSON)  # List of algorithm topics/patterns
    difficulty_level = Column(String(20))  # beginner, intermediate, advanced
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class Session(Base):
    """Learning session model."""
    
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    curriculum_id = Column(Integer)
    topic = Column(String(100))
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime)
    duration_minutes = Column(Integer)
    problems_attempted = Column(Integer, default=0)
    problems_solved = Column(Integer, default=0)
    feedback_score = Column(Float)  # Overall session quality score


class Problem(Base):
    """Algorithm problem model."""
    
    __tablename__ = "problems"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String(20))  # easy, medium, hard
    category = Column(String(50))  # array, tree, graph, etc.
    patterns = Column(JSON)  # List of algorithm patterns
    solution_template = Column(Text)
    test_cases = Column(JSON)
    hints = Column(JSON)  # Progressive hints
    created_at = Column(DateTime, default=datetime.utcnow)


class Attempt(Base):
    """User attempt at solving a problem."""
    
    __tablename__ = "attempts"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    problem_id = Column(Integer, nullable=False)
    session_id = Column(Integer)
    code = Column(Text)
    language = Column(String(20), default="python")
    status = Column(String(20))  # attempted, solved, needs_help
    feedback = Column(JSON)  # LLM feedback and suggestions
    patterns_recognized = Column(JSON)  # Identified algorithm patterns
    time_spent_minutes = Column(Integer)
    attempted_at = Column(DateTime, default=datetime.utcnow)


# Pydantic models for API/data validation
class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None


class CurriculumCreate(BaseModel):
    name: str
    description: Optional[str] = None
    topics: list[str]
    difficulty_level: str


class ProblemCreate(BaseModel):
    title: str
    description: str
    difficulty: str
    category: str
    patterns: list[str]
    solution_template: str
    test_cases: list[Dict[str, Any]]
    hints: list[str]


class AttemptCreate(BaseModel):
    problem_id: int
    code: str
    language: str = "python"
