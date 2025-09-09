"""
Tests for the Pattern model and related functionality.
"""



from algorithm_tutor.pattern import Difficulty, Pattern, PatternCategory, Problem


def test_problem_creation():
    """Test creating a Problem instance."""
    problem = Problem(
        name="Two Sum",
        description="Find two numbers that add up to target",
        difficulty=Difficulty.EASY,
        key_insights=["Use hash map", "One pass solution"],
    )

    assert problem.name == "Two Sum"
    assert problem.difficulty == Difficulty.EASY
    assert len(problem.key_insights) == 2


def test_pattern_creation():
    """Test creating a Pattern instance."""
    problems = [
        Problem(name="Two Sum", description="Test problem", difficulty=Difficulty.EASY),
        Problem(name="3Sum", description="Test problem", difficulty=Difficulty.MEDIUM),
    ]

    pattern = Pattern(
        name="Two Pointers",
        category=PatternCategory.TWO_POINTERS,
        description="Use two pointers technique",
        key_concepts=["Left and right pointers", "Same direction pointers"],
        problems=problems,
    )

    assert pattern.name == "Two Pointers"
    assert pattern.category == PatternCategory.TWO_POINTERS
    assert len(pattern.problems) == 2


def test_pattern_problem_filtering():
    """Test filtering problems by difficulty."""
    problems = [
        Problem(name="Easy1", description="Test", difficulty=Difficulty.EASY),
        Problem(name="Easy2", description="Test", difficulty=Difficulty.EASY),
        Problem(name="Medium1", description="Test", difficulty=Difficulty.MEDIUM),
        Problem(name="Hard1", description="Test", difficulty=Difficulty.HARD),
    ]

    pattern = Pattern(
        name="Test Pattern",
        category=PatternCategory.ARRAYS,
        description="Test pattern",
        key_concepts=["Test"],
        problems=problems,
    )

    easy_problems = pattern.get_problems_by_difficulty(Difficulty.EASY)
    medium_problems = pattern.get_problems_by_difficulty(Difficulty.MEDIUM)
    hard_problems = pattern.get_problems_by_difficulty(Difficulty.HARD)

    assert len(easy_problems) == 2
    assert len(medium_problems) == 1
    assert len(hard_problems) == 1


def test_pattern_progression_order():
    """Test getting problems in progression order."""
    problems = [
        Problem(name="Hard1", description="Test", difficulty=Difficulty.HARD),
        Problem(name="Easy1", description="Test", difficulty=Difficulty.EASY),
        Problem(name="Medium1", description="Test", difficulty=Difficulty.MEDIUM),
        Problem(name="Easy2", description="Test", difficulty=Difficulty.EASY),
    ]

    pattern = Pattern(
        name="Test Pattern",
        category=PatternCategory.ARRAYS,
        description="Test pattern",
        key_concepts=["Test"],
        problems=problems,
    )

    progression = pattern.get_progression_problems()

    # Should be: Easy, Easy, Medium, Hard
    assert len(progression) == 4
    assert progression[0].difficulty == Difficulty.EASY
    assert progression[1].difficulty == Difficulty.EASY
    assert progression[2].difficulty == Difficulty.MEDIUM
    assert progression[3].difficulty == Difficulty.HARD
