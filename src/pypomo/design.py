# The look of the full-screen timer. Change the settings below to restyle it.
import os

# --- Settings ---
TITLE_ART = """\
██████╗ ██╗   ██╗██████╗  ██████╗ ███╗   ███╗ ██████╗
██╔══██╗╚██╗ ██╔╝██╔══██╗██╔═══██╗████╗ ████║██╔═══██╗
██████╔╝ ╚████╔╝ ██████╔╝██║   ██║██╔████╔██║██║   ██║
██╔═══╝   ╚██╔╝  ██╔═══╝ ██║   ██║██║╚██╔╝██║██║   ██║
██║        ██║   ██║     ╚██████╔╝██║ ╚═╝ ██║╚██████╔╝
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝     ╚═╝ ╚═════╝"""
PLAIN_TITLE = "PYPOMO"  # used when the terminal is too small for TITLE_ART
TITLE_COLOUR = "\033[38;5;208m"  # orange
BORDER_COLOUR = "\033[90m"  # grey
ACTIVE_COLOUR = "\033[32m"  # green
SHOW_BORDER = True

# --- Terminal control codes ---
RESET = "\033[0m"
CLEAR_SCREEN = "\033[2J"
ENTER_SCREEN = "\033[?1049h"  # the alternate screen, which leaves your terminal history alone
LEAVE_SCREEN = "\033[?1049l"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
WRAP_OFF = "\033[?7l"  # stops long lines wrapping and breaking the layout
WRAP_ON = "\033[?7h"


def _at(row, col, text):
    """Place text at a screen position. Rows and columns start at 1."""
    return f"\033[{row};{col}H{text}"


class FullScreen:
    """Takes over the terminal inside a `with` block and restores it afterwards."""

    def __init__(self):
        self._size = None  # the terminal size the border and title were last drawn at

    def __enter__(self):
        print(ENTER_SCREEN + HIDE_CURSOR + WRAP_OFF, end="", flush=True)
        return self

    def __exit__(self, *exc_info):
        print(WRAP_ON + SHOW_CURSOR + LEAVE_SCREEN, end="")
        print("Timer stopped.")

    def draw(self, timers):
        """Draw one frame. `timers` is a list of (label, seconds, is_active)."""
        size = os.get_terminal_size()
        frame = ""
        if size != self._size:  # only redraw the fixed parts when they could have moved
            self._size = size
            frame += self._background(size.columns, size.lines)
        frame += self._timer_row(timers, size.columns, size.lines)
        print(frame, end="", flush=True)

    def _background(self, cols, rows):
        margin = 1 if SHOW_BORDER else 0
        inner = cols - 2 * margin
        out = CLEAR_SCREEN
        if SHOW_BORDER:
            out += BORDER_COLOUR
            out += _at(1, 1, "╭" + "─" * (cols - 2) + "╮")
            for row in range(2, rows):
                out += _at(row, 1, "│") + _at(row, cols, "│")
            out += _at(rows, 1, "╰" + "─" * (cols - 2) + "╯") + RESET

        art = TITLE_ART.splitlines()
        width = max(len(line) for line in art)
        # the art needs room for itself, the margins and the timer row below it
        if width > inner or len(art) + 2 * margin + 4 > rows:
            art, width = [PLAIN_TITLE], len(PLAIN_TITLE)
        col = margin + 1 + max(0, (inner - width) // 2)
        out += TITLE_COLOUR
        for i, line in enumerate(art):
            out += _at(margin + 2 + i, col, line)
        return out + RESET

    def _timer_row(self, timers, cols, rows):
        margin = 1 if SHOW_BORDER else 0
        inner = cols - 2 * margin
        texts = []
        for label, seconds, active in timers:
            mins, secs = divmod(seconds, 60)
            texts.append((f"{label}: {mins:02d}:{secs:02d}", active))
        plain = " | ".join(text for text, _ in texts)
        if len(plain) > inner:  # too narrow for both, so only show the active timer
            texts = [item for item in texts if item[1]]
            plain = " | ".join(text for text, _ in texts)
        coloured = " | ".join(
            f"{ACTIVE_COLOUR}{text}{RESET}" if active else text for text, active in texts
        )
        left = max(0, (inner - len(plain)) // 2)
        right = max(0, inner - left - len(plain))
        # the padding clears whatever the previous frame left on this row
        return _at(max(1, rows - margin - 1), margin + 1, " " * left + coloured + " " * right)
