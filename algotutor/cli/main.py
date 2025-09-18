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
import os
import shlex
import shutil
import ast
import time
import tempfile

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
                choices=["solve", "pick", "review", "progress", "quit"],
                default="solve"
            )
            
            if choice == "solve":
                # Default quick-start problem (Arrays and Strings → first)
                self.solve_problem()
            elif choice == "pick":
                problem = self.pick_problem()
                if problem:
                    self.current_problem = problem
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
        # If no problem pre-selected, pick default: first in Arrays and Strings
        if not self.current_problem:
            problems = db_service.get_problems_by_category("Arrays and Strings")
            if not problems:
                console.print("[red]No problems available. Please initialize the curriculum first.[/red]")
                return
            self.current_problem = problems[0]
        self.hint_level = 0
        
        # Display problem
        self.display_problem()
        
        # Interactive coding loop
        while True:
            action = Prompt.ask(
                "\nWhat would you like to do?",
                choices=["code", "format", "lint", "hint", "submit", "skip", "back"],
                default="code"
            )
            
            if action == "code":
                self.code_editor()
            elif action == "format":
                self.format_code()
            elif action == "lint":
                self.lint_code()
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
        console.print("[dim]Opening your editor. Save & quit to return.[/dim]")

        # Determine initial content
        initial = None
        if self.current_attempt and self.current_attempt.code:
            initial = self.current_attempt.code
        elif self.current_problem.solution_template:
            initial = self.current_problem.solution_template
        else:
            initial = "# Write your solution here\n"

        # Choose editor: Settings.editor_command > $VISUAL/$EDITOR > common fallbacks
        edited = None
        editor_cmd = self._select_editor()
        if editor_cmd:
            try:
                # require_save=False returns content even if unchanged
                edited = click.edit(initial, extension=".py", editor=editor_cmd, require_save=False)
            except Exception as e:
                console.print(f"[red]Failed to open external editor '{editor_cmd}': {e}[/red]")
        else:
            console.print("[yellow]No suitable editor found in PATH. Falling back to inline entry.[/yellow]")

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

        # Optional: pre-parse to catch obvious syntax issues early
        try:
            # Sanitize first to avoid tab/space mix false positives
            code_for_check = code_execution_service.sanitize_code(code)
            ast.parse(code_for_check)
        except SyntaxError as e:
            console.print(Panel(
                f"[red]Syntax error on line {getattr(e, 'lineno', '?')}: {e.msg}[/red]",
                title="❌ Syntax Error",
                border_style="red",
            ))
            # Show a snippet for context
            syntax = Syntax(code_for_check, "python", theme="monokai", line_numbers=True)
            console.print(syntax)
            if Confirm.ask("Open editor to fix it?", default=True):
                return self.code_editor()

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

    def pick_problem(self) -> Optional[Problem]:
        """Let the user choose a category and problem to solve."""
        categories = db_service.list_problem_categories()
        if not categories:
            console.print("[red]No problems available. Please initialize the curriculum first.[/red]")
            return None
        category = Prompt.ask("Choose a category", choices=categories, default=categories[0])
        problems = db_service.get_problems_by_category(category)
        if not problems:
            console.print("[red]No problems in that category.[/red]")
            return None
        titles = [p.title for p in problems]
        selected_title = Prompt.ask("Choose a problem", choices=titles, default=titles[0])
        for p in problems:
            if p.title == selected_title:
                return p
        return problems[0]

    def _select_editor(self) -> Optional[str]:
        """Pick an editor command to use with click.edit.

        Priority: settings.editor_command -> $VISUAL -> $EDITOR -> fallback list.
        Ensures VS Code waits for window close by adding -w if missing.
        Returns a shell command string or None if none found.
        """
        # Prefer explicit setting
        from algotutor.core.config import settings

        candidates: list[str] = []
        if settings.editor_command:
            candidates.append(settings.editor_command)

        env_visual = os.environ.get("VISUAL")
        env_editor = os.environ.get("EDITOR")
        if env_visual:
            candidates.append(env_visual)
        if env_editor:
            candidates.append(env_editor)

        # Common fallbacks by preference
        candidates.extend([
            "code -w",  # VS Code
            "cursor -w",  # Cursor editor
            "nvim",
            "vim",
            "nano",
            "vi",
        ])

        for cmd in candidates:
            # Extract executable for which()
            exe = shlex.split(cmd)[0] if cmd else ""
            if exe and shutil.which(exe):
                # Ensure VS Code waits
                if exe in {"code", "cursor"} and "-w" not in cmd:
                    cmd = f"{cmd} -w"
                return cmd
        return None
    
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

    def format_code(self):
        """Format the current code with Black if available."""
        if not self.current_attempt or not (self.current_attempt.code or "").strip():
            console.print("[yellow]No code to format. Use 'code' first.[/yellow]")
            return
        code = self.current_attempt.code
        try:
            import black

            mode = black.Mode()  # respects pyproject defaults
            formatted = black.format_str(code, mode=mode)
            if formatted != code:
                db_service.update_attempt(self.current_attempt.id, code=formatted)
                self.current_attempt.code = formatted
                console.print("[green]Code formatted with Black.[/green]")
            else:
                console.print("[green]Code already well-formatted.[/green]")
            syntax = Syntax(self.current_attempt.code, "python", theme="monokai", line_numbers=True)
            console.print(syntax)
        except Exception as e:
            console.print(Panel(
                f"Black not available or failed: {e}\nInstall dev extras: pip install -e .[dev]",
                title="⚠️ Formatter",
                border_style="yellow",
            ))

    def lint_code(self):
        """Lint the current code. Uses flake8 if available, else basic checks."""
        if not self.current_attempt or not (self.current_attempt.code or "").strip():
            console.print("[yellow]No code to lint. Use 'code' first.[/yellow]")
            return
        code = self.current_attempt.code

        # Try flake8 API first
        try:
            from flake8.api import legacy as flake8

            style_guide = flake8.get_style_guide(max_line_length=88)
            with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tf:
                tf.write(code)
                tmp_path = tf.name
            report = style_guide.check_files([tmp_path])
            os.unlink(tmp_path)
            if report.total_errors == 0:
                console.print(Panel("No lint issues found.", title="🧹 Lint", border_style="green"))
            else:
                console.print(Panel(f"Found {report.total_errors} issue(s). (See above)", title="🧹 Lint", border_style="yellow"))
                syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
                console.print(syntax)
            return
        except Exception:
            pass

        # Basic fallback checks
        issues = []
        lines = code.splitlines()
        for i, ln in enumerate(lines, 1):
            if "\t" in ln[:len(ln) - len(ln.lstrip())]:
                issues.append((i, "TABS", "Indentation uses tabs; prefer 4 spaces."))
            if len(ln) > 100:
                issues.append((i, "LINE", f"Line too long ({len(ln)} > 100)."))
            if ln.rstrip() != ln:
                issues.append((i, "WS", "Trailing whitespace."))
        try:
            ast.parse(code)
        except SyntaxError as e:
            issues.append((getattr(e, "lineno", 0) or 0, "SYNTAX", e.msg))

        if not issues:
            console.print(Panel("No lint issues found (basic checks).", title="🧹 Lint", border_style="green"))
        else:
            table = Table(title="Lint Issues (basic)")
            table.add_column("Line", style="cyan", justify="right")
            table.add_column("Code", style="magenta")
            table.add_column("Message", style="yellow")
            for line, code_, msg in issues[:50]:
                table.add_row(str(line), code_, msg)
            console.print(table)
    
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

        # Always compute heuristic complexity as a fallback
        heuristics = code_execution_service.analyze_complexity(code_execution_service.sanitize_code(code))
        
        # Display overall feedback
        overall = feedback.get("overall_feedback", "No feedback available")
        console.print(Panel(
            overall,
            title="📝 Overall Feedback",
            border_style="blue"
        ))
        
        # Display complexity analysis
        def _pref(val: Optional[str], h: str) -> str:
            if val and str(val).strip().lower() not in {"unknown", "n/a"}:
                return str(val)
            return h or "Unknown"

        time_c = _pref(feedback.get('time_complexity'), heuristics.get('time_complexity', 'Unknown'))
        space_c = _pref(feedback.get('space_complexity'), heuristics.get('space_complexity', 'Unknown'))
        complexity_info = f"""
        **Time Complexity:** {time_c}
        **Space Complexity:** {space_c}
        """
        console.print(Panel(
            Markdown(complexity_info),
            title="⚡ Complexity Analysis",
            border_style="cyan"
        ))

        # If no LLM available, provide a helpful hint to enable it
        if "Unable to analyze" in overall or "LLM not configured" in overall:
            from algotutor.core.config import settings
            tip = "Set OPENAI_API_KEY in your .env to enable AI analysis."
            if settings.openai_api_key:
                tip = f"LLM error occurred. Verify network access and model name (current: {settings.model_name})."
            console.print(Panel(tip, title="ℹ️ Tip", border_style="magenta"))
        
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
