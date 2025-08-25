# Rick_MK2 CLI

## Global
- `--json` / `--quiet` / `--no-emoji` are per *subcommand* (e.g., `python -m Rick_MK2.rick search --json`).

## search
```powershell
python -m Rick_MK2.rick search --tag quick
python -m Rick_MK2.rick search --tag quick --json
python -m Rick_MK2.rick search --text "error" --limit 5
python -m Rick_MK2.rick search --from 2025-08-01 --to 2025-08-31 --compact
python -m Rick_MK2.rick search --from 1900-01-01 --to 1900-01-02 --json --fail-empty
python -m Rick_MK2.rick search --tag quick --quiet
python -m Rick_MK2.rick status
python -m Rick_MK2.rick status --json
python -m Rick_MK2.rick status --quiet
$env:RICK_DATA = "$env:TEMP\rick_temp_data.json"
python -m Rick_MK2.rick status --json
Remove-Item Env:\RICK_DATA
