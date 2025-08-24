from Rick_MK2.status import show_status
from Rick_MK2.log import add_log

def test_status_default(capsys):
    show_status()
    captured = capsys.readouterr()
    assert "Streak" in captured.out

def test_log(capsys):
    add_log("Test Task")
    captured = capsys.readouterr()
    assert "Test Task" in captured.out
