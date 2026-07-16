# Daily refresh: update all datasets in parallel, then commit and push the
# regenerated site. Called by the kk-ontario-update scheduled task.
# Commits docs/ even when some cities failed (their reports are simply stale).

$projectDir = $PSScriptRoot
Set-Location $projectDir

# Python block-buffers stdout on a pipe (~8KB), which would leave the console
# and log silent for minutes; unbuffered output streams line by line. Set as
# an env var so the per-city run.py subprocesses inherit it too.
$env:PYTHONUNBUFFERED = '1'

# The script writes its own log (instead of relying on the scheduled task's
# output redirection) so manual reruns show up in progress.ps1 too.
$logDir  = "$projectDir\logs"
$logFile = "$logDir\update.log"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }

# Tees a line to the log and the console.
function Log([string]$msg) {
    Add-Content $logFile $msg
    Write-Host $msg
}

# Runs a native command with stdout+stderr merged at the cmd level (keeps
# stderr plain text, no ErrorRecord wrapping) and tees each line to the log
# and the console. $LASTEXITCODE afterwards is the command's exit code.
function Invoke-Logged([string]$commandLine) {
    cmd /c "$commandLine 2>&1" | ForEach-Object { Add-Content $logFile $_; Write-Host $_ }
}

# Probes anchor IPs over TCP 443 -- no DNS involved -- so "offline" means this
# machine has no internet at all. A city server that won't resolve or connect
# while the anchors answer still counts as a real failure, not offline.
function Test-Online {
    foreach ($ip in '1.1.1.1', '8.8.8.8', '9.9.9.9') {
        $tcp = [System.Net.Sockets.TcpClient]::new()
        try {
            if ($tcp.ConnectAsync($ip, 443).Wait(4000) -and $tcp.Connected) { return $true }
        } catch {} finally { $tcp.Dispose() }
    }
    return $false
}

# Waits up to $Minutes for connectivity (wifi lags behind wake-from-sleep).
function Wait-Online {
    param([int]$Minutes)
    $deadline = (Get-Date).AddMinutes($Minutes)
    while (-not (Test-Online)) {
        if ((Get-Date) -ge $deadline) { return $false }
        Start-Sleep -Seconds 30
    }
    return $true
}

# First log line is the run anchor progress.ps1 uses for elapsed/ETA.
# Set-Content truncates the previous run's log: one run per file.
$startLine = "START $(Get-Date -Format o) jobs=6"
Set-Content $logFile $startLine
Write-Host $startLine
$runStart = Get-Date

# Retry here, not in Task Scheduler: RestartCount never fires on a nonzero
# exit code (it only covers launch failures). Reruns are cheap because
# already-updated cities short-circuit (cached download + already-imported).
$updateExit = 1
$ranUpdate  = $false
foreach ($attempt in 1..3) {
    if ($attempt -gt 1) {
        Log "RETRY attempt $attempt $(Get-Date -Format o)"
        Start-Sleep -Seconds 900
    }
    # No internet is handled like the laptop being off: skip the attempt
    # instead of letting every city fail and be recorded as a run failure.
    if (-not (Wait-Online -Minutes 10)) {
        Log "OFFLINE $(Get-Date -Format o) attempt $attempt skipped"
        continue
    }
    Invoke-Logged "python run.py update --all --jobs 6"
    $updateExit = $LASTEXITCODE
    $ranUpdate  = $true
    if ($updateExit -eq 0) { break }
}

# A failed run on a machine that is (or went) offline is "offline", not
# "FAILED": same as if the laptop had been off, the update just didn't happen.
$outcome = $updateExit
if ($updateExit -ne 0 -and (-not $ranUpdate -or -not (Test-Online))) { $outcome = 'offline' }

git add docs
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    Invoke-Logged "git commit -m `"daily update $(Get-Date -Format yyyy-MM-dd)`""
    Invoke-Logged "git push"
}

# Final log line marks the run as over for progress.ps1.
Log "END $(Get-Date -Format o) exit=$outcome attempts=$attempt"

# One summary row per run; survives update.log being overwritten next run.
$runsCsv = "$projectDir\logs\runs.csv"
$row = [pscustomobject]@{
    started  = $runStart.ToString('o')
    finished = (Get-Date).ToString('o')
    attempts = $attempt
    exit     = $outcome
}
if (Test-Path $runsCsv) { $row | Export-Csv $runsCsv -NoTypeInformation -Append }
else                    { $row | Export-Csv $runsCsv -NoTypeInformation }

# Offline exits 0: nothing is wrong with the pipeline, there was just no network.
if ($outcome -eq 'offline') { exit 0 }
exit $updateExit
