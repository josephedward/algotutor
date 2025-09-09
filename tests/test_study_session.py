"""
Tests for the StudySession functionality.
"""

from datetime import datetime, timedelta



from algorithm_tutor.pattern import PatternCategory
from algorithm_tutor.study_session import StudyRecord, StudySession


def test_study_session_creation():
    """Test creating a new study session."""
    session = StudySession(user_id="test_user")

    assert session.user_id == "test_user"
    assert session.total_study_time == 0
    assert len(session.patterns_studied) == 0
    assert len(session.study_records) == 0


def test_adding_study_record():
    """Test adding a study record to session."""
    session = StudySession()

    record = StudyRecord(
        pattern_name="Two Pointers",
        category=PatternCategory.TWO_POINTERS,
        studied_at=datetime.now(),
        problems_completed=3,
        time_spent_minutes=45,
        difficulty_reached="medium",
    )

    session.add_study_record(record)

    assert session.total_study_time == 45
    assert session.patterns_studied["Two Pointers"] == 1
    assert len(session.study_records) == 1


def test_mastery_level_calculation():
    """Test mastery level calculation."""
    session = StudySession()

    # Add multiple study records for same pattern
    for i in range(3):
        record = StudyRecord(
            pattern_name="Two Pointers",
            category=PatternCategory.TWO_POINTERS,
            studied_at=datetime.now(),
            problems_completed=2,
            time_spent_minutes=30,
            difficulty_reached="easy",
        )
        session.add_study_record(record)

    mastery = session.get_pattern_mastery_level("Two Pointers")
    assert mastery == 60  # 3 studies * 20 points each


def test_mastery_level_max_cap():
    """Test mastery level is capped at 100."""
    session = StudySession()

    # Add many study records
    for i in range(10):
        record = StudyRecord(
            pattern_name="Arrays",
            category=PatternCategory.ARRAYS,
            studied_at=datetime.now(),
            problems_completed=1,
            time_spent_minutes=20,
            difficulty_reached="easy",
        )
        session.add_study_record(record)

    mastery = session.get_pattern_mastery_level("Arrays")
    assert mastery == 100  # Should be capped at 100


def test_weak_patterns_identification():
    """Test identifying weak patterns."""
    session = StudySession()

    # Add records for different patterns with different mastery levels
    patterns_data = [
        ("Strong Pattern", 5),  # 100% mastery
        ("Weak Pattern", 1),  # 20% mastery
        ("Medium Pattern", 3),  # 60% mastery
    ]

    for pattern_name, study_count in patterns_data:
        for i in range(study_count):
            record = StudyRecord(
                pattern_name=pattern_name,
                category=PatternCategory.ARRAYS,
                studied_at=datetime.now(),
                problems_completed=1,
                time_spent_minutes=30,
                difficulty_reached="easy",
            )
            session.add_study_record(record)

    weak_patterns = session.get_weak_patterns(threshold=40)
    assert "Weak Pattern" in weak_patterns
    assert "Strong Pattern" not in weak_patterns
    assert "Medium Pattern" not in weak_patterns


def test_recent_studies_filtering():
    """Test filtering studies by recency."""
    session = StudySession()

    # Add old record
    old_record = StudyRecord(
        pattern_name="Old Pattern",
        category=PatternCategory.ARRAYS,
        studied_at=datetime.now() - timedelta(days=10),
        problems_completed=1,
        time_spent_minutes=30,
        difficulty_reached="easy",
    )
    session.add_study_record(old_record)

    # Add recent record
    recent_record = StudyRecord(
        pattern_name="Recent Pattern",
        category=PatternCategory.ARRAYS,
        studied_at=datetime.now() - timedelta(days=2),
        problems_completed=1,
        time_spent_minutes=30,
        difficulty_reached="easy",
    )
    session.add_study_record(recent_record)

    recent_studies = session.get_recent_studies(days=7)
    assert len(recent_studies) == 1
    assert recent_studies[0].pattern_name == "Recent Pattern"


def test_spaced_repetition_logic():
    """Test spaced repetition review timing."""
    session = StudySession()

    # Pattern never studied should need review
    assert session.should_review_pattern("Never Studied")

    # Pattern studied once, 2 days ago (should need review after 1 day)
    old_record = StudyRecord(
        pattern_name="Test Pattern",
        category=PatternCategory.ARRAYS,
        studied_at=datetime.now() - timedelta(days=2),
        problems_completed=1,
        time_spent_minutes=30,
        difficulty_reached="easy",
    )
    session.add_study_record(old_record)

    assert session.should_review_pattern("Test Pattern")

    # Pattern studied recently (same day) should not need review yet
    recent_record = StudyRecord(
        pattern_name="Recent Pattern",
        category=PatternCategory.ARRAYS,
        studied_at=datetime.now(),
        problems_completed=1,
        time_spent_minutes=30,
        difficulty_reached="easy",
    )
    session.add_study_record(recent_record)

    assert not session.should_review_pattern("Recent Pattern")


def test_study_suggestions():
    """Test study suggestions based on progress."""
    session = StudySession()
    session.current_focus_patterns = ["Pattern A", "Pattern B"]

    # Add some study records
    record_a = StudyRecord(
        pattern_name="Pattern A",
        category=PatternCategory.ARRAYS,
        studied_at=datetime.now() - timedelta(days=2),
        problems_completed=1,
        time_spent_minutes=30,
        difficulty_reached="easy",
    )
    session.add_study_record(record_a)

    suggestions = session.get_suggested_next_patterns(limit=2)

    # Should suggest Pattern A for review (studied 2 days ago)
    # and Pattern B for new study
    assert len(suggestions) <= 2
    assert "Pattern A" in suggestions or "Pattern B" in suggestions
