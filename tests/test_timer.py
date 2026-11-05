from pypomo.timer import Timer
import time
import threading
import _thread

def test_init_stores_durations():
    timer = Timer(25, 5)
    assert timer.work == 25
    assert timer.pause == 5


def test_start_counts_down_to_zero(capsys):
    threading.Timer(0.1, _thread.interrupt_main).start()
    Timer(0, 0).start()
    out = capsys.readouterr().out
    assert "\rWork: 00:00" in out
    assert out.endswith("\n")


def test_timer_changes(capsys):
    threading.Timer(1, _thread.interrupt_main).start()
    Timer(0.01, 0).start()
    out = capsys.readouterr().out
    assert "\rWork: 00:00" in out
    time.sleep(0.01)
    assert "\rBreak: 00:00" in out
    assert out.endswith("\n")
