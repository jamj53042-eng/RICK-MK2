import json, os
from pathlib import Path
from Rick_MK2.rick import RickMK2

def test_basic_flow(tmp_path, monkeypatch):
    # Use temp HOME for isolation
    fake_home = tmp_path / "home"
    fake_home.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("HOME", str(fake_home))

    rick = RickMK2()

    # Initial status should not crash
    out = rick.status()
    assert "STATUS" in out

    # Log a success and check streak increments
    rick.log("✔️ Completed Unit Test (+10%)")
    data = rick.storage.load()
    assert data["streak"] >= 1

    # Undo should remove last entry but not rewind streak
    streak_before = data["streak"]
    rick.undo()
    data2 = rick.storage.load()
    assert len(data2["logs"]) == len(data["logs"]) - 1
    assert data2["streak"] == streak_before

    # Reset streak
    rick.reset("streak")
    data3 = rick.storage.load()
    assert data3["streak"] == 0
