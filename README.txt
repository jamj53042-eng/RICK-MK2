Files included in this patch:
- src/Rick_MK2/storage.py
- src/Rick_MK2/journal.py
- src/Rick_MK2/quest.py
- src/Rick_MK2/xp.py
- src/Rick_MK2/inventory.py
- src/Rick_MK2/cli.py

PowerShell quick apply from your project root (venv active):
    Expand-Archive -Force patch_inventory_rewards.zip -DestinationPath .
    python -m pip install -e .
