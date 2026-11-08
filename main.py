# Here will be the main file to run with uv run main with argparse
import argparse
import sys

from pypomo.design import FullScreen
from pypomo.sound import Sound
from pypomo.timer import Timer


def main():
    parser = argparse.ArgumentParser(description="Pomodoro timer. Press Ctrl+C to stop.")
    parser.add_argument("work", type=float, help="work time in minutes")
    parser.add_argument("pause", type=float, help="break time in minutes")
    parser.add_argument("-s", "--simple", action="store_true", help="use the one-line timer")
    args = parser.parse_args()
    # full screen needs a real terminal, so anything else gets the one-line timer
    if args.simple or not sys.stdout.isatty():
        Timer(args.work, args.pause, Sound()).start()
    else:
        with FullScreen() as screen:
            Timer(args.work, args.pause, Sound(), display=screen).start()


if __name__ == "__main__":
    main()

# Test to check if upstream is working
