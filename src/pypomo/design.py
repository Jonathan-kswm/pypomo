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
TIMER_SEPARATOR = "  │  "  # goes between the Work and Break timers
# the large timer font: every character is three rows of equal width
TIMER_FONT = {
    "0": ("┌─┐", "│ │", "└─┘"),
    "1": (" ┐ ", " │ ", " ┴ "),
    "2": ("┌─┐", "┌─┘", "└─┘"),
    "3": ("┌─┐", " ─┤", "└─┘"),
    "4": ("╷ ╷", "└─┤", "  ╵"),
    "5": ("┌─┐", "└─┐", "└─┘"),
    "6": ("┌─┐", "├─┐", "└─┘"),
    "7": ("┌─┐", "  │", "  ╵"),
    "8": ("┌─┐", "├─┤", "└─┘"),
    "9": ("┌─┐", "└─┤", "└─┘"),
    ":": (" ", ":", " "),
}

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


def _clock(seconds):
    mins, secs = divmod(seconds, 60)
    return f"{mins:02d}:{secs:02d}"


def _large(label, seconds):
    """The label above the time in the large font, as a list of equal-width rows."""
    clock = _clock(seconds)
    rows = [" ".join(TIMER_FONT[char][row] for char in clock) for row in range(3)]
    return [label.center(len(rows[0]))] + rows


def _small(label, seconds):
    return [f"{label}: {_clock(seconds)}"]


def _side_by_side(timers, block):
    """Join each timer's rows into (plain text, coloured text) pairs, one pair per row."""
    blocks = [(block(label, seconds), active) for label, seconds, active in timers]
    rows = []
    for i in range(len(blocks[0][0])):
        parts = [(lines[i], active) for lines, active in blocks]
        plain = TIMER_SEPARATOR.join(text for text, _ in parts)
        coloured = TIMER_SEPARATOR.join(
            f"{ACTIVE_COLOUR}{text}{RESET}" if active else text for text, active in parts
        )
        rows.append((plain, coloured))
    return rows


class FullScreen:
    """Takes over the terminal inside a `with` block and restores it afterwards."""

    def __init__(self):
        self._size = None  # the terminal size the border and title were last drawn at
        self._title_end = 0  # the last screen row used by the title

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
        frame += self._timer_area(timers, size.columns, size.lines)
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
        self._title_end = margin + 1 + len(art)
        return out + RESET

    def _timer_area(self, timers, cols, rows):
        """Centre the timers in the space between the title and the bottom of the screen."""
        margin = 1 if SHOW_BORDER else 0
        inner = cols - 2 * margin
        top = self._title_end + 1
        bottom = rows - margin
        space = bottom - top + 1

        # the biggest layout that fits, falling back to only the active timer
        active = [timer for timer in timers if timer[2]]
        layouts = [(timers, _large), (timers, _small), (active, _small)]
        for shown, block in layouts:
            lines = _side_by_side(shown, block)
            if len(lines) <= space and len(lines[0][0]) <= inner:
                break

        start = top + max(0, (space - len(lines)) // 2)
        out = ""
        # every row in the space is rewritten, which clears anything left by the last frame
        for row in range(top, bottom + 1):
            index = row - start
            if 0 <= index < len(lines):
                plain, coloured = lines[index]
                left = max(0, (inner - len(plain)) // 2)
                right = max(0, inner - left - len(plain))
                out += _at(row, margin + 1, " " * left + coloured + " " * right)
            else:
                out += _at(row, margin + 1, " " * inner)
        return out
