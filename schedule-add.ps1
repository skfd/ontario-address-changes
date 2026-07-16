# Registers ONE scheduled task that runs daily-update.ps1 (parallel update of all
# datasets, then commit + push docs). New cities in datasets\*.toml are picked up
# automatically; no re-registration needed.

$projectDir = $PSScriptRoot
$taskName   = "kk-ontario-update"
$runAt      = Get-Date "12:00"
$logFile    = "$projectDir\logs\update.log"

# No output redirection here: daily-update.ps1 writes its own log, so manual
# reruns are tracked by progress.ps1 the same way as scheduled ones.
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$projectDir\daily-update.ps1`""

$trigger = New-ScheduledTaskTrigger -Daily -At $runAt

# RestartCount does NOT fire on a nonzero exit code (only on launch failures) --
# observed 2026-07-16, when an all-cities failure never retried. daily-update.ps1
# retries failed runs itself; RestartCount stays only to cover launch failures.
$settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2) `
    -StartWhenAvailable `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 30)

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Force | Out-Null

Write-Host ("Registered {0}: daily {1:HH:mm} via daily-update.ps1, log: {2}" -f $taskName, $runAt, $logFile)
Write-Host "Retry: daily-update.ps1 itself reruns up to 3 attempts, 15 min apart, on failure."
