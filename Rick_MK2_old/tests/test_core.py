from Rick_MK2.cli import tracker, logger

def test_status_output(capsys):
    tracker.get_status()
    streak, bonus = tracker.get_status()
    assert isinstance(streak, int)
    assert isinstance(bonus, int)

def test_log_and_status():
    entry = logger.add_entry("Test Task")
    assert "Test Task" in entry
    today_entries = logger.get_today_entries()
    assert "Test Task" in today_entries
