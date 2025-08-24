from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Literal
from zoneinfo import ZoneInfo
import re

from .storage import Storage
from . import templates

Mode = Optional[Literal["daily", "weekly", "full"]]

CHECK = "✔️"
CROSS = "❌"

def _local_tz() -> ZoneInfo:
    try:
        return ZoneInfo("America/Vancouver")
    except Exception:
        # Fallback to system local time if ZoneInfo key unavailable
        return ZoneInfo("UTC")

@dataclass
class RickMK2:
    storage: Storage = field(default_factory=Storage)
    tz: ZoneInfo = field(default_factory=_local_tz)

    def _now(self) -> datetime:
        return datetime.now(self.tz)

    # ---- Core state helpers ----
    def _load(self) -> dict:
        return self.storage.load()

    def _save(self, data: dict) -> None:
        data["last_update"] = self._now().isoformat()
        self.storage.save(data)

    @staticmethod
    def _calc_bonus(streak: int, per: int, cap: int) -> int:
        return min(streak * per, cap)

    # ---- Public API ----
    def status(self, mode: Mode = None) -> str:
        data = self._load()
        streak = int(data.get("streak", 0))
        best = int(data.get("best_streak", 0))
        per = int(data.get("bonus_per_streak", 5))
        cap = int(data.get("bonus_cap", 100))
        last_iso = data.get("last_update")
        last_update = datetime.fromisoformat(last_iso) if last_iso else self._now()

        bonus = self._calc_bonus(streak, per, cap)
        logs = data.get("logs", [])

        # Last 3 logs
        last3 = []
        for item in logs[-3:]:
            ts = datetime.fromisoformat(item["timestamp"])
            last3.append((item["text"], ts))

        block = templates.status_block(
            status="Active",
            streak=streak,
            bonus_pct=bonus,
            best=best,
            last_update=last_update,
            last3=last3,
            tz=self.tz,
        )

        if mode is None:
            return block

        extras = []
        if mode in ("daily", "full"):
            extras.append(self._render_daily(logs))
        if mode in ("weekly", "full"):
            extras.append(self._render_weekly(logs))
        return block + ("\n\n" + "\n\n".join(x for x in extras if x)) if extras else block

    def log(self, text: str) -> None:
        """Append a manual log entry. If the text begins with ✔️ it increments the streak, if it begins with ❌ it resets streak to 0. Otherwise, streak unchanged."""
        data = self._load()
        logs = data.setdefault("logs", [])

        ts = self._now().isoformat()
        logs.append({"text": text, "timestamp": ts})

        # Update streak logic
        if text.strip().startswith(CHECK):
            data["streak"] = int(data.get("streak", 0)) + 1
            data["best_streak"] = max(int(data.get("best_streak", 0)), int(data["streak"]))
        elif text.strip().startswith(CROSS):
            data["streak"] = 0

        self._save(data)

    def undo(self, n: int = 1) -> None:
        """Remove last N entries only (does not rewind streak/bonus by design)."""
        if n < 1:
            return
        data = self._load()
        logs = data.get("logs", [])
        if not logs:
            return
        del logs[-n:]
        self._save(data)

    def reset(self, scope: Literal["streak", "log", "all"]) -> None:
        data = self._load()
        if scope == "streak":
            data["streak"] = 0
        elif scope == "log":
            data["logs"] = []
        elif scope == "all":
            data["streak"] = 0
            data["logs"] = []
            data["best_streak"] = 0
        self._save(data)

    # ---- Rendering helpers ----
    def _render_daily(self, logs: list[dict]) -> str:
        if not logs:
            return "No logs yet."
        # Group by local date
        by_date: dict[str, list[dict]] = {}
        for item in logs:
            dt = datetime.fromisoformat(item["timestamp"]).astimezone(self.tz)
            dkey = dt.date().isoformat()
            by_date.setdefault(dkey, []).append(item)

        # Today only
        today_key = self._now().date().isoformat()
        today = by_date.get(today_key, [])
        if not today:
            return "No logs for today yet."

        items: list[str] = []
        completed = skipped = 0
        for item in today:
            dt = datetime.fromisoformat(item["timestamp"])
            label = f"{item['text']} [{dt.astimezone(self.tz).strftime('%I:%M %p')}]"
            items.append(label)
            if item["text"].strip().startswith(CHECK):
                completed += 1
            elif item["text"].strip().startswith(CROSS):
                skipped += 1

        # daily bonus is current streak-based
        data = self._load()
        per = int(data.get("bonus_per_streak", 5))
        cap = int(data.get("bonus_cap", 100))
        bonus = self._calc_bonus(int(data.get('streak', 0)), per, cap)
        summary = f"{completed} completed | {skipped} skipped | +{bonus}% bonus"
        date_label = datetime.fromisoformat(today[0]["timestamp"]).astimezone(self.tz).strftime("%b %d, %Y")
        return templates.day_section(date_label, items, summary)

    def _render_weekly(self, logs: list[dict]) -> str:
        if not logs:
            return "No logs yet."
        # Determine current week (Monday start, Sunday end)
        now = self._now()
        start_of_week = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)

        completed = skipped = 0
        # Calculate daily average bonus: average of current-streak-based bonus for each day that had logs
        per_day_bonus: list[int] = []
        # Track streak high (best streak overall)
        data = self._load()
        streak_high = int(data.get("best_streak", 0))
        per = int(data.get("bonus_per_streak", 5))
        cap = int(data.get("bonus_cap", 100))

        # Group logs by day within the week
        by_day: dict[str, list[dict]] = {}
        for item in logs:
            dt = datetime.fromisoformat(item["timestamp"]).astimezone(self.tz)
            if start_of_week <= dt <= end_of_week:
                key = dt.date().isoformat()
                by_day.setdefault(key, []).append(item)
                if item["text"].strip().startswith(CHECK):
                    completed += 1
                elif item["text"].strip().startswith(CROSS):
                    skipped += 1

        for day_key, items in by_day.items():
            # For each day, compute bonus based on final streak value of that day (approximate = current streak)
            current_bonus = self._calc_bonus(int(data.get("streak", 0)), per, cap)
            per_day_bonus.append(current_bonus)

        avg_bonus = round(sum(per_day_bonus) / len(per_day_bonus)) if per_day_bonus else 0
        span_label = f"{start_of_week.strftime('%b %d')}–{end_of_week.strftime('%b %d, %Y')}"
        return templates.weekly_section(span_label, completed, skipped, streak_high, avg_bonus)
