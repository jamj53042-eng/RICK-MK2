# --- auto-added: silence module prints; CLI handles all user output ---
def _silent_print(*args, **kwargs):
    pass
import json
import csv
from datetime import datetime
from pathlib import Path

from tempfile import NamedTemporaryFile
import os
DATA_FILE = Path(__file__).resolve().parents[2] / "data.json"

class Logger:
    def __init__(self):
        self.data = {"logs": []}
        if DATA_FILE.exists():
            try:
                self.data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                self.data = {"logs": []}

    def save(self):

        _atomic_write_json(DATA_FILE, self.data)

    def add_log(self, entry, tag=None):
        log = {
            "text": entry,
            "time": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
            "tag": tag or ""
        }
        self.data["logs"].append(log)
        self.save()

    def undo(self, count=1):
        if len(self.data["logs"]) == 0:
            _silent_print("âš ï¸ No logs to undo.")
            return
        removed = self.data["logs"][-count:]
        self.data["logs"] = self.data["logs"][:-count]
        self.save()
        for r in removed:
            _silent_print(f"ðŸ—‘ï¸ Removed: {r['text']} [tag: {r['tag']}]")

    def reset(self, scope):
        if scope == "log" or scope == "all":
            self.data["logs"] = []
        self.save()
        _silent_print(f"âœ… Reset {scope}")

    def search_logs(self, tag=None, text=None):

        """Return a list of log dicts filtered by tag/text; never prints."""

        try:

            data = json.loads(DATA_FILE.read_text(encoding="utf-8")) if DATA_FILE.exists() else {}

            logs = data.get("logs", [])

        except Exception:

            return []

        def match(log):

            ok = True

            if tag:

                ok = ok and log.get("tag") == tag

            if text:

                ok = ok and (text.lower() in (log.get("text","").lower()))

            return ok

        return [l for l in logs if match(l)]

    def show_status(self, scope="summary"):

        """Return a pretty status string; never prints."""

        if not DATA_FILE.exists():

            return ""

        try:

            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))

        except Exception:

            return ""

        logs = data.get("logs", [])

        if not logs:

            return "No status available."

        lines = []

        lines.append("──────── STATUS ────────")

        lines.append(f"Total logs: {len(logs)}")

        if scope in ("summary","daily","weekly","full"):

            lines.append("Last 3 logs:")

            for log in logs[-3:]:

                tag_part = f" [tag: {log.get('tag')}]" if log.get('tag') else ""

                lines.append(f"- {log.get('text','')} [{log.get('time','')}]"+tag_part)

        lines.append("────────────────────────")

        return "\n".join(lines)

def export_csv(out_path: str):
    """Write logs to CSV at out_path and return the path. No prints here."""
    # Local import is fine; csv is also imported at module top
    data = {}
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    logs = data.get("logs", [])

    fieldnames = ["time", "text", "tag"]
    # newline="" avoids extra blank lines on Windows
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        import csv
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for l in logs:
            writer.writerow({
                "time": l.get("time", ""),
                "text": l.get("text", ""),
                "tag": l.get("tag", ""),
            })
    return out_path

def _atomic_write_json(path: Path, obj: dict):
    tmp = NamedTemporaryFile("w", delete=False, encoding="utf-8", newline="")
    try:
        json.dump(obj, tmp, indent=2, ensure_ascii=False)
        tmp.flush(); os.fsync(tmp.fileno())
        tmp.close()
        if path.exists():
            bak = path.with_suffix(path.suffix + ".bak")
            try: os.replace(path, bak)
            except Exception: pass
        os.replace(tmp.name, path)
    finally:
        try: os.unlink(tmp.name)
        except Exception: pass

# ---- RICK_DATA env override (append) ----
# If RICK_DATA is set, always use it (takes precedence over any earlier DATA_FILE assignment).
try:
    import os as _os
    _env = _os.getenv("RICK_DATA")
    if _env:
        DATA_FILE = Path(_env)
except Exception:
    pass
# ---- end RICK_DATA env override (append) ----
