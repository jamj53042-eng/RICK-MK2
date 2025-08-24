from __future__ import annotations
from typing import Any, Optional
from datetime import datetime, timezone
from .storage import Storage

storage = Storage()

def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()

def _next_id(items: list[dict[str, Any]]) -> int:
    return max((e.get("id", 0) for e in items), default=0) + 1

def add_quest(title: str, desc: str) -> dict[str, Any]:
    data = storage.load()
    quests = data.get("quests", [])
    q = {
        "id": _next_id(quests),
        "title": title,
        "desc": desc,
        "status": "active",
        "created": _now_iso(),
        "completed": None,
    }
    quests.append(q)
    data["quests"] = quests
    storage.save(data)
    return q

def list_quests(status: Optional[str] = None) -> list[dict[str, Any]]:
    data = storage.load()
    quests = data.get("quests", [])
    if status:
        return [q for q in quests if q.get("status") == status]
    return quests

def complete_quest(qid: int) -> bool:
    data = storage.load()
    for q in data.get("quests", []):
        if q.get("id") == qid and q.get("status") != "done":
            q["status"] = "done"
            q["completed"] = _now_iso()
            storage.save(data)
            return True
    return False

def delete_quest(qid: int) -> bool:
    data = storage.load()
    quests = data.get("quests", [])
    new_quests = [q for q in quests if q.get("id") != qid]
    if len(new_quests) == len(quests):
        return False
    data["quests"] = new_quests
    storage.save(data)
    return True

def clear_quests() -> int:
    data = storage.load()
    n = len(data.get("quests", []))
    data["quests"] = []
    storage.save(data)
    return n
