from datetime import date

class StreakTracker:
    def __init__(self):
        self.streak = 3
        self.bonus = 15

    def get_status(self):
        return self.streak, self.bonus

class LogManager:
    def __init__(self, tracker):
        self.tracker = tracker
        self.logs = {}

    def add_entry(self, task):
        today = date.today().isoformat()
        self.logs.setdefault(today, []).append(task)
        return f"✔️ {task} (+{self.tracker.bonus}%)"

    def get_today_entries(self):
        today = date.today().isoformat()
        return self.logs.get(today, [])
