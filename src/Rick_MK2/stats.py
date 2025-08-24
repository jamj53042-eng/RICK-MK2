from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
from .storage import Storage

storage = Storage()

XP_VALUES: dict[str, int] = {
    "easy": 2,
    "medium": 5,
    "hard": 10,
}

def _today_local():
    return datetime.now(timezone.utc).astimezone().date()

def take_challenge(difficulty: str) -> str:
    difficulty = difficulty.lower()
    if difficulty not in XP_VALUES:
        return f"Unknown difficulty: {difficulty}"

    data = storage.load()
    gained = XP_VALUES[difficulty]

    # Streak handling
    today = _today_local()
    last_update = data.get("last_update")
    if last_update:
        try:
            last_day = datetime.fromisoformat(last_update).date()
        except Exception:
            last_day = None
    else:
        last_day = None

    if last_day is None:
        data["streak"] = 1
    else:
        if today == last_day:
            # same day: keep current streak
            data["streak"] = int(data.get("streak", 0)) or 1
        elif (today - last_day).days == 1:
            data["streak"] = int(data.get("streak", 0)) + 1
        else:
            data["streak"] = 1

    if data["streak"] > int(data.get("best_streak", 0)):
        data["best_streak"] = data["streak"]

    bonus_per = int(data.get("bonus_per_streak", 5))
    bonus_cap = int(data.get("bonus_cap", 100))
    bonus = min(data["streak"] * bonus_per, bonus_cap)

    data["xp"] = int(data.get("xp", 0)) + gained + bonus
    data["level"] = 1 + (data["xp"] // 100)
    data["last_update"] = datetime.now(timezone.utc).astimezone().isoformat()

    storage.save(data)

    return (
        f"Rick takes on a {difficulty} challenge... 🗡️`n"
        f"Gained {gained} XP (+{bonus} streak bonus).`n"
        f"Total XP: {data['xp']} | Level: {data['level']} | "
        f"Streak: {data['streak']} (Best: {data['best_streak']})"
    )

def xp_status() -> str:
    d = storage.load()
    return (
        f"XP: {int(d.get('xp',0))} | Level: {int(d.get('level',1))}`n"
        f"Streak: {int(d.get('streak',0))} (Best: {int(d.get('best_streak',0))})"
    )
