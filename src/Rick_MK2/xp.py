from .storage import Storage
from datetime import date

def gain_xp(amount: int) -> int:
    """Gain XP with dynamic streak bonus. Returns new total XP."""
    data = Storage().load()
    stats = data.setdefault("stats", {})
    current = stats.get("xp", 0)

    # --- Streak tracking ---
    today = str(date.today())
    last_day = stats.get("last_challenge_day")
    streak = stats.get("streak_count", 0)

    if last_day == today:
        # already did a challenge today → streak unchanged
        pass
    elif last_day is None or (last_day != today):
        if last_day is None:
            streak = 1
        else:
            # reset if skipped a day
            from datetime import datetime, timedelta
            try:
                last = datetime.strptime(last_day, "%Y-%m-%d").date()
                if (date.today() - last).days == 1:
                    streak += 1
                else:
                    streak = 1
            except Exception:
                streak = 1
    stats["last_challenge_day"] = today
    stats["streak_count"] = streak

    # --- Bonus calculation ---
    streak_bonus = min(streak * 2, 20)
    total_gain = amount + streak_bonus
    new_total = current + total_gain

    stats["xp"] = new_total
    Storage().save(data)
    return new_total

def get_xp() -> int:
    data = Storage().load()
    stats = data.get("stats", {})
    return stats.get("xp", 0)

def get_streak() -> int:
    data = Storage().load()
    stats = data.get("stats", {})
    return stats.get("streak_count", 0)
