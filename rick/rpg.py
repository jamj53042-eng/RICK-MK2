import random

class RPGSystem:
    def __init__(self):
        self.level = 1
        self.xp = 0
        self.xp_to_next = 10
        self.badges = []
        self.perks = []
        self.results = []
        self.streak = 0

    def status(self):
        perks = ', '.join(self.perks) if self.perks else 'None'
        badges = ', '.join(self.badges) if self.badges else 'None'
        return f"Level: {self.level}\nXP: {self.xp}/{self.xp_to_next}\nBadges: {badges}\nPerks: {perks}\nStreak: {self.streak} 🔥"

    def attempt_challenge(self, difficulty):
        base_xp = {"easy": 2, "medium": 12, "hard": 28}.get(difficulty, 0)
        if base_xp == 0:
            return f"Unknown challenge: {difficulty}"

        # streak bonus
        self.streak += 1
        bonus_percent = min(self.streak * 0.1, 0.5)
        total_xp = int(base_xp * (1 + bonus_percent))

        self.xp += total_xp
        msg = f"Rick takes on a {difficulty} challenge... 🗡️\nGained {total_xp} XP! 🎉"
        if bonus_percent > 0:
            msg += f" (+{int(bonus_percent*100)}% streak bonus)"

        self.results.insert(0, f"{difficulty.title()} → +{total_xp} XP ({int(bonus_percent*100)}% bonus)")
        if len(self.results) > 5:
            self.results.pop()

        # level up
        if self.xp >= self.xp_to_next:
            self.level += 1
            self.xp -= self.xp_to_next
            self.xp_to_next = int(self.xp_to_next * 1.5)
            msg += f"\nLevel up! Rick is now Level {self.level} 💪"
            self.streak = 0  # reset streak on level up

        return msg

    def get_results(self):
        if not self.results:
            return "No results yet."
        return "Recent results:\n" + "\n".join(f"{i+1}. {r}" for i, r in enumerate(self.results))
