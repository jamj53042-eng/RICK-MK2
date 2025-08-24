from __future__ import annotations
from datetime import datetime
from zoneinfo import ZoneInfo

def fmt_dt(dt: datetime, tz: ZoneInfo | None = None) -> str:
    if tz:
        dt = dt.astimezone(tz)
    return dt.strftime("%b %d, %Y - %I:%M %p")

def fmt_time(dt: datetime, tz: ZoneInfo | None = None) -> str:
    if tz:
        dt = dt.astimezone(tz)
    return dt.strftime("%-I:%M %p") if hasattr(dt, "strftime") else str(dt)

def status_block(status: str, streak: int, bonus_pct: int, best: int, last_update: datetime, last3: list[tuple[str, datetime]], tz: ZoneInfo | None) -> str:
    header = "══════════════════════════════"
    lines = [header]
    lines.append(f"✅ STATUS: {status.upper()}")
    lines.append(f"🔥 Streak: {streak}     🎯 Bonus: +{bonus_pct}%     🏆 Best: {best}")
    lines.append(f"🕒 Last update: {fmt_dt(last_update, tz)}")
    lines.append("──────────────────────────────")
    lines.append("Last 3 Logs:")
    if not last3:
        lines.append("(no recent logs)")
    else:
        for i, (text, ts) in enumerate(last3, start=1):
            # Each log shows date + time per your preference
            lines.append(f"{i}️⃣ {text} [{fmt_dt(ts, tz)}]")
    lines.append(header)
    return "\n".join(lines)

def day_section(date_label: str, items: list[str], summary: str) -> str:
    header = "══════════════════════════════"
    lines = [header]
    lines.append(f"📅 {date_label}")
    lines.extend([f"   {line}" for line in items])
    lines.append(f"   --- Summary: {summary} ---")
    lines.append(header)
    return "\n".join(lines)

def weekly_section(span_label: str, completed: int, skipped: int, streak_high: int, avg_bonus: int) -> str:
    header = "══════════════════════════════"
    lines = [header]
    lines.append(f"📊 WEEKLY OVERVIEW ({span_label})")
    lines.append(f"✔️ Completed: {completed}")
    lines.append(f"❌ Skipped:   {skipped}")
    lines.append(f"🔥 Streak high: {streak_high}")
    lines.append(f"🎯 Avg daily bonus: +{avg_bonus}%")
    lines.append(header)
    return "\n".join(lines)

def reset_prompt(scope: str) -> str:
    return (f"⚠️ Are you sure you want to reset {scope}?\n"
            f"Type YES to confirm.")

def undo_feedback(n: int) -> str:
    return f"↩️ Removed the last {n} log entr{'y' if n==1 else 'ies'}."
