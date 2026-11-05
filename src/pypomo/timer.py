# This will be the main location for the timer functions for the pomodoro timer
import time


class Timer:
    def __init__(self, work, pause):
        self.work = work  # amount of time for work (minutes)
        self.pause = pause  # amount of time for a break (minutes)

    def start(self):
        # countdown timer that prints to the terminal, updating in place
        total_seconds = int(self.work * 60)
        end_time = time.monotonic() + total_seconds
        try:
            while True:
                remaining = max(0, round(end_time - time.monotonic()))
                mins, secs = divmod(remaining, 60)
                # \r returns the cursor to the line start so the next print overwrites it
                print(f"\rWork: {mins:02d}:{secs:02d}", end="", flush=True)
                if remaining == 0:
                    break
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nTimer cancelled.")
            return
        print()
