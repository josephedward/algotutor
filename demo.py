"""Demo script showcasing CB Algorithm Tutor functionality."""

from simple_tutor import CBAlgorithmTutor, User
from datetime import datetime


def demo_two_sum_solution():
    """Demonstrate solving the Two Sum problem."""
    print("🎯 CB Algorithm Tutor Demo")
    print("=" * 50)
    
    tutor = CBAlgorithmTutor()
    
    # Create demo user
    user = User(
        username="demo_user",
        created_at=datetime.now().isoformat()
    )
    
    # Get the Two Sum problem
    problem = tutor.sample_problems[0]  # Two Sum
    
    print(f"\nWorking on: {problem.title}")
    print(f"Difficulty: {problem.difficulty}")
    print(f"Category: {problem.category}")
    print(f"Patterns: {', '.join(problem.patterns)}")
    
    print(f"\nProblem Description:")
    print(problem.description)
    
    print(f"\nStarting template:")
    print(problem.solution_template)
    
    # Demo different solution attempts
    solutions = [
        {
            "name": "Brute Force Solution",
            "code": """def twoSum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []""",
            "explanation": "This is a brute force approach that checks every pair."
        },
        {
            "name": "Optimized Hash Map Solution", 
            "code": """def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []""",
            "explanation": "This optimized solution uses a hash map for O(n) time complexity."
        }
    ]
    
    for sol in solutions:
        print(f"\n" + "="*60)
        print(f"🧑‍💻 Trying: {sol['name']}")
        print("="*60)
        print(sol['explanation'])
        print("\nCode:")
        print(sol['code'])
        
        # Generate Socratic question
        question = tutor.feedback.generate_socratic_question(sol['code'], problem.description)
        print(f"\n🤔 Tutor asks: {question}")
        
        # Execute and get results
        results = tutor.executor.execute_python_code(sol['code'], problem.test_cases)
        
        print(f"\n⚡ Test Results:")
        if results["success"]:
            print("✅ All tests passed!")
        else:
            print(f"❌ {results['output']}")
            
        for test in results["test_results"]:
            status = "✅" if test["passed"] else "❌"
            print(f"  {status} Test {test['test_case']}: input={test['input']}, expected={test['expected']}, actual={test.get('actual', 'Error')}")
        
        # Analyze patterns
        patterns = tutor.feedback.analyze_patterns(sol['code'])
        if patterns:
            print(f"🔍 Algorithm patterns detected: {', '.join(patterns)}")
        
        # Get feedback
        feedback = tutor.feedback.provide_feedback(sol['code'], results)
        print(f"📝 Tutor feedback: {feedback}")
        
        # Save attempt
        from simple_tutor import Attempt
        attempt = Attempt(
            user=user.username,
            problem_id=problem.id,
            code=sol['code'],
            timestamp=datetime.now().isoformat(),
            status="solved" if results["success"] else "attempted",
            feedback=results
        )
        tutor.storage.save_attempt(attempt)


def demo_hint_system():
    """Demonstrate the progressive hint system."""
    print(f"\n" + "="*60)
    print("💡 Progressive Hint System Demo")
    print("="*60)
    
    tutor = CBAlgorithmTutor()
    problem = tutor.sample_problems[0]  # Two Sum
    
    print(f"Problem: {problem.title}")
    print("\nProgressive hints:")
    
    for i, hint in enumerate(problem.hints, 1):
        print(f"  Hint {i}: {hint}")
    
    print(f"\nThis system provides incremental guidance without giving away the solution!")


def demo_pattern_recognition():
    """Demonstrate algorithm pattern recognition."""
    print(f"\n" + "="*60)
    print("🔍 Algorithm Pattern Recognition Demo")  
    print("="*60)
    
    tutor = CBAlgorithmTutor()
    
    sample_codes = [
        ("Nested Loop Pattern", "for i in range(n):\n    for j in range(i+1, n):\n        process(i, j)"),
        ("Hash Table Pattern", "seen = {}\nfor item in items:\n    if item in seen:\n        return True\n    seen[item] = True"),
        ("Recursion Pattern", "def solve(n):\n    if n <= 1:\n        return n\n    return solve(n-1) + solve(n-2)"),
        ("Array Access Pattern", "result = []\nfor i in range(len(arr)):\n    result.append(arr[i] * 2)"),
    ]
    
    for name, code in sample_codes:
        patterns = tutor.feedback.analyze_patterns(code)
        print(f"\n{name}:")
        print(f"Code: {code.replace(chr(10), ' | ')}")
        print(f"Detected patterns: {', '.join(patterns) if patterns else 'None detected'}")


if __name__ == "__main__":
    demo_two_sum_solution()
    demo_hint_system()
    demo_pattern_recognition()
    
    print(f"\n" + "="*60)
    print("🎉 Demo Complete!")
    print("="*60)
    print("Key Features Demonstrated:")
    print("✅ Real-time code execution and testing")
    print("✅ Socratic questioning for guided learning")
    print("✅ Algorithm pattern recognition")
    print("✅ Progressive hint system")
    print("✅ Session persistence and progress tracking")
    print("✅ Line-by-line feedback and analysis")
    print("\nFor full LLM integration, add your OpenAI API key to the .env file!")