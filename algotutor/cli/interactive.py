"""Lightweight interactive selection with arrow keys.

Falls back to Rich Prompt when not attached to a TTY or when curses
is unavailable. Designed to keep dependencies minimal.
"""

from typing import List, Optional
import sys
import os


def select(prompt: str, choices: List[str], default: Optional[str] = None) -> str:
    """Select one item from a list with arrow keys.

    - Uses curses when stdin/stdout are TTYs and curses is available.
    - Falls back to simple input with a default when not interactive.
    """
    # Local import to avoid mandatory dependency when not used
    from rich.prompt import Prompt

    # Resolve default index
    default_idx = 0
    if default is not None and default in choices:
        default_idx = choices.index(default)

    # UI mode: classic (no curses), tui (force when TTY), auto (default)
    ui_mode = os.getenv("ALGOTUTOR_UI", "auto").strip().lower()

    # Only attempt curses when both streams are TTYs and mode allows it
    if ui_mode != "classic" and sys.stdin.isatty() and sys.stdout.isatty():
        try:
            import curses

            def _curses_main(stdscr):
                curses.curs_set(0)
                stdscr.keypad(True)
                current = default_idx

                while True:
                    stdscr.clear()
                    # Render prompt
                    stdscr.addstr(0, 0, f"{prompt}")
                    # Render choices
                    start_row = 2
                    h, w = stdscr.getmaxyx()
                    visible_height = max(1, h - start_row - 1)

                    # Basic scrolling support when many options
                    top = 0
                    if current >= top + visible_height:
                        top = current - visible_height + 1
                    if current < top:
                        top = current

                    for idx, item in enumerate(choices[top : top + visible_height]):
                        actual_idx = top + idx
                        prefix = "➤ " if actual_idx == current else "  "
                        line = f"{prefix}{item}"
                        if actual_idx == current:
                            stdscr.attron(curses.A_REVERSE)
                            stdscr.addstr(start_row + idx, 0, line[: w - 1])
                            stdscr.attroff(curses.A_REVERSE)
                        else:
                            stdscr.addstr(start_row + idx, 0, line[: w - 1])

                    stdscr.refresh()

                    key = stdscr.getch()
                    if key in (curses.KEY_UP, ord("k")):
                        current = (current - 1) % len(choices)
                    elif key in (curses.KEY_DOWN, ord("j")):
                        current = (current + 1) % len(choices)
                    elif key in (curses.KEY_ENTER, ord("\n"), ord("\r")):
                        return choices[current]
                    elif key in (27,):  # ESC
                        # Return default or current selection on ESC
                        return choices[default_idx]

            return curses.wrapper(_curses_main)
        except Exception:
            # Any curses failure -> fallback
            pass

    # Fallback: use rich Prompt with choices listing
    return Prompt.ask(prompt, choices=choices, default=default or choices[0])
