# All of the sounds for the pomodoro timer. Uses macOS's afplay, so there is nothing to install.
import subprocess

BELL = "/System/Library/Sounds/Glass.aiff"
TICK = "/System/Library/Sounds/Tink.aiff"


class Sound:
    def __init__(self, bell=BELL, tick=TICK):
        self.bell_file = bell  # path to the bell sound file
        self.tick_file = tick  # path to the ticking sound file

    def _play(self, path):
        # Popen, not run: the sound plays in the background so the timer never pauses
        subprocess.Popen(["afplay", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def bell(self):
        self._play(self.bell_file)

    def tick(self):
        self._play(self.tick_file)
