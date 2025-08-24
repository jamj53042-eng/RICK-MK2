# Rick MK2 🚀 (Python 3.10+)

Modular streak + bonus + results log system with styled outputs, daily summaries, and on-demand weekly scoreboard.
Includes a minimal CLI **and** an importable class for easy integration and future remote upgrades.

## Features
- Status block: Streak, Bonus %, Best streak, Last 3 logs, Timestamp
- Logs with **date + time**, grouped by day with daily summaries
- Weekly scoreboard (on demand)
- Reset commands (all require confirmation)
- Undo last N log entries (log-only; does not rewind streak/bonus)
- Dual config: ships with starter config; persists to `~/.rick_mk2/config.json` on first run

## Install
1) Unzip this archive.
2) (Optional, recommended for imports) Install in editable mode:
```
pip install -e ./Rick_MK2
```

## Quick Test (CLI)
```
python -m Rick_MK2 status
python -m Rick_MK2 log "✔️ Completed Task A (+15%)"
python -m Rick_MK2 log "✔️ Completed Task B (+20%)"
python -m Rick_MK2 status daily
python -m Rick_MK2 status weekly
python -m Rick_MK2 undo 2
python -m Rick_MK2 reset all
```

## Quick Test (Import)
```python
from Rick_MK2.rick import RickMK2
rick = RickMK2()
print(rick.status())
rick.log("✔️ Completed Task X (+20%)")
print(rick.status("daily"))
```

## Config
- Ships with `Rick_MK2/config.json` (starter).
- On first run, copies/uses `~/.rick_mk2/config.json`.
- Safe across upgrades; copy `~/.rick_mk2/` between machines for portability.

## Commands (CLI)
- `status` | `status daily` | `status weekly` | `status full`
- `log "TEXT"`  (manual entry string)
- `undo [N]`   (default 1)
- `reset streak|log|all` (asks for confirmation)
- `help`

## Timezone
All timestamps use your local system timezone; recommended: America/Vancouver.
