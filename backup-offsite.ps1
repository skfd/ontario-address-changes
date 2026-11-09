# Off-machine backup to two independent places: Google Drive (via rclone) and
# Backblaze B2 (S3 API). Each one is a separate restic repo that gets the
# vault's restic archive copied in, plus the state the archive does not hold
# (catalog.db, hot geojson files, data\*.db stores). Called by the
# kk-ontario-backup scheduled task after the noon run; safe to run by hand.
#
# Each destination is copied straight from the laptop, never one cloud from the
# other, so damage in one copy cannot spread to the other. Why repos and not a
# synced folder: restic packs never change once written, so `restic copy` only
# uploads what is new, and each repo can be checked and restored on its own.
#
# One-time setup (needs a browser on this machine):
#   0. Put the password in .address-cache\restic.pass into the password manager.
#      Both repos use the same password, and that file is deliberately NOT
#      backed up -- without the password neither copy can be opened.
#   Drive:
#   1. rclone config  ->  new remote named "gdrive", type "drive", scope "drive"
#      (ideally with your own Google OAuth client id; the shared one is slow).
#   Backblaze B2:
#   2. Create a private bucket (Canadian region if offered) and an application
#      key limited to that bucket, read and write. On the bucket page, note the
#      S3 endpoint (s3.<region>.backblazeb2.com).
#   3. Store them as user environment variables (restart the terminal after):
#        [Environment]::SetEnvironmentVariable('KK_B2_REPO',   's3:https://s3.<region>.backblazeb2.com/<bucket>/address-vault', 'User')
#        [Environment]::SetEnvironmentVariable('KK_B2_KEY_ID', '<keyID>',          'User')
#        [Environment]::SetEnvironmentVariable('KK_B2_KEY',    '<applicationKey>', 'User')
#      The script hands the key to restic as AWS_* only inside its own process,
#      so other AWS tools on the machine are not affected.
#   Both:
#   4. .\backup-offsite.ps1 -ListDestinations   (shows which are configured)
#   5. .\backup-offsite.ps1 -Init               (creates each repo with the local
#      repo's chunker params, so dedup carries over)
#   6. First run by hand on home wifi (~15 GB up per destination, can take
#      hours), detached:
#        Start-Process powershell -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','backup-offsite.ps1'
#   7. schedule-add.ps1 registers the daily task once any destination exists.
#
# Restore drill, per destination (-r <repo>, --password-file <pass>):
#   restic snapshots
#   restic dump latest --tag slug=<slug>,date=<date> /<slug>-<date>.geojson   (a vault pull)
#   restic restore latest --tag kind=state --target <dir>                     (catalog + stores)
#   For B2, set AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY from KK_B2_KEY_ID / KK_B2_KEY first.

param(
    [string]$VaultDir = $(if ($env:ADDRESSVAULT_DIR) { $env:ADDRESSVAULT_DIR } else { 'C:\Users\kk\Code\.address-cache' }),
    [string]$DataDir  = "$PSScriptRoot\data",
    # Override the destinations: "name=repo;name=repo" (tests, one-off runs).
    # One string, because powershell -File cannot pass an array.
    [string]$Repos,
    [int]$WaitMinutes = 150,
    [switch]$ListDestinations,
    [switch]$Init
)

$projectDir = $PSScriptRoot
$logDir     = "$projectDir\logs"
$logFile    = "$logDir\backup.log"
$csvFile    = "$logDir\backup.csv"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }

$localRepo = "$VaultDir\restic"
$passFile  = "$VaultDir\restic.pass"
$env:RESTIC_PASSWORD_FILE = $passFile
# Keep restic's own env override (used by the vault) from redirecting -r.
$env:RESTIC_REPOSITORY = $null

# The configured destinations, in order. A destination whose credentials or
# remote are missing is simply not listed, so a half-done setup backs up to
# whatever is ready instead of failing every day.
function Get-Destinations {
    if ($Repos) {
        return @($Repos -split ';' | Where-Object { $_ } | ForEach-Object {
            $name, $repo = $_ -split '=', 2
            [pscustomobject]@{ Name = $name; Repo = $repo }
        })
    }
    $list = @()
    $conf = (& rclone config file 2>$null | Select-Object -Last 1)
    if ($conf -and (Test-Path $conf) -and (Select-String -Path $conf -Pattern '^\[gdrive\]' -Quiet)) {
        $list += [pscustomobject]@{ Name = 'drive'; Repo = 'rclone:gdrive:backups/address-vault' }
    }
    if ($env:KK_B2_REPO -and $env:KK_B2_KEY_ID -and $env:KK_B2_KEY) {
        $env:AWS_ACCESS_KEY_ID     = $env:KK_B2_KEY_ID
        $env:AWS_SECRET_ACCESS_KEY = $env:KK_B2_KEY
        $list += [pscustomobject]@{ Name = 'b2'; Repo = $env:KK_B2_REPO }
    }
    return $list
}

function Log([string]$msg) {
    Add-Content $logFile $msg
    Write-Host $msg
}

# Same shape as daily-update.ps1: stdout+stderr merged at the cmd level, teed
# to log and console; $LASTEXITCODE is the command's exit code.
function Invoke-Logged([string]$commandLine) {
    Log "> $commandLine"
    cmd /c "$commandLine 2>&1" | ForEach-Object { Add-Content $logFile $_; Write-Host $_ }
}

# restic exits 10 when the repo does not exist (0.17+), 0 when it opens.
function Get-RepoState([string]$repo) {
    cmd /c "restic -r $repo cat config >nul 2>&1"
    switch ($LASTEXITCODE) { 0 { 'ready' } 10 { 'missing' } default { 'unreachable' } }
}

# Copied from daily-update.ps1 (keep in step): TCP-by-IP anchors, no DNS.
function Test-Online {
    foreach ($ip in '1.1.1.1', '8.8.8.8', '9.9.9.9') {
        $tcp = [System.Net.Sockets.TcpClient]::new()
        try {
            if ($tcp.ConnectAsync($ip, 443).Wait(4000) -and $tcp.Connected) { return $true }
        } catch {} finally { $tcp.Dispose() }
    }
    return $false
}

# Copied from daily-update.ps1 (keep in step): WinRT via a 5.1 subprocess,
# fails open.
function Test-Metered {
    $probe = '[Windows.Networking.Connectivity.NetworkInformation,Windows.Networking.Connectivity,ContentType=WindowsRuntime]::GetInternetConnectionProfile().GetConnectionCost().NetworkCostType'
    $cost = powershell -NoProfile -Command "try { $probe } catch {}"
    return $cost -in 'Fixed', 'Variable'
}

# One CSV row per destination per run; dest '*' for a run that stopped before
# reaching any destination.
function Write-Row([string]$dest, [datetime]$from, [string]$outcome, $copyExit, $stateExit, $maintExit) {
    $mins = [math]::Round(((Get-Date) - $from).TotalMinutes, 1)
    if (-not (Test-Path $csvFile)) { Add-Content $csvFile 'start,dest,minutes,outcome,copy_exit,state_exit,maint_exit' }
    Add-Content $csvFile ("{0},{1},{2},{3},{4},{5},{6}" -f $from.ToString('s'), $dest, $mins, $outcome, $copyExit, $stateExit, $maintExit)
    Log "  [$dest] outcome=$outcome minutes=$mins"
}

function Finish([string]$outcome, [int]$code) {
    $mins = [math]::Round(((Get-Date) - $start).TotalMinutes, 1)
    Log "END $(Get-Date -Format o) outcome=$outcome minutes=$mins"
    exit $code
}

# Copy the vault archive and back up the rest into one destination. Returns its
# outcome: ok / partial / FAILED / repo-unreachable / not-initialized.
function Backup-To($dest) {
    $from = Get-Date
    $r = $dest.Repo
    Log "-- $($dest.Name) $(Get-Date -Format o) repo=$r"

    $state = Get-RepoState $r
    if ($state -eq 'missing')     { Write-Row $dest.Name $from 'not-initialized' '' '' ''; return 'not-initialized' }
    if ($state -eq 'unreachable') { Write-Row $dest.Name $from 'repo-unreachable' '' '' ''; return 'repo-unreachable' }

    # Clears only locks left by a killed run (restic leaves live ones alone).
    Invoke-Logged "restic -r $r unlock"

    # 1. Every vault snapshot not yet there. Same password both sides.
    Invoke-Logged "restic -r $r copy --from-repo `"$localRepo`" --from-password-file `"$passFile`""
    $copyExit = $LASTEXITCODE

    # 2. What the archive does not hold: catalog, hot pulls, city stores. The
    # password file stays out on purpose (see header), and _download is scratch.
    Invoke-Logged ("restic -r $r backup --tag kind=state --host ontario-backup " +
        "`"$VaultDir`" `"$DataDir`" " +
        "--exclude `"$localRepo`" --exclude `"$passFile`" --exclude `"$VaultDir\_download`"")
    $stateExit = $LASTEXITCODE   # 3 = some files unreadable, snapshot still made

    # 3. Maintenance. Only kind=state snapshots are ever forgotten: the vault's
    # own snapshots are kept forever, as they are locally.
    $maintExit = 0
    if ($from.Day -eq 1) {
        Invoke-Logged "restic -r $r forget --tag kind=state --keep-daily 14 --keep-weekly 8 --keep-monthly 36 --prune"
        $maintExit = $LASTEXITCODE
    }
    if ($from.DayOfWeek -eq 'Sunday') {
        Invoke-Logged "restic -r $r check --read-data-subset=5%"
        if ($LASTEXITCODE -ne 0) { $maintExit = $LASTEXITCODE }
    }

    $outcome = 'ok'
    if (($copyExit -ne 0) -or ($stateExit -notin @(0, 3)) -or ($maintExit -ne 0)) { $outcome = 'FAILED' }
    elseif ($stateExit -eq 3) { $outcome = 'partial' }
    Write-Row $dest.Name $from $outcome $copyExit $stateExit $maintExit
    return $outcome
}

$destinations = @(Get-Destinations)

if ($ListDestinations) {
    $destinations | ForEach-Object { "{0}`t{1}" -f $_.Name, $_.Repo }
    exit 0
}

if ($Init) {
    if (-not $destinations) { Write-Host 'No destinations configured (see the header).'; exit 1 }
    $bad = 0
    foreach ($d in $destinations) {
        $state = Get-RepoState $d.Repo
        if ($state -eq 'ready') { Write-Host "$($d.Name): already initialised"; continue }
        if ($state -eq 'unreachable') { Write-Host "$($d.Name): unreachable, check the remote / keys"; $bad = 1; continue }
        restic -r $d.Repo init --copy-chunker-params --from-repo $localRepo --from-password-file $passFile
        if ($LASTEXITCODE -ne 0) { $bad = 1 }
    }
    exit $bad
}

$start = Get-Date
Log "BEGIN $(Get-Date -Format o) destinations=$(($destinations | ForEach-Object Name) -join ',')"

if (-not $destinations)       { Write-Row '*' $start 'not-configured' '' '' ''; Finish 'not-configured' 1 }
if (-not (Test-Path $passFile)) { Write-Row '*' $start 'no-password' '' '' ''; Finish 'no-password' 1 }

# The noon run writes the stores, the catalog and the local repo. Copying a
# SQLite file mid-write captures a torn page, so wait for it to finish.
$deadline = $start.AddMinutes($WaitMinutes)
$task = Get-ScheduledTask -TaskName 'kk-ontario-update' -ErrorAction SilentlyContinue
while ($task -and $task.State -eq 'Running') {
    if ((Get-Date) -gt $deadline) { Write-Row '*' $start 'busy' '' '' ''; Finish 'busy' 1 }
    Start-Sleep -Seconds 60
    $task = Get-ScheduledTask -TaskName 'kk-ontario-update' -ErrorAction SilentlyContinue
}

if (-not (Test-Online)) { Write-Row '*' $start 'offline' '' '' ''; Finish 'offline' 0 }
if (Test-Metered)       { Write-Row '*' $start 'metered' '' '' ''; Finish 'metered' 0 }

# One destination failing never stops the other, and the run fails if any did.
$outcomes = @(foreach ($d in $destinations) { Backup-To $d })
if ($outcomes | Where-Object { $_ -ne 'ok' }) { Finish ($outcomes -join ',') 1 }
Finish 'ok' 0
