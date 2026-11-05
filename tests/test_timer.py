from pypomo.timer import GREEN, Timer
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
    threading.Timer(1.5, _thread.interrupt_main).start()
    Timer(0.01, 0).start()
    out = capsys.readouterr().out
    assert GREEN + "Work: 00:01" in out
    assert GREEN + "Break: 00:00" in out
    assert out.endswith("\n")


def test_timers_appear_in_place(capsys):
    threading.Timer(0.1, _thread.interrupt_main).start()
    Timer(0.01, 0).start()
    out = capsys.readouterr().out
    assert "Work: 00:01" in out
    assert "Break: 00:00" in out
    assert out.count("\n") == 2  # only the "Timer stopped." message adds lines

