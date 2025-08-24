import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("data.json")

class Logger:
    def __init__(self):
        self.data = {"logs": []}
        if DATA_FILE.exists():
            try:
                self.data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                self.data = {"logs": []}

    def save(self):
        DATA_FILE.write_text(json.dumps(self.data, indent=2), encoding="utf-8")

    def add_log(self, entry, tag=None):
        log = {
            "text": entry,
            "time": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
            "tag": tag or ""
        }
        self.data["logs"].append(log)
        self.save()
        print(f"✅ Logged: {entry}" + (f" [tag: {tag}]" if tag else ""))

    def undo(self, count=1):
        if len(self.data["logs"]) == 0:
            print("⚠️ No logs to undo.")
            return
        removed = self.data["logs"][-count:]
        self.data["logs"] = self.data["logs"][:-count]
        self.save()
        for r in removed:
            print(f"🗑️ Removed: {r['text']} [tag: {r['tag']}]")

    def reset(self, scope):
        if scope == "log" or scope == "all":
            self.data["logs"] = []
        self.save()
        print(f"✅ Reset {scope}")

    def show_status(self, scope="summary"):
        logs = self.data["logs"]
        print("═══════════════════════════")
        print("📊 STATUS")
        print(f"Total logs: {len(logs)}")
        if logs:
            print("Last 3 logs:")
            for log in logs[-3:]:
                print(f"- {log['text']} [{log['time']}] [tag: {log['tag']}]")
        print("═══════════════════════════")

    def search_logs(self, tag=None, text=None):
        logs = self.data["logs"]
        results = []
        for log in logs:
            if tag and log["tag"] != tag:
                continue
            if text and text.lower() not in log["text"].lower():
                continue
            results.append(log)

        if not results:
            print("⚠️ No matching logs found.")
            return

        print(f"🔎 Found {len(results)} logs:")
        for log in results:
            print(f"- {log['text']} [{log['time']}] [tag: {log['tag']}]")
