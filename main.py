# Here will be the main file to run with uv run main with argparse
import argparse

from pypomo.timer import Timer


def main():
    parser = argparse.ArgumentParser(description="Pomodoro timer. Press Ctrl+C to stop.")
    parser.add_argument("work", type=float, help="work time in minutes")
    parser.add_argument("pause", type=float, help="break time in minutes")
    args = parser.parse_args()
    Timer(args.work, args.pause).start()


if __name__ == "__main__":
    main()
