"""
Tests for the Study System functionality
"""

import os
import json
import tempfile
import shutil
from study_system import StudySystemManager, StudentProgress, StudySession


def test_study_system_basic_functionality():
    """Test basic study system operations."""
    # Create temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Initialize study system
        study_system = StudySystemManager(data_dir=temp_dir)
        
        # Test starting a session
        student_id = "test_student"
        session_id = study_system.start_study_session(student_id)
        assert session_id is not None
        assert student_id in study_system.student_progress
        
        # Test ending a session
        study_system.end_study_session(
            student_id, 
            session_id,
            ["arrays"], 
            5, 
            4
        )
        
        # Verify progress was recorded
        progress = study_system.student_progress[student_id]
        assert progress.total_problems_solved == 4
        assert len(progress.sessions) == 1
        assert progress.sessions[0].problems_completed == 4
        assert progress.sessions[0].performance_score == 0.8
        
        # Test topic mastery (should be mastered with 80% score)
        assert "arrays" in progress.topics_mastered
        
        # Test recommendations
        recommendations = study_system.get_recommended_topics(student_id)
        assert "linked_lists" in recommendations  # No prerequisites
        assert "stacks_queues" in recommendations  # Prerequisites met (arrays)
        assert "binary_trees" not in recommendations  # Prerequisites not met
        
        # Test statistics
        stats = study_system.get_student_statistics(student_id)
        assert stats["topics_mastered"] == 1
        assert stats["total_problems_solved"] == 4
        assert stats["total_sessions"] == 1
        
        print("✓ All basic functionality tests passed!")
        
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)


def test_persistence():
    """Test that data persists across system restarts."""
    temp_dir = tempfile.mkdtemp()
    
    try:
        # First system instance - create some data
        system1 = StudySystemManager(data_dir=temp_dir)
        session_id = system1.start_study_session("persistent_student")
        system1.end_study_session("persistent_student", session_id, ["arrays"], 3, 3)
        
        # Second system instance - should load existing data
        system2 = StudySystemManager(data_dir=temp_dir)
        assert "persistent_student" in system2.student_progress
        stats = system2.get_student_statistics("persistent_student")
        assert stats["total_problems_solved"] == 3
        
        print("✓ Data persistence test passed!")
        
    finally:
        shutil.rmtree(temp_dir)


def test_topic_progression():
    """Test that topic recommendations follow prerequisite requirements."""
    temp_dir = tempfile.mkdtemp()
    
    try:
        study_system = StudySystemManager(data_dir=temp_dir)
        student_id = "progression_student"
        
        # Start with arrays
        session1 = study_system.start_study_session(student_id)
        study_system.end_study_session(student_id, session1, ["arrays"], 5, 5)
        
        # Check recommendations after mastering arrays
        recommendations = study_system.get_recommended_topics(student_id)
        assert "linked_lists" in recommendations
        assert "stacks_queues" in recommendations  # arrays is prerequisite
        
        # Master linked_lists
        session2 = study_system.start_study_session(student_id)
        study_system.end_study_session(student_id, session2, ["linked_lists"], 4, 4)
        
        # Now binary_trees should be recommended
        recommendations = study_system.get_recommended_topics(student_id)
        assert "binary_trees" in recommendations  # linked_lists is prerequisite
        
        print("✓ Topic progression test passed!")
        
    finally:
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    test_study_system_basic_functionality()
    test_persistence()
    test_topic_progression()
    print("\n✅ All tests passed successfully!")