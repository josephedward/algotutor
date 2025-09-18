import os
import importlib
from click.testing import CliRunner


def test_e2e_init_and_quit(monkeypatch, tmp_path):
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

    # Start a session, visit a problem, request hints, back out, then quit
    # Sequence of inputs for interactive prompts
    user_inputs = "\n".join([
        "solve",  # main menu
        "hint",   # in-problem menu
        "hint",   # another hint
        "back",   # back to main menu
        "quit",   # exit
        "",
    ])

    session_result = runner.invoke(main, ["--user", "e2e_tester"], input=user_inputs)
    assert session_result.exit_code == 0, session_result.output

    # Sanity checks on output content
    assert "Welcome to CB Algorithm Tutor" in session_result.output
    assert "Problem:" in session_result.output
    assert "Hint" in session_result.output
    assert "Happy learning!" in session_result.output
