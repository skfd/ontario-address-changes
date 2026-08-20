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

# Asks Windows whether the internet connection is metered (cellular/tethering,
# or a wifi marked "Metered connection" in Settings). Runs the WinRT call in a
# Windows PowerShell 5.1 subprocess because the projection syntax doesn't load
# under pwsh 7; any detection failure fails open (unmetered) so a broken API
# never silently blocks updates.
function Test-Metered {
    $probe = '[Windows.Networking.Connectivity.NetworkInformation,Windows.Networking.Connectivity,ContentType=WindowsRuntime]::GetInternetConnectionProfile().GetConnectionCost().NetworkCostType'
    $cost = powershell -NoProfile -Command "try { $probe } catch {}"
    return $cost -in 'Fixed', 'Variable'
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
$skipReason = 'offline'
foreach ($attempt in 1..3) {
    if ($attempt -gt 1) {
        Log "RETRY attempt $attempt $(Get-Date -Format o)"
        Start-Sleep -Seconds 900
    }
    # No internet is handled like the laptop being off: skip the attempt
    # instead of letting every city fail and be recorded as a run failure.
    if (-not (Wait-Online -Minutes 10)) {
        Log "OFFLINE $(Get-Date -Format o) attempt $attempt skipped"
        $skipReason = 'offline'
        continue
    }
    # Metered connections (tethering/hotspot) are unreliable and cost data:
    # don't even try. Later attempts re-check, so a hotspot that ends within
    # ~30 min still gets that day's update.
    if (Test-Metered) {
        Log "METERED $(Get-Date -Format o) attempt $attempt skipped"
        $skipReason = 'metered'
        continue
    }
    Invoke-Logged "python run.py update --all --jobs 6"
    $updateExit = $LASTEXITCODE
    $ranUpdate  = $true
    if ($updateExit -eq 0) { break }
}

# A failed run on a machine that is (or went) offline/metered is not "FAILED":
# same as if the laptop had been off, the update just didn't happen.
$outcome = $updateExit
if ($updateExit -ne 0) {
    if (-not $ranUpdate)        { $outcome = $skipReason }
    elseif (-not (Test-Online)) { $outcome = 'offline' }
    elseif (Test-Metered)       { $outcome = 'metered' }
}

# The vault's status page, regenerated from the catalog the update just wrote.
# Runs on every outcome, including offline/metered: it reads only the catalog
# and the vault on disk, so a day when nothing was pulled is exactly when the
# "no attempt" gaps are worth looking at. It is a local artifact under the vault
# root -- nothing here commits or publishes it -- and a render failure leaves
# $outcome alone, since a stale status page is not a failed update.
Invoke-Logged "python -m addressvault.cli report"
if ($LASTEXITCODE -ne 0) { Log "REPORT-FAILED $(Get-Date -Format o) exit=$LASTEXITCODE" }

# A crashed git process can leave a stale .lock behind, and any of them stalls
# the publish: index.lock fails the add (nothing staged, commit silently
# skipped), while a ref lock fails the commit or the push's ref update
# (observed 2026-08-05: refs\remotes\origin\main.lock left the day's docs staged
# and the site a day stale). So sweep every lock under .git, not just index.lock.
# An hour-old lock during a noon run is never a live one.
$gitDir = Join-Path $projectDir '.git'
foreach ($lock in @(Get-ChildItem $gitDir -Filter '*.lock' -Recurse -Force -File -ErrorAction SilentlyContinue)) {
    if (((Get-Date) - $lock.LastWriteTime).TotalMinutes -gt 60) {
        Log "STALE-LOCK $(Get-Date -Format o) removing $($lock.FullName.Substring($projectDir.Length + 1))"
        Remove-Item -Force $lock.FullName
    }
}

# flags.toml rides along: report generation appends newly flagged events to it,
# and the append is only durable history once committed.
Invoke-Logged "git add docs flags.toml"
$publishExit = $LASTEXITCODE
if ($publishExit -eq 0) {
    git diff --cached --quiet
    if ($LASTEXITCODE -ne 0) {
        Invoke-Logged "git commit -m `"daily update $(Get-Date -Format yyyy-MM-dd)`""
        $publishExit = $LASTEXITCODE
        # Nothing new to push if the commit never landed, and pushing anyway
        # reports "Everything up-to-date" -- a success that hides the failure.
        if ($publishExit -eq 0) {
            Invoke-Logged "git push"
            $publishExit = $LASTEXITCODE
        }
    }
}

# A failed add/commit/push leaves docs\ staged and the site stale, but every
# step above is fire-and-forget, so the run used to exit 0 and look healthy
# (observed 2026-08-05). Report it -- but never over-write a real update
# failure or an offline/metered skip: those are the bigger news, and the first
# already exits nonzero.
if ($publishExit -ne 0 -and $outcome -eq 0) { $outcome = 'publish-failed' }

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

# Offline/metered exits 0: nothing is wrong with the pipeline, there was just
# no (usable) network.
if ($outcome -in 'offline', 'metered') { exit 0 }
# The cities updated but the site did not: $updateExit is 0 here, so this needs
# its own nonzero exit to reach Task Scheduler as a failure.
if ($outcome -eq 'publish-failed') { exit 1 }
exit $updateExit
