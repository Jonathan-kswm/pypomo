# This will be the main location for the timer functions for the pomodoro timer
import time


class Timer:
    def __init__(self, work, pause):
        self.work = work  # amount of time for work (minutes)
        self.pause = pause  # amount of time for a break (minutes)

    def _countdown(self, minutes, label):
        """Count down `minutes`, printing MM:SS in place on one terminal line."""
        end_time = time.monotonic() + minutes * 60
        while True:
            remaining = max(0, round(end_time - time.monotonic()))
            mins, secs = divmod(remaining, 60)
            # \r returns the cursor to the line start so the next print overwrites it;
            # trailing spaces clear leftovers when switching to a shorter label
            print(f"\r{label}: {mins:02d}:{secs:02d}   ", end="", flush=True)
            if remaining == 0:
                break
            time.sleep(0.1)
        print()

    def start(self):
        # alternate work and break countdowns until a keyboard interrupt (Ctrl+C)
        try:
            while True:
                self._countdown(self.work, "Work")
                self._countdown(self.pause, "Break")
        except KeyboardInterrupt:
            print("\nTimer stopped.")
