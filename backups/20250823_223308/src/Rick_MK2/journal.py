import json
from datetime import datetime
from pathlib import Path

JOURNAL_FILE = Path("journal.json")

def _load_entries():
    if JOURNAL_FILE.exists():
        with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def _save_entries(entries):
    with open(JOURNAL_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

def log_entry(text, tag=None):
    """Save a new journal entry."""
    entries = _load_entries()
    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "text": text,
        "tag": tag
    }
    entries.append(entry)
    _save_entries(entries)

def search_entries(text=None, tag=None):
    """Return a list of matching entries."""
    entries = _load_entries()
    results = []
    for e in entries:
        if (text and text.lower() in e["text"].lower()) or (tag and e["tag"] == tag):
            results.append(e)
    return results

def status_report(level="summary", compact=False):
    """Return entries or summary stats depending on level."""
    entries = _load_entries()
    if not entries:
        return {"summary": "No entries logged yet.", "entries": []}

    if compact:
        return {
            "summary": f"📊 Total entries: {len(entries)}",
            "entries": [
                {"index": i+1, "text": e["text"], "tag": e["tag"]}
                for i, e in enumerate(entries)
            ]
        }

    if level == "summary":
        return {"summary": f"📊 Total entries: {len(entries)}", "entries": []}
    elif level == "full":
        return {"summary": f"📊 Total entries: {len(entries)}", "entries": entries}

def clear_entries():
    """Delete all journal entries."""
    _save_entries([])
    return "🧹 Journal cleared."
