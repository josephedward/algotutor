"""Database service for CB Algorithm Tutor."""

from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from algotutor.core.config import settings
from algotutor.models import Base, User, Curriculum, Session as LearningSession, Problem, Attempt


class DatabaseService:
    """Service for database operations."""
    
    def __init__(self):
        self.engine = create_engine(settings.database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
    def create_tables(self):
        """Create database tables."""
        Base.metadata.create_all(bind=self.engine)
        
    def get_session(self) -> Session:
        """Get database session."""
        return self.SessionLocal()
        
    # User operations
    def create_user(self, username: str, email: Optional[str] = None) -> User:
        """Create a new user."""
        with self.get_session() as session:
            user = User(username=username, email=email)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
            
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        with self.get_session() as session:
            return session.query(User).filter(User.id == user_id).first()
            
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        with self.get_session() as session:
            return session.query(User).filter(User.username == username).first()
    
    # Curriculum operations
    def create_curriculum(self, name: str, description: str, topics: List[str], 
                         difficulty_level: str) -> Curriculum:
        """Create a new curriculum."""
        with self.get_session() as session:
            curriculum = Curriculum(
                name=name,
                description=description,
                topics=topics,
                difficulty_level=difficulty_level
            )
            session.add(curriculum)
            session.commit()
            session.refresh(curriculum)
            return curriculum
            
    def get_curriculum(self, curriculum_id: int) -> Optional[Curriculum]:
        """Get curriculum by ID."""
        with self.get_session() as session:
            return session.query(Curriculum).filter(Curriculum.id == curriculum_id).first()
            
    def list_curricula(self) -> List[Curriculum]:
        """List all active curricula."""
        with self.get_session() as session:
            return session.query(Curriculum).filter(Curriculum.is_active == True).all()
    
    # Problem operations
    def create_problem(self, title: str, description: str, difficulty: str,
                      category: str, patterns: List[str], solution_template: str,
                      test_cases: list, hints: List[str]) -> Problem:
        """Create a new problem."""
        with self.get_session() as session:
            problem = Problem(
                title=title,
                description=description,
                difficulty=difficulty,
                category=category,
                patterns=patterns,
                solution_template=solution_template,
                test_cases=test_cases,
                hints=hints
            )
            session.add(problem)
            session.commit()
            session.refresh(problem)
            return problem
            
    def get_problem(self, problem_id: int) -> Optional[Problem]:
        """Get problem by ID."""
        with self.get_session() as session:
            return session.query(Problem).filter(Problem.id == problem_id).first()
            
    def get_problems_by_category(self, category: str) -> List[Problem]:
        """Get problems by category."""
        with self.get_session() as session:
            return session.query(Problem).filter(Problem.category == category).all()

    def list_problem_categories(self) -> List[str]:
        """List distinct categories that have problems."""
        with self.get_session() as session:
            rows = session.query(Problem.category).distinct().all()
            return [r[0] for r in rows if r and r[0]]

    def get_all_problems(self) -> List[Problem]:
        """Get all problems, ordered by category and title."""
        with self.get_session() as session:
            return session.query(Problem).order_by(Problem.category, Problem.title).all()

    def get_solved_problem_ids(self, user_id: int) -> List[int]:
        """Get IDs of all problems solved by a user."""
        with self.get_session() as session:
            solved_attempts = session.query(Attempt.problem_id).filter(
                Attempt.user_id == user_id,
                Attempt.status == "solved"
            ).distinct().all()
            return [problem_id for problem_id, in solved_attempts]
    
    # Attempt operations
    def create_attempt(self, user_id: int, problem_id: int, code: str,
                      language: str = "python", session_id: Optional[int] = None) -> Attempt:
        """Create a new attempt."""
        with self.get_session() as session:
            attempt = Attempt(
                user_id=user_id,
                problem_id=problem_id,
                session_id=session_id,
                code=code,
                language=language,
                status="attempted"
            )
            session.add(attempt)
            session.commit()
            session.refresh(attempt)
            return attempt
            
    def update_attempt(self, attempt_id: int, **kwargs) -> Optional[Attempt]:
        """Update an attempt."""
        with self.get_session() as session:
            attempt = session.query(Attempt).filter(Attempt.id == attempt_id).first()
            if attempt:
                for key, value in kwargs.items():
                    setattr(attempt, key, value)
                session.commit()
                session.refresh(attempt)
            return attempt


# Global database service instance
db_service = DatabaseService()
