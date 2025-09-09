"""Curriculum management service."""

from typing import Dict, List, Any, Optional
from cb.services.database import db_service
from cb.models import Curriculum, Problem


class CurriculumService:
    """Service for managing learning curricula."""
    
    def __init__(self):
        self.db = db_service
        
    def create_default_curriculum(self) -> Curriculum:
        """Create a default algorithm curriculum."""
        topics = [
            "Arrays and Strings",
            "Two Pointers",
            "Sliding Window",
            "Hash Tables",
            "Linked Lists",
            "Stacks and Queues",
            "Binary Search",
            "Sorting Algorithms",
            "Binary Trees",
            "Binary Search Trees",
            "Tree Traversal",
            "Heaps",
            "Graphs - BFS/DFS",
            "Dynamic Programming",
            "Backtracking",
            "Greedy Algorithms"
        ]
        
        return self.db.create_curriculum(
            name="Complete Algorithm Mastery",
            description="Comprehensive algorithm curriculum covering all essential patterns",
            topics=topics,
            difficulty_level="progressive"
        )
    
    def create_sample_problems(self) -> List[Problem]:
        """Create sample problems for the curriculum."""
        sample_problems = [
            {
                "title": "Two Sum",
                "description": """Given an array of integers nums and an integer target, 
                return indices of the two numbers such that they add up to target.
                
                You may assume that each input would have exactly one solution, 
                and you may not use the same element twice.
                
                Example:
                Input: nums = [2,7,11,15], target = 9
                Output: [0,1]
                Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].""",
                "difficulty": "easy",
                "category": "Arrays and Strings",
                "patterns": ["hash_table", "two_pointer"],
                "solution_template": """def twoSum(nums, target):
    # Your solution here
    pass""",
                "test_cases": [
                    {"input": [[2, 7, 11, 15], 9], "expected": [0, 1]},
                    {"input": [[3, 2, 4], 6], "expected": [1, 2]},
                    {"input": [[3, 3], 6], "expected": [0, 1]}
                ],
                "hints": [
                    "Think about what data structure can help you find complements efficiently",
                    "Consider using a hash map to store values and their indices",
                    "For each number, check if target - number exists in your hash map"
                ]
            },
            {
                "title": "Valid Parentheses",
                "description": """Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', 
                determine if the input string is valid.
                
                An input string is valid if:
                1. Open brackets must be closed by the same type of brackets
                2. Open brackets must be closed in the correct order
                
                Example:
                Input: s = "()[]{}"
                Output: true""",
                "difficulty": "easy",
                "category": "Stacks and Queues",
                "patterns": ["stack"],
                "solution_template": """def isValid(s):
    # Your solution here
    pass""",
                "test_cases": [
                    {"input": ["()"], "expected": True},
                    {"input": ["()[]{})"], "expected": True},
                    {"input": ["(]"], "expected": False},
                    {"input": ["([)]"], "expected": False}
                ],
                "hints": [
                    "Think about Last In, First Out (LIFO) data structure",
                    "Use a stack to keep track of opening brackets",
                    "When you see a closing bracket, check if it matches the most recent opening bracket"
                ]
            },
            {
                "title": "Maximum Subarray",
                "description": """Given an integer array nums, find the contiguous subarray 
                (containing at least one number) which has the largest sum and return its sum.
                
                Example:
                Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
                Output: 6
                Explanation: [4,-1,2,1] has the largest sum = 6.""",
                "difficulty": "medium",
                "category": "Dynamic Programming",
                "patterns": ["dynamic_programming", "kadanes_algorithm"],
                "solution_template": """def maxSubArray(nums):
    # Your solution here
    pass""",
                "test_cases": [
                    {"input": [[-2,1,-3,4,-1,2,1,-5,4]], "expected": 6},
                    {"input": [[1]], "expected": 1},
                    {"input": [[5,4,-1,7,8]], "expected": 23}
                ],
                "hints": [
                    "Consider Kadane's algorithm for this classic problem",
                    "At each position, decide whether to extend the current subarray or start a new one",
                    "Keep track of the maximum sum seen so far"
                ]
            }
        ]
        
        problems = []
        for problem_data in sample_problems:
            problem = self.db.create_problem(**problem_data)
            problems.append(problem)
            
        return problems
    
    def get_next_topic(self, user_id: int, curriculum_id: int) -> Optional[str]:
        """Get the next topic for a user based on their progress."""
        curriculum = self.db.get_curriculum(curriculum_id)
        if not curriculum:
            return None
            
        # Simple progression - return first topic for now
        # In a real implementation, this would track user progress
        return curriculum.topics[0] if curriculum.topics else None
    
    def get_problems_for_topic(self, topic: str, difficulty: str = None) -> List[Problem]:
        """Get problems for a specific topic."""
        problems = self.db.get_problems_by_category(topic)
        
        if difficulty:
            problems = [p for p in problems if p.difficulty == difficulty]
            
        return problems
    
    def initialize_default_data(self):
        """Initialize the database with default curriculum and problems."""
        # Check if we already have data
        curricula = self.db.list_curricula()
        if curricula:
            return  # Already initialized
            
        # Create default curriculum
        curriculum = self.create_default_curriculum()
        
        # Create sample problems
        problems = self.create_sample_problems()
        
        print(f"Initialized curriculum '{curriculum.name}' with {len(problems)} sample problems")


# Global curriculum service instance
curriculum_service = CurriculumService()