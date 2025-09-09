# Algorithm Tutor 📚

A Python-based algorithm study system focused on structured pattern-based learning for technical interview preparation. Built to address the core dilemma of time investment vs. study effectiveness by providing a minimal yet focused approach to mastering algorithmic patterns.

## 🎯 Philosophy

Based on research showing that **structured, pattern-based learning consistently outperforms random problem-solving**, this system implements:

- **Quality over Quantity**: Focus on deep understanding of 15-20 core patterns that cover 80%+ of interview questions
- **Structured Pattern Recognition**: Learn algorithmic patterns systematically rather than grinding random problems  
- **Spaced Repetition**: Built-in review system to ensure long-term retention
- **Progressive Difficulty**: Master patterns through easy → medium → hard problem progression

## ⚡ Quick Start

### Installation

```bash
# Install the package in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Basic Usage

```bash
# View all available patterns
algo-tutor patterns

# Get study recommendations
algo-tutor recommend

# Study a specific pattern
algo-tutor study "Two Pointers"

# View problems for a pattern
algo-tutor problems "Sliding Window"

# Complete a study session
algo-tutor complete "Two Pointers" --problems 3 --time 45 --difficulty medium

# Check your progress
algo-tutor progress

# Set focus patterns for concentrated study
algo-tutor focus "Two Pointers" "Sliding Window" "Binary Search"
```

## 🏗️ Core Components

### Pattern System
- **15-20 Essential Patterns**: Covering arrays, trees, graphs, dynamic programming, etc.
- **Structured Problems**: Each pattern includes curated problems with difficulty progression
- **Key Insights**: Every problem includes the essential insights needed to solve it

### Study Management
- **Session Tracking**: Log study time, problems completed, and difficulty reached
- **Progress Persistence**: Your progress is saved locally and persists across sessions
- **Mastery Levels**: Track your mastery (0-100%) for each pattern

### Intelligent Recommendations
- **Spaced Repetition**: Automatically suggests patterns that need review
- **Weakness Identification**: Highlights patterns below mastery threshold
- **Focus Mode**: Set specific patterns for concentrated study

## 📊 Pattern Categories

The system covers these essential algorithmic categories:

- **Two Pointers** - Array/string problems with pairs or palindromes
- **Sliding Window** - Substring/subarray problems with constraints  
- **Fast & Slow Pointers** - Cycle detection and linked list problems
- **Merge Intervals** - Scheduling and time interval problems
- **Cyclic Sort** - Arrays with numbers in specific ranges
- **Tree BFS/DFS** - Tree traversal and path finding
- **Binary Search** - Search problems in sorted arrays
- **Top K Elements** - Heap-based problems
- **In-place LinkedList Reversal** - LinkedList modification problems

## 🧪 Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=algorithm_tutor

# Run specific test file
pytest tests/test_patterns_db.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/
```

## 🚀 Design Principles

### Avoiding Feature Creep
This system deliberately stays minimal to avoid the "interesting features trap" that can distract from the core goal of interview preparation.

### Time Investment ROI
Built with the understanding that 6-12 weeks spent building a custom system could instead be 66-132 hours of direct interview preparation. Every feature is justified by learning effectiveness.

### Evidence-Based Learning
Implements proven study techniques:
- Pattern-based learning (higher ROI than random problems)
- Spaced repetition for long-term retention
- Progressive difficulty scaling
- Quality over quantity emphasis

## 📈 Usage Examples

### Daily Study Routine
```bash
# 1. Check recommendations
algo-tutor recommend

# 2. Study recommended pattern
algo-tutor study "Sliding Window"

# 3. Complete problems and log session
algo-tutor complete "Sliding Window" --problems 2 --time 60 --difficulty medium

# 4. Check progress
algo-tutor progress
```

### Focus Mode for Weak Areas
```bash
# Identify weak patterns
algo-tutor progress

# Set focus on specific patterns
algo-tutor focus "Dynamic Programming" "Backtracking" "Graphs"

# Get focused recommendations
algo-tutor recommend
```

## 🎓 Learning Path

1. **Start with Beginner Patterns**: Two Pointers, Sliding Window, Fast & Slow Pointers
2. **Master Tree Patterns**: BFS and DFS for tree problems  
3. **Advanced Patterns**: Binary Search, Top K Elements, Merge Intervals
4. **Expert Level**: Dynamic Programming, Backtracking, Graph algorithms

## 📝 Contributing

This system is designed to be minimal and focused. Before adding features, consider:
- Does this improve learning effectiveness?
- Does this save more time than it costs to implement?
- Is this essential for the core goal of interview preparation?

## 📄 License

MIT License - see LICENSE file for details.
