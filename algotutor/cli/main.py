"""CLI interface for CB Algorithm Tutor."""

import click
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown
from typing import Optional, Dict, Any
import time

from algotutor.services.database import db_service
from algotutor.services.llm import llm_service
from algotutor.services.execution import code_execution_service
from algotutor.services.curriculum import curriculum_service
from algotutor.models import User, Problem, Attempt

console = Console()


class TutorSession:
    """Interactive tutoring session manager."""
    
    def __init__(self, user: User):
        self.user = user
        self.current_problem: Optional[Problem] = None
        self.current_attempt: Optional[Attempt] = None
        self.hint_level = 0
        
    def start_session(self):
        """Start an interactive learning session."""
        console.print(Panel.fit(
            f"[bold green]Welcome to CB Algorithm Tutor, {self.user.username}![/bold green]\n"
            "Let's begin your personalized learning session.",
            title="🎯 Learning Session"
        ))
        
        while True:
            choice = Prompt.ask(
                "\nWhat would you like to do?",
                choices=["solve", "review", "progress", "quit"],
                default="solve"
            )
            
            if choice == "solve":
                self.solve_problem()
            elif choice == "review":
                self.review_progress()
            elif choice == "progress":
                self.show_progress()
            elif choice == "quit":
                console.print("[yellow]Happy learning! See you next time! 👋[/yellow]")
                break
    
    def solve_problem(self):
        """Interactive problem solving with LLM guidance."""
        # Get a problem (simplified - just get first available problem)
        problems = db_service.get_problems_by_category("Arrays and Strings")
        if not problems:
            console.print("[red]No problems available. Please initialize the curriculum first.[/red]")
            return
            
        self.current_problem = problems[0]  # For demo, use first problem
        self.hint_level = 0
        
        # Display problem
        self.display_problem()
        
        # Interactive coding loop
        while True:
            action = Prompt.ask(
                "\nWhat would you like to do?",
                choices=["code", "hint", "submit", "skip", "back"],
                default="code"
            )
            
            if action == "code":
                self.code_editor()
            elif action == "hint":
                self.get_hint()
            elif action == "submit":
                if self.submit_solution():
                    break
            elif action == "skip":
                console.print("[yellow]Skipping this problem. Try another one![/yellow]")
                break
            elif action == "back":
                break
    
    def display_problem(self):
        """Display the current problem details."""
        if not self.current_problem:
            return
            
        problem = self.current_problem
        
        # Problem header
        console.print(f"\n[bold blue]Problem: {problem.title}[/bold blue]")
        console.print(f"[dim]Difficulty: {problem.difficulty.title()} | Category: {problem.category}[/dim]")
        console.print(f"[dim]Patterns: {', '.join(problem.patterns)}[/dim]\n")
        
        # Problem description
        console.print(Panel(
            Markdown(problem.description),
            title="📋 Problem Description",
            border_style="blue"
        ))
        
        # Template code
        if problem.solution_template:
            console.print("\n[bold]Starting Template:[/bold]")
            syntax = Syntax(problem.solution_template, "python", theme="monokai", line_numbers=True)
            console.print(syntax)
    
    def code_editor(self):
        """Open system editor for code entry, with fallback."""
        if not self.current_problem:
            return

        console.print("\n[bold]Code Editor[/bold]")
        console.print("[dim]Opening your $EDITOR (falls back to vi). Save & quit to return.[/dim]")

        # Determine initial content
        initial = None
        if self.current_attempt and self.current_attempt.code:
            initial = self.current_attempt.code
        elif self.current_problem.solution_template:
            initial = self.current_problem.solution_template
        else:
            initial = "# Write your solution here\n"

        edited = None
        try:
            edited = click.edit(initial, extension=".py")
        except Exception as e:
            console.print(f"[red]Failed to open external editor: {e}[/red]")

        # If editor was aborted or failed, fall back to simple inline input
        if edited is None:
            console.print("[yellow]Editor aborted. Falling back to inline entry. Press Enter twice to finish.[/yellow]")
            code_lines = []
            empty_lines = 0
            while empty_lines < 2:
                try:
                    line = input(">>> " if not code_lines else "... ")
                except (EOFError, KeyboardInterrupt):
                    break
                if line.strip() == "":
                    empty_lines += 1
                else:
                    empty_lines = 0
                code_lines.append(line)
            while code_lines and code_lines[-1].strip() == "":
                code_lines.pop()
            edited = "\n".join(code_lines)

        code = (edited or "").rstrip()
        if not code.strip():
            console.print("[red]No code captured.[/red]")
            return

        # Create or update attempt
        if self.current_attempt is None:
            self.current_attempt = db_service.create_attempt(
                user_id=self.user.id,
                problem_id=self.current_problem.id,
                code=code,
            )
        else:
            db_service.update_attempt(self.current_attempt.id, code=code)

        # Show code with syntax highlighting
        console.print("\n[bold]Your Code:[/bold]")
        syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
        console.print(syntax)

        # Get Socratic question from LLM
        self.provide_socratic_feedback(code)
    
    def provide_socratic_feedback(self, code: str):
        """Provide Socratic questioning feedback."""
        with console.status("[dim]Analyzing your code...[/dim]") as status:
            question = llm_service.generate_socratic_question(
                code=code,
                problem=self.current_problem.description,
                context="Student is working on their solution"
            )
        
        console.print(Panel(
            f"[italic]{question}[/italic]",
            title="🤔 Think About This",
            border_style="green"
        ))
        
        response = Prompt.ask("\nYour thoughts")
        if response:
            console.print(f"[dim]Interesting perspective: {response}[/dim]")
    
    def get_hint(self):
        """Get a progressive hint."""
        if not self.current_problem:
            return
            
        self.hint_level = min(self.hint_level + 1, 3)
        
        if self.hint_level <= len(self.current_problem.hints):
            hint = self.current_problem.hints[self.hint_level - 1]
        else:
            # Generate LLM hint
            with console.status("[dim]Generating hint...[/dim]"):
                code = self.current_attempt.code if self.current_attempt else ""
                hint = llm_service.generate_hint(
                    problem=self.current_problem.description,
                    current_code=code,
                    hint_level=self.hint_level
                )
        
        console.print(Panel(
            f"[yellow]Hint {self.hint_level}: {hint}[/yellow]",
            title="💡 Hint",
            border_style="yellow"
        ))
    
    def submit_solution(self) -> bool:
        """Submit and test the solution."""
        if not self.current_attempt:
            console.print("[red]No code to submit. Write some code first![/red]")
            return False
        
        code = self.current_attempt.code
        test_cases = self.current_problem.test_cases
        
        console.print("\n[bold]Testing your solution...[/bold]")
        
        # Execute code with test cases
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Running tests...", total=None)
            results = code_execution_service.execute_python_code(code, test_cases)
        
        # Display results
        self.display_test_results(results)
        
        # Get detailed feedback from LLM
        if results["syntax_valid"]:
            self.provide_detailed_feedback(code, results)
        
        # Update attempt record
        db_service.update_attempt(
            self.current_attempt.id,
            status="solved" if results["success"] else "attempted",
            feedback=results
        )
        
        return results["success"]
    
    def display_test_results(self, results: Dict[str, Any]):
        """Display test execution results."""
        if not results["syntax_valid"]:
            console.print(Panel(
                f"[red]Syntax Error:\n{results['errors']}[/red]",
                title="❌ Syntax Error",
                border_style="red"
            ))
            return
        
        if results["success"]:
            console.print(Panel(
                "[green]🎉 All tests passed! Great job![/green]",
                title="✅ Success",
                border_style="green"
            ))
        else:
            console.print(f"[yellow]Test Results: {results['output']}[/yellow]")
        
        # Show individual test results
        if results["test_results"]:
            table = Table(title="Test Case Results")
            table.add_column("Test", style="cyan")
            table.add_column("Input", style="magenta")
            table.add_column("Expected", style="green")
            table.add_column("Actual", style="yellow")
            table.add_column("Result", justify="center")
            
            for test in results["test_results"]:
                status = "✅" if test["passed"] else "❌"
                table.add_row(
                    str(test["test_case"]),
                    str(test["input"]),
                    str(test["expected"]),
                    str(test.get("actual", "Error")),
                    status
                )
            
            console.print(table)
    
    def provide_detailed_feedback(self, code: str, results: Dict[str, Any]):
        """Provide detailed LLM feedback on the solution."""
        with console.status("[dim]Generating detailed feedback...[/dim]"):
            feedback = llm_service.provide_line_by_line_feedback(
                code=code,
                problem=self.current_problem.description
            )
        
        # Display overall feedback
        console.print(Panel(
            feedback.get("overall_feedback", "No feedback available"),
            title="📝 Overall Feedback",
            border_style="blue"
        ))
        
        # Display complexity analysis
        complexity_info = f"""
        **Time Complexity:** {feedback.get('time_complexity', 'Unknown')}
        **Space Complexity:** {feedback.get('space_complexity', 'Unknown')}
        """
        console.print(Panel(
            Markdown(complexity_info),
            title="⚡ Complexity Analysis",
            border_style="cyan"
        ))
        
        # Display patterns identified
        patterns = feedback.get("patterns_used", [])
        if patterns:
            console.print(f"[dim]Patterns identified: {', '.join(patterns)}[/dim]")
    
    def review_progress(self):
        """Review user's progress and patterns."""
        console.print("[blue]Coming soon: Progress review feature![/blue]")
    
    def show_progress(self):
        """Show detailed progress statistics."""
        console.print("[blue]Coming soon: Detailed progress statistics![/blue]")


@click.command()
@click.option('--user', '-u', help='Username for the session')
@click.option('--init', is_flag=True, help='Initialize database with sample data')
def main(user: str, init: bool):
    """CB Algorithm Tutor - Your AI-powered coding mentor."""
    
    if init:
        console.print("[yellow]Initializing database and sample data...[/yellow]")
        db_service.create_tables()
        curriculum_service.initialize_default_data()
        console.print("[green]✅ Initialization complete![/green]")
        return
    
    # Ensure database is set up
    db_service.create_tables()
    
    # Get or create user
    if not user:
        user = Prompt.ask("Enter your username")
    
    db_user = db_service.get_user_by_username(user)
    if not db_user:
        console.print(f"[green]Creating new user account for {user}[/green]")
        db_user = db_service.create_user(username=user)
    
    # Start tutoring session
    session = TutorSession(db_user)
    session.start_session()


if __name__ == "__main__":
    main()
