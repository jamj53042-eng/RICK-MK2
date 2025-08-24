
# === Restore Script ===
$Timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$PreBackupDest = ".\Rick_MK2_PRE_RESTORE_$Timestamp.zip"
$Items = Get-Content .\backup_items.txt
$LogFile = ".\restore.log"

try {
    $ValidItems = @()
    foreach ($Item in $Items) {
        if ([string]::IsNullOrWhiteSpace($Item)) { continue }
        if (Test-Path $Item) {
            $ValidItems += $Item
        }
    }

    if ($ValidItems.Count -gt 0) {
        Compress-Archive -Path $ValidItems -DestinationPath $PreBackupDest -Force
        Write-Host "💾 Auto-backup created before restore: $(Split-Path $PreBackupDest -Leaf)"
        Add-Content $LogFile "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [INFO] Auto-backup created: $PreBackupDest"
    }
}
catch {
    Write-Host "❌ Pre-restore backup failed: $($_.Exception.Message)" -ForegroundColor Red
    Add-Content $LogFile "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [ERROR] Pre-restore backup failed: $($_.Exception.Message)"
}

# === Cleanup old PRE_RESTORE backups (keep only last 5) ===
$MaxPreBackups = 5
$PreBackups = Get-ChildItem -Filter "Rick_MK2_PRE_RESTORE_*.zip" | Sort-Object LastWriteTime -Descending

if ($PreBackups.Count -gt $MaxPreBackups) {
    $ToDelete = $PreBackups | Select-Object -Skip $MaxPreBackups
    foreach ($File in $ToDelete) {
        Remove-Item $File.FullName -Force
        Write-Host "🗑️ Deleted old PRE_RESTORE backup: $($File.Name)"
        Add-Content $LogFile "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [INFO] Deleted old PRE_RESTORE backup: $($File.Name)"
    }
}

# === Restore process ===
$Backups = Get-ChildItem -Filter "Rick_MK2_backup_*.zip" | Sort-Object LastWriteTime -Descending
if ($Backups.Count -eq 0) {
    Write-Host "❌ No backups found to restore." -ForegroundColor Red
    exit 1
}

Write-Host "`nAvailable backups:`n"
for ($i = 0; $i -lt $Backups.Count; $i++) {
    Write-Host "$($i+1)) $($Backups[$i].Name)"
}

$Choice = Read-Host "`nEnter the number of the backup to restore"
if (-not ($Choice -as [int]) -or $Choice -lt 1 -or $Choice -gt $Backups.Count) {
    Write-Host "❌ Invalid choice." -ForegroundColor Red
    exit 1
}

$SelectedBackup = $Backups[$Choice - 1].FullName
Write-Host "You selected: $(Split-Path $SelectedBackup -Leaf)"
$Confirm = Read-Host "⚠️ This will overwrite files in the project folder. Continue? (y/n)"

if ($Confirm -eq 'y') {
    Expand-Archive -Path $SelectedBackup -DestinationPath . -Force
    Write-Host "✅ Restore complete from $(Split-Path $SelectedBackup -Leaf)"
    Add-Content $LogFile "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [INFO] Restored from $SelectedBackup"
} else {
    Write-Host "❌ Restore cancelled."
}
