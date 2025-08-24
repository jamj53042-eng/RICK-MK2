
class PerkSystem:
    def __init__(self):
        self.available_perks = {
            "quick_learner": "Gain extra XP from challenges",
            "resilient": "Take less penalty from failures",
            "charismatic": "Unlocks fun dialogue options"
        }
        self.unlocked = []

    def list_perks(self):
        if not self.unlocked:
            return "No perks unlocked yet."
        return f"Unlocked perks: {', '.join(self.unlocked)}"

    def unlock(self, name):
        if name not in self.available_perks:
            return f"Perk '{name}' does not exist."
        if name in self.unlocked:
            return f"Perk '{name}' already unlocked."
        self.unlocked.append(name)
        return f"Perk '{name}' unlocked! 🎯"
