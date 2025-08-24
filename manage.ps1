param (
    [string]$Action
)

switch ($Action) {
    "cheatsheet" {
        notepad ".\commands.md"
    }
    default {
        Write-Host "Usage: .\manage.ps1 [cheatsheet]" -ForegroundColor Yellow
    }
}
