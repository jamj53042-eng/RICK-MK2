from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Optional
from .storage import Storage

storage = Storage()

def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()

def add_quest(title: str, desc: str) -> dict[str, Any]:
    data = storage.load()
    quests = data.get("quests", [])
    next_id = max((q.get("id", 0) for q in quests), default=0) + 1
    quest = {
        "id": next_id,
        "created": _now_iso(),
        "title": title,
        "desc": desc,
        "status": "active",   # "active" | "done"
        "done_at": None,
    }
    quests.append(quest)
    data["quests"] = quests
    storage.save(data)
    return quest

def list_quests(status: Optional[str] = None) -> list[dict[str, Any]]:
    data = storage.load()
    quests = data.get("quests", [])
    if status is None:
        return quests
    return [q for q in quests if q.get("status") == status]

def complete_quest(quest_id: int) -> bool:
    data = storage.load()
    quests = data.get("quests", [])
    for q in quests:
        if q.get("id") == quest_id and q.get("status") != "done":
            q["status"] = "done"
            q["done_at"] = _now_iso()
            storage.save(data)
            return True
    return False

def delete_quest(quest_id: int) -> bool:
    data = storage.load()
    quests = data.get("quests", [])
    new_quests = [q for q in quests if q.get("id") != quest_id]
    if len(new_quests) == len(quests):
        return False
    data["quests"] = new_quests
    storage.save(data)
    return True

def clear_quests(status: Optional[str] = None, all_: bool = False) -> int:
    data = storage.load()
    quests = data.get("quests", [])
    if all_:
        removed = len(quests)
        data["quests"] = []
        if removed:
            storage.save(data)
        return removed
    if status not in {"active", "done"}:
        return 0
    new_quests = [q for q in quests if q.get("status") != status]
    removed = len(quests) - len(new_quests)
    if removed:
        data["quests"] = new_quests
        storage.save(data)
    return removed
