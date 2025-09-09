"""
Tests for the patterns database.
"""

import pytest

from algorithm_tutor.pattern import PatternCategory
from algorithm_tutor.patterns_db import (
    get_core_patterns,
    get_pattern_by_name,
    get_patterns_by_category,
)


def test_core_patterns_count():
    """Test that we have the expected number of core patterns."""
    patterns = get_core_patterns()

    # Should have around 10-15 core patterns (we have 10 implemented)
    assert len(patterns) >= 8
    assert len(patterns) <= 20


def test_all_patterns_have_required_fields():
    """Test that all patterns have the required fields populated."""
    patterns = get_core_patterns()

    for pattern in patterns:
        assert pattern.name
        assert pattern.description
        assert pattern.category
        assert len(pattern.key_concepts) > 0
        assert pattern.when_to_use
        assert pattern.time_complexity_notes
        assert pattern.space_complexity_notes


def test_patterns_have_problems():
    """Test that patterns have associated problems."""
    patterns = get_core_patterns()

    patterns_with_problems = [p for p in patterns if len(p.problems) > 0]

    # Most patterns should have at least some problems
    assert len(patterns_with_problems) >= len(patterns) * 0.8


def test_get_pattern_by_name():
    """Test retrieving specific pattern by name."""
    pattern = get_pattern_by_name("Two Pointers")

    assert pattern.name == "Two Pointers"
    assert pattern.category == PatternCategory.TWO_POINTERS
    assert len(pattern.key_concepts) > 0


def test_get_pattern_by_name_case_insensitive():
    """Test that pattern retrieval is case insensitive."""
    pattern1 = get_pattern_by_name("two pointers")
    pattern2 = get_pattern_by_name("TWO POINTERS")
    pattern3 = get_pattern_by_name("Two Pointers")

    assert pattern1.name == pattern2.name == pattern3.name


def test_get_pattern_by_name_not_found():
    """Test that invalid pattern name raises ValueError."""
    with pytest.raises(ValueError, match="Pattern 'Nonexistent' not found"):
        get_pattern_by_name("Nonexistent")


def test_get_patterns_by_category():
    """Test filtering patterns by category."""
    tree_patterns = get_patterns_by_category(PatternCategory.TREES)

    assert len(tree_patterns) > 0
    for pattern in tree_patterns:
        assert pattern.category == PatternCategory.TREES


def test_pattern_problems_have_valid_difficulties():
    """Test that all problems have valid difficulty levels."""
    patterns = get_core_patterns()

    valid_difficulties = ["easy", "medium", "hard"]

    for pattern in patterns:
        for problem in pattern.problems:
            assert problem.difficulty.value in valid_difficulties


def test_pattern_coverage_categories():
    """Test that we cover essential algorithmic categories."""
    patterns = get_core_patterns()
    categories = {p.category for p in patterns}

    # Should cover essential categories
    essential_categories = {
        PatternCategory.TWO_POINTERS,
        PatternCategory.SLIDING_WINDOW,
        PatternCategory.TREES,
        PatternCategory.ARRAYS,
        PatternCategory.BINARY_SEARCH,
    }

    assert essential_categories.issubset(categories)
