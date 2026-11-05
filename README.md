# pypomo

A simple pomodoro timer for the terminal, written in Python.

It alternates between work and break countdowns on a single line that updates in place. The active timer is shown in green, and a bell rings each time the timer changes.

```
Work: 24:59 | Break: 05:00
```

## Requirements

- macOS (sounds are played with the built-in `afplay` command)
- [uv](https://docs.astral.sh/uv/)
- Python 3.12 or newer

## Installation

```
git clone git@github.com:Jonathan-kswm/pypomo.git
cd pypomo
uv sync
```

## Usage

From the project root, give the work time and then the break time, both in minutes:

```
uv run main.py 25 5
```

The timer keeps cycling between work and break until you press Ctrl+C.

Decimals are allowed, so `uv run main.py 0.5 0.1` is a quick way to try it out.

## Customising the sounds

The sounds live in the `Sound` class in `src/pypomo/sound.py`. By default it uses macOS system sounds, and you can pass in your own files:

```python
from pypomo.sound import Sound
from pypomo.timer import Timer

Timer(25, 5, Sound(bell="my_bell.mp3")).start()
```

`Sound` also has a ticking noise, `Sound().tick()`, which the timer doesn't use yet.

## Running the tests

From the project root:

```
uv run pytest
```

## Licence

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
