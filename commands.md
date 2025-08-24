
# Rick MK2 - Command Cheat Sheet

Your personal CLI assistant commands.

---

## Journal Commands

### Log an entry
```
rick log "your text here" --tag optional_tag
```
Example:
```
rick log "gym session" --tag health
```

### Search entries
```
rick search --text keyword
rick search --tag tagname
```

### Status report
```
rick status summary   # Show total number of entries
rick status full      # Show all entries with details
```

### Clear journal (with confirmation)
```
rick clear
```
- Prompts you to confirm before deleting **all entries**.
- Type `y` to confirm, or `n` to cancel.

---

## Backup & Restore

### Create backup (keeps last 10 backups)
```
./backup.ps1
```

### Restore from backup
```
./restore.ps1
```
- Lists available backups.
- Lets you pick one to restore.
- Creates an automatic pre-restore backup before overwriting.

---

## Tips
- Always run inside the virtual environment:  
  ```
  .venv\Scripts\Activate
  ```
- Use `rick status summary` often to keep track of logs.
- Backups older than 10 will be automatically deleted.
