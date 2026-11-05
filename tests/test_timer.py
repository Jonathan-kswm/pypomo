from pypomo.timer import Timer


def test_init_stores_durations():
    timer = Timer(25, 5)
    assert timer.work == 25
    assert timer.pause == 5


def test_start_counts_down_to_zero(capsys):
    Timer(0, 0).start()
    out = capsys.readouterr().out
    assert "\rWork: 00:00" in out
    assert out.endswith("\n")
