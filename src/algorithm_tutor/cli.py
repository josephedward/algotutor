"""
Command line interface for the Algorithm Tutor.
"""

import click
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel

from rich.table import Table


from .tutor import AlgorithmTutor

console = Console()


@click.group()
@click.pass_context
def cli(ctx):
    """Algorithm Tutor - Structured pattern-based interview preparation."""
    ctx.ensure_object(dict)
    ctx.obj["tutor"] = AlgorithmTutor()


@cli.command()
@click.pass_context
def patterns(ctx):
    """List all available algorithm patterns."""
    tutor = ctx.obj["tutor"]
    patterns = tutor.get_available_patterns()

    table = Table(title="📚 Core Algorithm Patterns")
    table.add_column("Pattern", style="cyan", no_wrap=True)
    table.add_column("Category", style="magenta")
    table.add_column("Description", style="white")
    table.add_column("Problems", justify="center", style="yellow")
    table.add_column("Mastery", justify="center", style="green")

    for pattern in patterns:
        mastery = tutor.session.get_pattern_mastery_level(pattern.name)
        mastery_display = f"{mastery}%"

        # Color code mastery level
        if mastery >= 80:
            mastery_display = f"[green]{mastery}%[/green]"
        elif mastery >= 40:
            mastery_display = f"[yellow]{mastery}%[/yellow]"
        else:
            mastery_display = f"[red]{mastery}%[/red]"

        table.add_row(
            pattern.name,
            pattern.category.value.replace("_", " ").title(),
            (
                pattern.description[:60] + "..."
                if len(pattern.description) > 60
                else pattern.description
            ),
            str(len(pattern.problems)),
            mastery_display,
        )

    console.print(table)


@cli.command()
@click.argument("pattern_name")
@click.pass_context
def study(ctx, pattern_name):
    """Start studying a specific pattern."""
    tutor = ctx.obj["tutor"]

    try:
        pattern = tutor.start_study_session(pattern_name)

        # Show available problems
        if pattern.problems:
            rprint("\\n📋 Available Problems:")
            tutor.show_pattern_problems(pattern_name)

        # Get next problem suggestion
        suggested = tutor.get_next_problem_suggestion(pattern_name)
        if suggested:
            rprint(f"\\n💡 Suggested next problem: [bold cyan]{suggested}[/bold cyan]")

        # Interactive completion
        rprint("\\n" + "=" * 50)
        rprint("[bold green]Study Session Active[/bold green]")
        rprint(
            "Complete your study session and then use 'complete' command to log progress."
        )

    except ValueError as e:
        rprint(f"[red]Error: {e}[/red]")


@cli.command()
@click.argument("pattern_name")
@click.option("--problems", "-p", default=1, help="Number of problems completed")
@click.option("--time", "-t", default=30, help="Time spent in minutes")
@click.option(
    "--difficulty",
    "-d",
    type=click.Choice(["easy", "medium", "hard"], case_sensitive=False),
    default="easy",
    help="Highest difficulty reached",
)
@click.option("--notes", "-n", default="", help="Additional notes about the session")
@click.pass_context
def complete(ctx, pattern_name, problems, time, difficulty, notes):
    """Complete and log a study session."""
    tutor = ctx.obj["tutor"]

    try:
        tutor.complete_study_session(pattern_name, problems, time, difficulty, notes)

        # Show recommendations for next study
        recommendations = tutor.get_study_recommendations()
        if recommendations:
            rprint("\\n🎯 Recommended patterns for next study:")
            for rec in recommendations:
                rprint(f"   • [cyan]{rec}[/cyan]")

    except ValueError as e:
        rprint(f"[red]Error: {e}[/red]")


@cli.command()
@click.pass_context
def progress(ctx):
    """Show detailed progress summary."""
    tutor = ctx.obj["tutor"]
    summary = tutor.get_progress_summary()

    # Main stats panel
    stats_text = f"""
📊 Total Study Time: {summary['total_study_time']} minutes
📚 Patterns Studied: {summary['patterns_studied']}/{summary['total_patterns']}
📈 Average Mastery: {summary['average_mastery']}%
📅 Recent Studies (7 days): {summary['recent_studies_count']}
    """

    console.print(Panel(stats_text, title="📈 Study Progress", border_style="green"))

    # Focus patterns
    if summary["current_focus"]:
        focus_text = "\\n".join(
            [f"• {pattern}" for pattern in summary["current_focus"]]
        )
        console.print(
            Panel(focus_text, title="🎯 Current Focus Patterns", border_style="cyan")
        )

    # Weak patterns that need attention
    if summary["weak_patterns"]:
        weak_text = "\\n".join([f"• {pattern}" for pattern in summary["weak_patterns"]])
        console.print(
            Panel(weak_text, title="⚠️ Patterns Needing Attention", border_style="red")
        )

    # Mastery levels table
    table = Table(title="🏆 Pattern Mastery Levels")
    table.add_column("Pattern", style="cyan")
    table.add_column("Mastery", justify="center")
    table.add_column("Status", justify="center")

    for pattern_name, mastery in summary["mastery_levels"].items():
        if mastery >= 80:
            status = "[green]Excellent[/green]"
        elif mastery >= 60:
            status = "[yellow]Good[/yellow]"
        elif mastery >= 40:
            status = "[orange]Fair[/orange]"
        else:
            status = "[red]Needs Work[/red]"

        table.add_row(pattern_name, f"{mastery}%", status)

    console.print(table)


@cli.command()
@click.pass_context
def recommend(ctx):
    """Get study recommendations for next session."""
    tutor = ctx.obj["tutor"]
    recommendations = tutor.get_study_recommendations(limit=5)

    if not recommendations:
        rprint("[green]Great job! You're up to date with all patterns.[/green]")
        rprint("Consider reviewing advanced problems or adding new focus patterns.")
        return

    rprint("\\n🎯 [bold cyan]Recommended Study Plan[/bold cyan]")
    rprint("Based on spaced repetition and your progress:")

    for i, pattern_name in enumerate(recommendations, 1):
        mastery = tutor.session.get_pattern_mastery_level(pattern_name)
        needs_review = tutor.session.should_review_pattern(pattern_name)

        status = "🔄 Review due" if needs_review else "📈 Continue progress"
        rprint(f"\\n{i}. [bold]{pattern_name}[/bold] ({mastery}% mastery)")
        rprint(f"   {status}")

        # Get next problem suggestion
        suggested = tutor.get_next_problem_suggestion(pattern_name)
        if suggested:
            rprint(f"   💡 Suggested problem: {suggested}")


@cli.command()
@click.argument("pattern_name")
@click.option(
    "--difficulty",
    "-d",
    type=click.Choice(["easy", "medium", "hard"], case_sensitive=False),
    help="Filter problems by difficulty",
)
@click.pass_context
def problems(ctx, pattern_name, difficulty):
    """Show problems for a specific pattern."""
    tutor = ctx.obj["tutor"]

    try:
        tutor.show_pattern_problems(pattern_name, difficulty)
    except ValueError as e:
        rprint(f"[red]Error: {e}[/red]")


@cli.command()
@click.argument("patterns", nargs=-1, required=True)
@click.pass_context
def focus(ctx, patterns):
    """Set focus patterns for concentrated study."""
    tutor = ctx.obj["tutor"]

    try:
        tutor.set_focus_patterns(list(patterns))
    except ValueError as e:
        rprint(f"[red]Error: {e}[/red]")


@cli.command()
@click.argument("pattern_name")
@click.pass_context
def info(ctx, pattern_name):
    """Show detailed information about a specific pattern."""
    tutor = ctx.obj["tutor"]

    try:
        pattern = tutor.get_pattern_details(pattern_name)

        # Main pattern info
        info_text = f"""
📝 {pattern.description}

🔑 Key Concepts:
{chr(10).join([f'   • {concept}' for concept in pattern.key_concepts])}

🎪 When to use: {pattern.when_to_use}

⏱️ Time Complexity: {pattern.time_complexity_notes}
🗂️ Space Complexity: {pattern.space_complexity_notes}
        """

        console.print(
            Panel(info_text.strip(), title=f"📚 {pattern.name}", border_style="blue")
        )

        # Show problems
        if pattern.problems:
            rprint("\\n📋 Problems:")
            tutor.show_pattern_problems(pattern_name)

        # Show current mastery
        mastery = tutor.session.get_pattern_mastery_level(pattern_name)
        rprint(f"\\n📈 Your current mastery level: [bold]{mastery}%[/bold]")

    except ValueError as e:
        rprint(f"[red]Error: {e}[/red]")


def main():
    """Entry point for the CLI application."""
    cli()


if __name__ == "__main__":
    main()
