import json
import os
import uuid
from datetime import datetime

STORAGE_FILE = "entries.json"

def load_entries():
    if not os.path.exists(STORAGE_FILE):
        return []
    with open(STORAGE_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_entries(entries):
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

def add_entry(text, tag="general"):
    entries = load_entries()
    entry = {
        "id": str(uuid.uuid4())[:8],
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "tag": tag,
        "text": text,
    }
    entries.append(entry)
    save_entries(entries)
    return entry

def search_entries(tag=None):
    entries = load_entries()
    if tag:
        entries = [e for e in entries if e.get("tag") == tag]
    return entries

def edit_entry(entry_id, new_text=None, new_tag=None):
    entries = load_entries()
    updated = None
    for entry in entries:
        if entry.get("id") == entry_id:
            if new_text:
                entry["text"] = new_text
            if new_tag:
                entry["tag"] = new_tag
            updated = entry
            break
    if updated:
        save_entries(entries)
    return updated

def delete_entry(entry_id):
    entries = load_entries()
    new_entries = [e for e in entries if e.get("id") != entry_id]
    if len(new_entries) == len(entries):
        return False
    save_entries(new_entries)
    return True
