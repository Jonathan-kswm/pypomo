# All of the sounds for the pomodoro timer. Uses the system's own player and sounds, so there is nothing to install:
# afplay with the built-in sounds on macOS, and paplay with the freedesktop sounds on Linux.
import subprocess
import sys

if sys.platform == "darwin":
    PLAYER = "afplay"
    BELL = "/System/Library/Sounds/Glass.aiff"
    TICK = "/System/Library/Sounds/Tink.aiff"
else:
    PLAYER = "paplay"
    BELL = "/usr/share/sounds/freedesktop/stereo/complete.oga"
    TICK = "/usr/share/sounds/freedesktop/stereo/onboard-key-feedback.oga"


class Sound:
    def __init__(self, bell=BELL, tick=TICK):
        self.bell_file = bell  # path to the bell sound file
        self.tick_file = tick  # path to the ticking sound file

    def _play(self, path):
        # Popen, not run: the sound plays in the background so the timer never pauses
        try:
            subprocess.Popen([PLAYER, path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            pass  # no player installed: stay silent rather than crash the timer

    def bell(self):
        self._play(self.bell_file)

    def tick(self):
        self._play(self.tick_file)
