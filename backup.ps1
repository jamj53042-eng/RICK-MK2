# === Backup Script ===
$Timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$Dest = ".\Rick_MK2_backup_$Timestamp.zip"
$Items = Get-Content .\backup_items.txt
$LogFile = ".\backup.log"

try {
    $ValidItems = @()
    foreach ($Item in $Items) {
        if ([string]::IsNullOrWhiteSpace($Item)) { continue }
        if (Test-Path $Item) {
            $ValidItems += $Item
        } else {
            Write-Host "⚠️ Skipped missing item: $Item"
            Add-Content $LogFile "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [WARN] Skipped missing item: $Item"
        }
    }

    Compress-Archive -Path $ValidItems -DestinationPath $Dest -Force
    Write-Host "✅ Backup complete: $(Split-Path $Dest -Leaf)"
    Add-Content $LogFile "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [INFO] Backup complete: $Dest"
}
catch {
    Write-Host "❌ Backup failed: $($_.Exception.Message)" -ForegroundColor Red
    Add-Content $LogFile "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [ERROR] Backup failed: $($_.Exception.Message)"
    exit 1
}

# === Cleanup old backups (keep only last 5) ===
$MaxBackups = 5
$Backups = Get-ChildItem -Filter "Rick_MK2_backup_*.zip" | Sort-Object LastWriteTime -Descending

if ($Backups.Count -gt $MaxBackups) {
    $ToDelete = $Backups | Select-Object -Skip $MaxBackups
    foreach ($File in $ToDelete) {
        Remove-Item $File.FullName -Force
        Write-Host "🗑️ Deleted old backup: $($File.Name)"
        Add-Content $LogFile "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [INFO] Deleted old backup: $($File.Name)"
    }
}
