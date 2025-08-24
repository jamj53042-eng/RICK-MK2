from __future__ import annotations
import random
from .xp import gain_xp
from .inventory import roll_challenge_loot, add_item

def challenge(difficulty: str) -> str:
    """Simulate a challenge attempt, award XP and loot if successful"""
    # Difficulty multipliers
    xp_rewards = {
        "easy": 2,
        "medium": 5,
        "hard": 10,
    }

    # Random success chance by difficulty
    success_chance = {
        "easy": 0.9,
        "medium": 0.7,
        "hard": 0.5,
    }

    if difficulty not in xp_rewards:
        return f"Unknown difficulty: {difficulty}"

    success = random.random() < success_chance[difficulty]
    if success:
        xp = xp_rewards[difficulty]
        gain_xp(xp)
        loot = roll_challenge_loot()
        added = add_item(loot["name"], loot["qty"], loot["rarity"])
        return (
            f"Rick takes on a {difficulty} challenge... ???\n"
            f"Gained {xp} XP! ??\n"
            f"Rick found: {added['name']} x{loot['qty']} [{loot['rarity']}] ??"
        )
    else:
        return f"Rick takes on a {difficulty} challenge... but failed. ?"
