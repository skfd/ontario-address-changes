# Registers one scheduled task per dataset in datasets\*.toml.
# Task names are prefixed with the terminal user (kk-<slug>).
# Re-run after adding a new city; -Force replaces existing tasks.

$projectDir = $PSScriptRoot
$prefix     = "kk"
$baseTime   = Get-Date "12:00"
$staggerMin = 5      # minutes between successive cities
$logDir     = "$projectDir\logs"

if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir | Out-Null
}

$tomls = Get-ChildItem -Path "$projectDir\datasets\*.toml" | Sort-Object Name
if (-not $tomls) {
    Write-Host "No datasets found in $projectDir\datasets."
    return
}

$i = 0
foreach ($toml in $tomls) {
    $slug     = $toml.BaseName
    $taskName = "$prefix-$slug"
    $logFile  = "$logDir\$slug.log"
    $runAt    = $baseTime.AddMinutes($i * $staggerMin)

    $action = New-ScheduledTaskAction `
        -Execute "cmd.exe" `
        -Argument "/c cd /d `"$projectDir`" && python run.py update --city $slug >> `"$logFile`" 2>&1"

    $trigger = New-ScheduledTaskTrigger -Daily -At $runAt

    # RestartCount/Interval retry only fires because run.py now exits non-zero on a failed city.
    $settings = New-ScheduledTaskSettingsSet `
        -ExecutionTimeLimit (New-TimeSpan -Hours 2) `
        -StartWhenAvailable `
        -RestartCount 3 `
        -RestartInterval (New-TimeSpan -Minutes 30)

    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Force | Out-Null

    Write-Host ("Registered {0,-24} daily {1:HH:mm}  log: {2}" -f $taskName, $runAt, $logFile)
    $i++
}

Write-Host ""
Write-Host "$($tomls.Count) task(s) registered, staggered $staggerMin min apart starting $($baseTime.ToString('HH:mm'))."
Write-Host "Retry: up to 3 restarts, 30 min apart, on per-city failure."
