"""Simplified CB Algorithm Tutor - Core functionality without external dependencies."""

import json
import os
import sys
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import ast
import tempfile
import subprocess
import time


@dataclass
class Problem:
    id: int
    title: str
    description: str
    difficulty: str
    category: str
    patterns: List[str]
    solution_template: str
    test_cases: List[Dict[str, Any]]
    hints: List[str]


@dataclass
class User:
    username: str
    created_at: str
    problems_solved: int = 0
    current_streak: int = 0


@dataclass
class Attempt:
    user: str
    problem_id: int
    code: str
    timestamp: str
    status: str = "attempted"
    feedback: Dict[str, Any] = None


class SimpleStorage:
    """Simple JSON file-based storage."""
    
    def __init__(self, data_dir: str = "cb_data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
    def save_user(self, user: User):
        with open(f"{self.data_dir}/user_{user.username}.json", 'w') as f:
            json.dump(asdict(user), f, indent=2)
            
    def load_user(self, username: str) -> Optional[User]:
        try:
            with open(f"{self.data_dir}/user_{username}.json", 'r') as f:
                data = json.load(f)
                return User(**data)
        except FileNotFoundError:
            return None
    
    def save_attempt(self, attempt: Attempt):
        filename = f"{self.data_dir}/attempts_{attempt.user}.json"
        attempts = []
        try:
            with open(filename, 'r') as f:
                attempts = json.load(f)
        except FileNotFoundError:
            pass
        
        attempts.append(asdict(attempt))
        with open(filename, 'w') as f:
            json.dump(attempts, f, indent=2)


class SimpleCodeExecutor:
    """Simple code execution without external dependencies."""
    
    def execute_python_code(self, code: str, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        results = {
            "success": False,
            "output": "",
            "errors": "",
            "test_results": [],
            "syntax_valid": False
        }
        
        # Check syntax
        try:
            ast.parse(code)
            results["syntax_valid"] = True
        except SyntaxError as e:
            results["errors"] = f"Syntax Error: {str(e)}"
            return results
        
        # Execute code
        try:
            exec_globals = {"__builtins__": __builtins__}
            exec_locals = {}
            exec(code, exec_globals, exec_locals)
            
            # Find the main function
            main_function = None
            for name, obj in exec_locals.items():
                if callable(obj) and not name.startswith('_'):
                    main_function = obj
                    break
            
            if main_function is None:
                results["errors"] = "No callable function found in code"
                return results
            
            # Run test cases
            passed_tests = 0
            for i, test_case in enumerate(test_cases):
                try:
                    input_args = test_case.get("input", [])
                    expected_output = test_case.get("expected", None)
                    
                    if isinstance(input_args, list) and len(input_args) > 0:
                        if isinstance(input_args[0], list):
                            actual_output = main_function(*input_args)
                        else:
                            actual_output = main_function(input_args)
                    else:
                        actual_output = main_function(input_args)
                    
                    test_passed = actual_output == expected_output
                    if test_passed:
                        passed_tests += 1
                    
                    results["test_results"].append({
                        "test_case": i + 1,
                        "input": input_args,
                        "expected": expected_output,
                        "actual": actual_output,
                        "passed": test_passed
                    })
                    
                except Exception as e:
                    results["test_results"].append({
                        "test_case": i + 1,
                        "input": input_args,
                        "expected": expected_output,
                        "actual": None,
                        "passed": False,
                        "error": str(e)
                    })
            
            results["success"] = passed_tests == len(test_cases)
            results["output"] = f"Passed {passed_tests}/{len(test_cases)} test cases"
            
        except Exception as e:
            results["errors"] = str(e)
        
        return results


class SimpleFeedbackGenerator:
    """Simple feedback generation without LLM."""
    
    def generate_socratic_question(self, code: str, problem: str) -> str:
        questions = [
            "What data structure might be most efficient for this problem?",
            "Can you identify the time complexity of your current approach?",
            "Are there any edge cases you haven't considered?",
            "Could you solve this with a different algorithm pattern?",
            "What's the space-time tradeoff in your solution?"
        ]
        return questions[hash(code) % len(questions)]
    
    def analyze_patterns(self, code: str) -> List[str]:
        patterns = []
        if "for" in code and "range" in code:
            patterns.append("iteration")
        if "while" in code:
            patterns.append("while_loop")
        if "def " in code and code.count("def ") > 1:
            patterns.append("recursion")
        if "[" in code and "]" in code:
            patterns.append("array_access")
        if "dict" in code or "{" in code:
            patterns.append("hash_table")
        return patterns
    
    def provide_feedback(self, code: str, results: Dict[str, Any]) -> str:
        if results["success"]:
            return "Great job! Your solution passes all test cases. Consider if you can optimize for time or space complexity."
        else:
            failed_tests = [t for t in results["test_results"] if not t["passed"]]
            if failed_tests:
                return f"Some test cases failed. Check test case {failed_tests[0]['test_case']}: expected {failed_tests[0]['expected']} but got {failed_tests[0]['actual']}"
            else:
                return "There seems to be an issue with your code logic. Review the problem requirements."


class CBAlgorithmTutor:
    """Main tutor application."""
    
    def __init__(self):
        self.storage = SimpleStorage()
        self.executor = SimpleCodeExecutor()
        self.feedback = SimpleFeedbackGenerator()
        self.sample_problems = self._create_sample_problems()
        
    def _create_sample_problems(self) -> List[Problem]:
        return [
            Problem(
                id=1,
                title="Two Sum",
                description="""Given an array of integers nums and an integer target, 
return indices of the two numbers such that they add up to target.

Example:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].""",
                difficulty="easy",
                category="Arrays",
                patterns=["hash_table", "two_pointer"],
                solution_template="""def twoSum(nums, target):
    # Your solution here
    pass""",
                test_cases=[
                    {"input": [[2, 7, 11, 15], 9], "expected": [0, 1]},
                    {"input": [[3, 2, 4], 6], "expected": [1, 2]},
                    {"input": [[3, 3], 6], "expected": [0, 1]}
                ],
                hints=[
                    "Consider what data structure can help you find complements efficiently",
                    "Hash maps provide O(1) lookup time",
                    "Store each number with its index as you iterate"
                ]
            ),
            Problem(
                id=2,
                title="Valid Parentheses",
                description="""Given a string s containing just the characters '(', ')', '{', '}', '[' and ']',
determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets
2. Open brackets must be closed in the correct order

Example:
Input: s = "()[]{}"
Output: true""",
                difficulty="easy",
                category="Stack",
                patterns=["stack"],
                solution_template="""def isValid(s):
    # Your solution here
    pass""",
                test_cases=[
                    {"input": ["()"], "expected": True},
                    {"input": ["()[]{})"], "expected": True},
                    {"input": ["(]"], "expected": False}
                ],
                hints=[
                    "Think about Last In, First Out (LIFO) data structure",
                    "Use a stack to keep track of opening brackets",
                    "Match closing brackets with the most recent opening bracket"
                ]
            )
        ]
    
    def start_session(self, username: str):
        """Start an interactive tutoring session."""
        print(f"\n🎯 Welcome to CB Algorithm Tutor, {username}!")
        print("=" * 50)
        
        user = self.storage.load_user(username)
        if not user:
            user = User(
                username=username,
                created_at=datetime.now().isoformat()
            )
            self.storage.save_user(user)
            print(f"Created new profile for {username}")
        
        while True:
            print("\nOptions:")
            print("1. Solve a problem")
            print("2. View progress")
            print("3. Quit")
            
            choice = input("Choose an option (1-3): ").strip()
            
            if choice == "1":
                self.solve_problem(user)
            elif choice == "2":
                self.show_progress(user)
            elif choice == "3":
                print("Happy learning! 👋")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def solve_problem(self, user: User):
        """Interactive problem solving."""
        print("\nAvailable Problems:")
        for i, problem in enumerate(self.sample_problems):
            print(f"{i + 1}. {problem.title} ({problem.difficulty})")
        
        try:
            choice = int(input("Choose a problem (1-2): ")) - 1
            if 0 <= choice < len(self.sample_problems):
                self.work_on_problem(user, self.sample_problems[choice])
            else:
                print("Invalid problem number.")
        except ValueError:
            print("Please enter a valid number.")
    
    def work_on_problem(self, user: User, problem: Problem):
        """Work on a specific problem."""
        print(f"\n{'=' * 60}")
        print(f"Problem: {problem.title}")
        print(f"Difficulty: {problem.difficulty} | Category: {problem.category}")
        print(f"Patterns: {', '.join(problem.patterns)}")
        print("=" * 60)
        print("\nDescription:")
        print(problem.description)
        print("\nStarting template:")
        print(problem.solution_template)
        print("=" * 60)
        
        hint_count = 0
        
        while True:
            print("\nOptions:")
            print("1. Write/Edit solution")
            print("2. Get hint")
            print("3. Submit solution")
            print("4. Back to main menu")
            
            choice = input("Choose an option (1-4): ").strip()
            
            if choice == "1":
                code = self.get_code_input()
                if code:
                    question = self.feedback.generate_socratic_question(code, problem.description)
                    print(f"\n🤔 Think about this: {question}")
                    
            elif choice == "2":
                if hint_count < len(problem.hints):
                    print(f"\n💡 Hint {hint_count + 1}: {problem.hints[hint_count]}")
                    hint_count += 1
                else:
                    print("No more hints available for this problem.")
                    
            elif choice == "3":
                if 'code' in locals():
                    self.submit_solution(user, problem, code)
                else:
                    print("Please write some code first!")
                    
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")
    
    def get_code_input(self) -> str:
        """Get code input from user."""
        print("\nEnter your solution (press Enter twice when done):")
        lines = []
        empty_lines = 0
        
        while empty_lines < 2:
            line = input(">>> " if not lines else "... ")
            if line.strip() == "":
                empty_lines += 1
            else:
                empty_lines = 0
            lines.append(line)
        
        # Remove trailing empty lines
        while lines and lines[-1].strip() == "":
            lines.pop()
        
        return "\n".join(lines)
    
    def submit_solution(self, user: User, problem: Problem, code: str):
        """Submit and evaluate solution."""
        print("\n⚡ Testing your solution...")
        
        results = self.executor.execute_python_code(code, problem.test_cases)
        
        # Display results
        if not results["syntax_valid"]:
            print(f"❌ Syntax Error: {results['errors']}")
        elif results["success"]:
            print("🎉 Congratulations! All test cases passed!")
            user.problems_solved += 1
            user.current_streak += 1
            self.storage.save_user(user)
        else:
            print(f"📊 Test Results: {results['output']}")
            print("\nDetailed Results:")
            for test in results["test_results"]:
                status = "✅" if test["passed"] else "❌"
                print(f"  {status} Test {test['test_case']}: input={test['input']}, expected={test['expected']}, got={test.get('actual', 'Error')}")
        
        # Provide feedback
        feedback_text = self.feedback.provide_feedback(code, results)
        patterns = self.feedback.analyze_patterns(code)
        
        print(f"\n📝 Feedback: {feedback_text}")
        if patterns:
            print(f"🔍 Patterns detected: {', '.join(patterns)}")
        
        # Save attempt
        attempt = Attempt(
            user=user.username,
            problem_id=problem.id,
            code=code,
            timestamp=datetime.now().isoformat(),
            status="solved" if results["success"] else "attempted",
            feedback=results
        )
        self.storage.save_attempt(attempt)
    
    def show_progress(self, user: User):
        """Show user progress."""
        print(f"\n📈 Progress for {user.username}")
        print("=" * 40)
        print(f"Problems solved: {user.problems_solved}")
        print(f"Current streak: {user.current_streak}")
        print(f"Member since: {user.created_at[:10]}")


def main():
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "--init":
        print("✅ CB Algorithm Tutor initialized!")
        print("Run: python simple_tutor.py")
        return
    
    tutor = CBAlgorithmTutor()
    
    username = input("Enter your username: ").strip()
    if username:
        tutor.start_session(username)
    else:
        print("Username cannot be empty!")


if __name__ == "__main__":
    main()