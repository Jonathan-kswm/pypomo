# This will be the main location for the timer functions for the pomodoro timer
import math
import os
import sys
import time

GREEN = "\033[32m"
RESET = "\033[0m"
CLEAR_LINE = "\033[2K"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CURSOR_UP = "\033[1A"


def _can_move_cursor():
    """True in a real terminal. PyCharm's consoles can't move the cursor up a line."""
    return sys.stdout.isatty() and "PYCHARM_HOSTED" not in os.environ


class Timer:
    def __init__(self, work, pause):
        self.work = work  # amount of time for work (minutes)
        self.pause = pause  # amount of time for a break (minutes)

    @staticmethod
    def _format(label, seconds, active):
        mins, secs = divmod(seconds, 60)
        text = f"{label}: {mins:02d}:{secs:02d}"
        return f"{GREEN}{text}{RESET}" if active else text

    def start(self):
        # Redrawn in place: Work above Break in a real terminal, or side by side on
        # one line in consoles that can't move the cursor up.
        # The active timer is green; when it hits zero the other one takes over.
        phases = [("Work", round(self.work * 60)), ("Break", round(self.pause * 60))]
        active = 0
        end_time = time.monotonic() + phases[active][1]
        two_lines = _can_move_cursor()
        if two_lines:
            print(HIDE_CURSOR, end="")
        try:
            while True:
                # ceil, not round: round hits 0 with half a second still left
                remaining = math.ceil(end_time - time.monotonic())
                if remaining <= 0:
                    # switch to the other timer; the finished one shows its full time again
                    active = 1 - active
                    end_time = time.monotonic() + phases[active][1]
                    remaining = phases[active][1]
                lines = []
                for i, (label, total) in enumerate(phases):
                    is_active = i == active
                    lines.append(self._format(label, remaining if is_active else total, is_active))
                if two_lines:
                    # draw both lines, then return the cursor to the start of line 1
                    frame = "\n".join(CLEAR_LINE + line for line in lines) + CURSOR_UP + "\r"
                else:
                    # \r overwrites the current line, so no new lines are added
                    frame = "\r" + " | ".join(lines) + "   "
                print(frame, end="", flush=True)
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            if two_lines:
                # leave the cursor below the two lines and restore it
                print("\n\nTimer stopped." + SHOW_CURSOR)
            else:
                print("\nTimer stopped.")
