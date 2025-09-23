import sys
import types


def test_curses_selector_path(monkeypatch):
    # Force TTY path
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)

    # Build a fake curses module
    fake_curses = types.ModuleType("curses")
    fake_curses.KEY_UP = 259
    fake_curses.KEY_DOWN = 258
    fake_curses.A_REVERSE = 1
    fake_curses.KEY_ENTER = 10

    events = [fake_curses.KEY_DOWN, fake_curses.KEY_DOWN, ord("\n")]  # move to index 2 and select

    class FakeWin:
        def __init__(self):
            self.calls = []

        def keypad(self, flag):
            self.calls.append(("keypad", flag))

        def clear(self):
            pass

        def addstr(self, *args, **kwargs):
            # Accept any write
            pass

        def getmaxyx(self):
            return (10, 80)

        def attron(self, *_):
            pass

        def attroff(self, *_):
            pass

        def refresh(self):
            pass

        def getch(self):
            return events.pop(0) if events else ord("\n")

    def curs_set(_):
        return 0

    def wrapper(fn):
        return fn(FakeWin())

    fake_curses.curs_set = curs_set
    fake_curses.wrapper = wrapper

    # Install fake curses before import inside function
    monkeypatch.setitem(sys.modules, "curses", fake_curses)

    # Import the selector and call it
    from algotutor.cli.interactive import select

    choices = ["first", "second", "third", "fourth"]
    result = select("Choose one", choices, default=choices[0])

    assert result == "third"
