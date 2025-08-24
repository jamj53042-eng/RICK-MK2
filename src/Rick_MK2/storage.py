from __future__ import annotations
import json, shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PACKAGE_DIR = Path(__file__).resolve().parent
STARTER_CONFIG = PACKAGE_DIR / "config.json"
HOME_DIR = Path.home() / ".rick_mk2"
HOME_CONFIG = HOME_DIR / "config.json"

@dataclass
class Storage:
    def ensure_home_config(self) -> None:
        HOME_DIR.mkdir(parents=True, exist_ok=True)
        if not HOME_CONFIG.exists():
            if STARTER_CONFIG.exists():
                shutil.copy2(STARTER_CONFIG, HOME_CONFIG)
            else:
                HOME_CONFIG.write_text(json.dumps(self.default_config(), indent=2))

    def load(self) -> dict[str, Any]:
        self.ensure_home_config()
        with HOME_CONFIG.open("r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data: dict[str, Any]) -> None:
        self.ensure_home_config()
        with HOME_CONFIG.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def default_config() -> dict[str, Any]:
        return {
            "version": 1,
            "streak": 0,
            "best_streak": 0,
            "last_update": None,
            "bonus_per_streak": 5,
            "bonus_cap": 100,
            "xp": 0,
            "level": 1,
            "logs": [],
            "quests": [],
            "inventory": [],
            "gold": 0
        }
