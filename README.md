# CB - Algorithm Tutor with Study System

A Python-based algorithm tutor featuring an intelligent study system that tracks student progress, adapts to learning patterns, and provides personalized recommendations.

## Features

- **Progress Tracking**: Monitor student performance across multiple study sessions
- **Adaptive Learning**: Personalized topic recommendations based on prerequisites and mastery
- **Performance Analytics**: Detailed statistics on learning progress and problem-solving success
- **Persistent Data**: Student progress is automatically saved and restored across sessions

## Quick Start

### Using the Command Line Interface

1. **Start a study session:**
   ```bash
   python tutor_cli.py -s your_name start
   ```

2. **End a study session with progress:**
   ```bash
   python tutor_cli.py -s your_name end --session SESSION_ID --topics arrays linked_lists --attempted 8 --completed 6
   ```

3. **View your statistics:**
   ```bash
   python tutor_cli.py -s your_name stats
   ```

4. **Get topic recommendations:**
   ```bash
   python tutor_cli.py -s your_name recommend
   ```

### Using the Python API

```python
from study_system import StudySystemManager

# Initialize the study system
study_system = StudySystemManager()

# Start a session
session_id = study_system.start_study_session("student_name")

# End session with progress
study_system.end_study_session(
    "student_name", 
    session_id,
    ["arrays", "sorting"], 
    problems_attempted=5, 
    problems_completed=4
)

# Get statistics
stats = study_system.get_student_statistics("student_name")
print(stats)
```

## Study System Features

The study system tracks learning across these algorithm topics:

- **Beginner**: Arrays, Linked Lists, Stacks & Queues
- **Intermediate**: Binary Trees, Graphs  
- **Advanced**: Dynamic Programming

Topics are unlocked based on prerequisites, ensuring a structured learning path.

## Files

- `study_system_analysis.md` - Detailed analysis of study system requirements
- `study_system.py` - Core study system implementation
- `tutor_cli.py` - Command-line interface
- `test_study_system.py` - Test suite

## Testing

Run the test suite to verify functionality:

```bash
python test_study_system.py
```
