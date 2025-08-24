from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Optional
from .storage import Storage

storage = Storage()

def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()

def log_entry(text: str, tag: str) -> dict[str, Any]:
    data = storage.load()
    logs = data.get("logs", [])
    next_id = max((e.get("id", 0) for e in logs), default=0) + 1
    entry = {"id": next_id, "timestamp": _now_iso(), "tag": tag, "text": text}
    logs.append(entry)
    data["logs"] = logs
    storage.save(data)
    return entry

def search_entries_by_tag(tag: str) -> list[dict[str, Any]]:
    data = storage.load()
    return [e for e in data.get("logs", []) if e.get("tag") == tag]

def update_entry(entry_id: int, new_text: Optional[str], new_tag: Optional[str]) -> bool:
    data = storage.load()
    updated = False
    for e in data.get("logs", []):
        if e.get("id") == entry_id:
            if new_text is not None:
                e["text"] = new_text
            if new_tag is not None:
                e["tag"] = new_tag
            updated = True
            break
    if updated:
        storage.save(data)
    return updated

def remove_entry(entry_id: int) -> bool:
    data = storage.load()
    logs = data.get("logs", [])
    new_logs = [e for e in logs if e.get("id") != entry_id]
    if len(new_logs) == len(logs):
        return False
    data["logs"] = new_logs
    storage.save(data)
    return True

def clear_entries_by_tag(tag: str) -> int:
    data = storage.load()
    logs = data.get("logs", [])
    new_logs = [e for e in logs if e.get("tag") != tag]
    removed = len(logs) - len(new_logs)
    if removed > 0:
        data["logs"] = new_logs
        storage.save(data)
    return removed

def clear_all_entries() -> int:
    data = storage.load()
    count = len(data.get("logs", []))
    if count:
        data["logs"] = []
        storage.save(data)
    return count
