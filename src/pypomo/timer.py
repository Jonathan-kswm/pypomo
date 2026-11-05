# This will be the main location for the timer functions for the pomodoro timer
import time

GREEN = "\033[32m"
RESET = "\033[0m"


class Timer:
    def __init__(self, work, pause, sound=None):
        self.work = work  # amount of time for work (minutes)
        self.pause = pause  # amount of time for a break (minutes)
        self.sound = sound  # a Sound to play when the timer changes, or None for silence

    @staticmethod
    def _format(label, seconds, active):
        mins, secs = divmod(seconds, 60)
        text = f"{label}: {mins:02d}:{secs:02d}"
        return f"{GREEN}{text}{RESET}" if active else text

    def start(self):
        # Work and Break are redrawn in place, side by side on one line.
        # The active timer is green; when it hits zero the other one takes over.
        phases = [("Work", round(self.work * 60)), ("Break", round(self.pause * 60))]
        active = 0
        phase_start = time.monotonic()
        try:
            while True:
                # whole seconds since the phase began, so every value, including
                # the starting time and 00:00, stays on screen for one full second
                remaining = phases[active][1] - int(time.monotonic() - phase_start)
                if remaining < 0:
                    # 00:00 has had its second: switch to the other timer, and the
                    # finished one shows its full time again
                    active = 1 - active
                    phase_start = time.monotonic()
                    remaining = phases[active][1]
                    if self.sound:
                        self.sound.bell()
                lines = []
                for i, (label, total) in enumerate(phases):
                    is_active = i == active
                    lines.append(self._format(label, remaining if is_active else total, is_active))
                # \r overwrites the current line, so no new lines are added
                print("\r" + " | ".join(lines) + "   ", end="", flush=True)
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nTimer stopped.")
