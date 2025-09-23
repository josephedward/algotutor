# AlgoTutor 🎯

An AI-powered algorithm tutor that provides personalized learning with accountability, persistence, and real-time feedback. Think LeetCode + OpenAI Study Mode but with Socratic questioning, line-by-line feedback, and structured pattern recognition.

## Features ✨

- **🤖 LLM-Powered Guidance**: Uses OpenAI GPT-4 for Socratic questioning and personalized feedback
- **📚 Structured Curriculum**: Progressive learning path covering all essential algorithm patterns
- **💾 Session Persistence**: Your progress and learning sessions are saved and tracked
- **⚡ Real-time Code Execution**: Execute and test your solutions instantly with detailed feedback
- **🎯 Pattern Recognition**: Automatically identifies algorithm patterns in your code
- **📝 Line-by-line Feedback**: Detailed analysis of your solution with suggestions for improvement
- **🔄 Quality over Quantity**: Focus on deep understanding rather than solving many problems
- **❓ Progressive Hints**: Get hints that guide your thinking without giving away solutions

## Installation 🚀

1. **Clone the repository**:
```bash
git clone <your fork or this repo>
cd algotutor
```

2. **Install dependencies**:
```bash
pip install -e .
```

3. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

4. **Initialize the database**:
```bash
algotutor --init
```

## Usage 📖

### Start a Learning Session
```bash
algotutor --user your_username
```

### Available Commands
- **solve**: Work on algorithm problems with AI guidance
- **review**: Review your past solutions and progress
- **progress**: View detailed learning statistics
- **quit**: End your session

### Interactive Features

When solving problems, you can:
- **code**: Write and edit your solution
- **hint**: Get progressive hints (3 levels available)
- **submit**: Test your solution and get detailed feedback
- **skip**: Move to another problem

## Architecture 🏗️

```
algotutor/
├── core/           # Core configuration and utilities
├── models/         # Database models and schemas
├── services/       # Business logic services
│   ├── llm.py      # OpenAI integration for AI feedback
│   ├── execution.py # Code execution and testing
│   ├── database.py  # Data persistence
│   └── curriculum.py # Learning curriculum management
├── cli/            # Command-line interface
└── data/           # Sample data and curricula
```

### Key Components

1. **LLM Service**: Handles all AI interactions including:
   - Socratic questioning
   - Pattern recognition  
   - Line-by-line code analysis
   - Progressive hint generation

2. **Code Execution Service**: Safely executes Python code with:
   - Syntax validation
   - Test case execution
   - Timeout protection
   - Basic complexity analysis

3. **Database Service**: Manages persistence for:
   - User progress tracking
   - Session history
   - Problem attempts and feedback
   - Curriculum data

4. **Curriculum Service**: Organizes learning with:
   - Structured topic progression
   - Pattern-based problem categorization
   - Difficulty-adaptive content

## Curriculum Structure 📚

The tutor covers essential algorithm patterns:

- **Arrays & Strings**: Two pointers, sliding window
- **Hash Tables**: Fast lookups, frequency counting
- **Linked Lists**: Traversal, cycle detection, reversal
- **Stacks & Queues**: LIFO/FIFO, monotonic patterns
- **Trees**: Traversals, BST operations, construction
- **Graphs**: DFS/BFS, topological sort, union-find
- **Dynamic Programming**: Memoization, tabulation, patterns
- **Backtracking**: Constraint satisfaction, exhaustive search
- **Sorting & Searching**: Binary search, custom comparators

## Configuration ⚙️

Environment variables (`.env`):

```bash
# Required
OPENAI_API_KEY=your_api_key_here

# Optional  
MODEL_NAME=gpt-4-turbo-preview
MAX_TOKENS=2000
TEMPERATURE=0.7
DATABASE_URL=sqlite:///cb_tutor.db
DEBUG=False
LOG_LEVEL=INFO
```

## Examples 🎓

### Sample Learning Flow

1. **Start Session**: `algotutor --user alice`
2. **Choose Problem**: System suggests "Two Sum" for beginners
3. **Code Solution**: Interactive editor with syntax highlighting
4. **Get Feedback**: AI asks "What data structure could help you find complements efficiently?"
5. **Refine Approach**: Based on Socratic guidance
6. **Submit & Test**: Real-time execution with test cases
7. **Review Results**: Line-by-line analysis and pattern recognition

### AI Feedback Example

**Your Code**:
```python
def twoSum(nums, target):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
```

**AI Feedback**:
- "Your solution works but has O(n²) complexity. What if the array was very large?"
- "Line 2-3: The nested loops suggest we're checking every pair. Can we avoid this?"
- **Pattern Recognition**: `nested_loops`, `brute_force`
- **Suggestion**: "Consider using a hash map to store numbers you've seen"

## Development 🛠️

### Project Structure
- Uses SQLAlchemy for database ORM
- Pydantic for data validation
- Rich library for beautiful CLI interface
- Click for command-line parsing
- OpenAI API for LLM integration

### Adding New Problems
```python
problem = db_service.create_problem(
    title="Your Problem",
    description="Problem description...",
    difficulty="medium",
    category="Dynamic Programming",
    patterns=["dp", "memoization"],
    solution_template="def solve():\n    pass",
    test_cases=[{"input": [1, 2], "expected": 3}],
    hints=["Think about subproblems", "Consider memoization"]
)
```

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Submit a pull request

## License 📄

MIT License - see [LICENSE](LICENSE) file for details.

---

**Happy Learning!** 🚀 The best way to master algorithms is through guided practice with immediate feedback. AlgoTutor provides the AI mentorship you need to level up your coding skills.
