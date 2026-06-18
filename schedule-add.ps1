# Registers ONE scheduled task that runs daily-update.ps1 (parallel update of all
# datasets, then commit + push docs). New cities in datasets\*.toml are picked up
# automatically; no re-registration needed.

$projectDir = $PSScriptRoot
$taskName   = "kk-ontario-update"
$runAt      = Get-Date "12:00"
$logDir     = "$projectDir\logs"
$logFile    = "$logDir\update.log"

if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir | Out-Null
}

$action = New-ScheduledTaskAction `
    -Execute "cmd.exe" `
    -Argument "/c powershell -NoProfile -ExecutionPolicy Bypass -File `"$projectDir\daily-update.ps1`" > `"$logFile`" 2>&1"

$trigger = New-ScheduledTaskTrigger -Daily -At $runAt

# run.py exits non-zero if any city failed, so RestartCount retries the whole run;
# already-updated cities short-circuit (cached download + already-imported), making
# a restart effectively a per-city retry.
$settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2) `
    -StartWhenAvailable `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 30)

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Force | Out-Null

Write-Host ("Registered {0}: daily {1:HH:mm} via daily-update.ps1, log: {2}" -f $taskName, $runAt, $logFile)
Write-Host "Retry: up to 3 whole-run restarts, 30 min apart, when any city fails."
