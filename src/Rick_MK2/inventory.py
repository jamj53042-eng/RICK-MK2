from __future__ import annotations
from .storage import Storage
import random

def list_items():
    """Return (items_list, gold_amount)"""
    data = Storage().load()
    items = data.get("inventory", [])
    gold = data.get("gold", 0)
    return items, gold

def add_item(name: str, qty: int = 1, rarity: str = "common"):
    """Add an item and return the added/updated item dict"""
    store = Storage()
    data = store.load()
    inventory = data.setdefault("inventory", [])

    # Merge with existing same name+rarity if present
    for it in inventory:
        if it.get("name") == name and it.get("rarity") == rarity:
            it["qty"] = it.get("qty", 0) + qty
            store.save(data)
            return it

    new_item = {"name": name, "qty": qty, "rarity": rarity}
    inventory.append(new_item)
    store.save(data)
    return new_item

def remove_item(name: str, qty: int = 1):
    """Remove qty of an item by name; return removed item dict or None"""
    store = Storage()
    data = store.load()
    inventory = data.get("inventory", [])

    for it in list(inventory):
        if it.get("name") == name:
            removed_qty = min(qty, it.get("qty", 0))
            removed = {"name": name, "qty": removed_qty, "rarity": it.get("rarity", "common")}
            if it.get("qty", 0) > qty:
                it["qty"] = it.get("qty", 0) - qty
            else:
                inventory.remove(it)
            store.save(data)
            return removed
    return None

def roll_challenge_loot(difficulty: str):
    """Return a loot dict for the given difficulty"""
    loot_tables = {
        "easy": [
            {"name": "Gold Coin", "qty": random.randint(5, 15), "rarity": "common"},
            {"name": "Healing Potion", "qty": 1, "rarity": "common"},
        ],
        "hard": [
            {"name": "Iron Sword", "qty": 1, "rarity": "uncommon"},
            {"name": "Gold Coin", "qty": random.randint(10, 25), "rarity": "common"},
            {"name": "Magic Scroll", "qty": 1, "rarity": "rare"},
        ],
    }
    table = loot_tables.get(difficulty, [
        {"name": "Gold Coin", "qty": random.randint(1, 5), "rarity": "common"}
    ])
    return random.choice(table)

def get_inventory_summary():
    items, gold = list_items()
    if not items and not gold:
        return "Inventory is empty."
    lines = [f"{it.get('name')} x{it.get('qty')} [{it.get('rarity')}]" for it in items]
    lines.append(f"Gold: {gold}")
    return "\n".join(lines)
