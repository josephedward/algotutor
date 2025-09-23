import os
import importlib
from click.testing import CliRunner


def test_pick_problem_fallback_selection(monkeypatch, tmp_path):
    # Point DB to a temp file and set a dummy OpenAI key before importing
    db_file = tmp_path / "cb_tutor_test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_file}"
    os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "test-123")

    # Import CLI after env is set
    cli_main_mod = importlib.import_module("algotutor.cli.main")
    main = getattr(cli_main_mod, "main")

    runner = CliRunner()

    # Initialize database and sample data
    init_result = runner.invoke(main, ["--init"])
    assert init_result.exit_code == 0, init_result.output
    assert "Initialization complete" in init_result.output

    # Choose via textual fallback (non-TTY) to ensure no escape sequences leak
    # The categories from default data include 'Dynamic Programming'
    # Then select the 'Maximum Subarray' problem, back out, and quit
    user_inputs = "\n".join(
        [
            "pick",
            "Dynamic Programming",
            "Maximum Subarray",
            "back",
            "quit",
            "",
        ]
    )

    session_result = runner.invoke(main, ["--user", "e2e_selector"], input=user_inputs)
    assert session_result.exit_code == 0, session_result.output

    out = session_result.output
    # Sanity: saw prompts and selected problem shown
    assert "Choose a category" in out
    assert "Choose a problem" in out
    assert "Maximum Subarray" in out

    # Ensure no raw arrow escape sequences leaked into output
    assert "^[[A" not in out

