# Registers the scheduled tasks (see each block below for the rest):
#   kk-ontario-update   daily 12:00  daily-update.ps1 (parallel update of all
#                       datasets, then commit + push docs). New cities in
#                       datasets\*.toml are picked up automatically.
#   kk-ontario-article  daily 15:00  monthly-article.ps1 (from the 3rd of each
#                       month, write the monthly newsletter pieces due across
#                       every publishable city: quiet months from a fixed shape,
#                       the rest with headless Claude up to a daily cap; render,
#                       commit + push after each city). Exits at once before the
#                       3rd; 15:00 keeps it clear of the noon run's git.

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
# 3 h is a backstop: daily-update.ps1 budgets its own retries to finish inside
# ~2 h (a killed run leaves no END line and no commit, 2026-09-08), and the
# 15:00 article task waits up to 90 min for a live update anyway.
$settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Hours 3) `
    -StartWhenAvailable `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 30)

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Force | Out-Null

Write-Host ("Registered {0}: daily {1:HH:mm} via daily-update.ps1, log: {2}" -f $taskName, $runAt, $logFile)
Write-Host "Retry: daily-update.ps1 itself reruns up to 3 attempts, 15 min apart, on failure."

# The article writer. Long limit: each researched article is a headless Claude
# run with web research, 40-60 min, and a day's run writes several before its
# own budget stops it. No RestartCount: a failed or deferred city is retried by
# the next day's run, which resumes from whatever is missing.
$articleTask  = "kk-ontario-article"
$articleAt    = Get-Date "15:00"
$articleLog   = "$projectDir\logs\article.log"

$articleAction = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$projectDir\monthly-article.ps1`""

$articleTrigger = New-ScheduledTaskTrigger -Daily -At $articleAt

$articleSettings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Hours 4) `
    -StartWhenAvailable

Register-ScheduledTask -TaskName $articleTask -Action $articleAction -Trigger $articleTrigger -Settings $articleSettings -Force | Out-Null

Write-Host ("Registered {0}: daily {1:HH:mm} via monthly-article.ps1 (acts from the 3rd), log: {2}" -f $articleTask, $articleAt, $articleLog)

# The flag review. Hourly through the evening, when the operator is actually
# answering issues: 18:00, 19:00, 20:00, 21:00, 22:00. Nothing before the noon
# run has had its retries, nothing in the 23:00-06:00 quiet hours. Short limit:
# a pass is a few gh calls plus, at most, one headless Claude triage.
$flagsTask = "kk-ontario-flags"
$flagsAt   = Get-Date "18:00"
$flagsLog  = "$projectDir\logs\flags-review.log"

$flagsAction = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$projectDir\review-flags.ps1`""

$flagsTrigger = New-ScheduledTaskTrigger -Daily -At $flagsAt
$flagsTrigger.Repetition = (New-ScheduledTaskTrigger -Once -At $flagsAt `
    -RepetitionInterval (New-TimeSpan -Hours 1) `
    -RepetitionDuration (New-TimeSpan -Hours 4 -Minutes 30)).Repetition

$flagsSettings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 50) `
    -StartWhenAvailable

Register-ScheduledTask -TaskName $flagsTask -Action $flagsAction -Trigger $flagsTrigger -Settings $flagsSettings -Force | Out-Null

Write-Host ("Registered {0}: hourly 18:00-22:00 via review-flags.ps1, log: {1}" -f $flagsTask, $flagsLog)

# The off-machine backup: vault restic repo + catalog + stores to two restic
# repos, Google Drive and Backblaze B2. 14:20 sits after the noon run's retry
# budget (~2 h), and backup-offsite.ps1 waits for it anyway if it is still going.
# Skipped until at least one destination is configured (see the header of
# backup-offsite.ps1), so a fresh machine does not fail every day.
$backupTask   = "kk-ontario-backup"
$backupAt     = Get-Date "14:20"
$backupLog    = "$projectDir\logs\backup.log"
$backupScript = "$projectDir\backup-offsite.ps1"
$backupDests  = @(& powershell -NoProfile -ExecutionPolicy Bypass -File $backupScript -ListDestinations)

if ($backupDests) {
    $backupAction = New-ScheduledTaskAction `
        -Execute "powershell.exe" `
        -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$backupScript`""

    $backupTrigger = New-ScheduledTaskTrigger -Daily -At $backupAt

    # Long limit: a day's delta is small, but a laptop off for a week, or a
    # Sunday check of both repos, can take a while over home upload speeds.
    $backupSettings = New-ScheduledTaskSettingsSet `
        -ExecutionTimeLimit (New-TimeSpan -Hours 6) `
        -StartWhenAvailable

    Register-ScheduledTask -TaskName $backupTask -Action $backupAction -Trigger $backupTrigger -Settings $backupSettings -Force | Out-Null

    $names = ($backupDests | ForEach-Object { ($_ -split "`t")[0] }) -join ', '
    Write-Host ("Registered {0}: daily {1:HH:mm} via backup-offsite.ps1 to {2}, log: {3}" -f $backupTask, $backupAt, $names, $backupLog)
} else {
    Write-Host "Skipped $backupTask`: no backup destination configured yet (see backup-offsite.ps1 header)."
}
