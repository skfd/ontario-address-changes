# Monthly article: from the 3rd of each month, write the previous month's
# newsletter piece for one city (offline variant, research notes, researched
# variant) with headless Claude runs, then commit and push articles\.
# Called daily at 15:00 by the kk-ontario-article scheduled task; every run
# after the month is written exits at once, and a month held by an open flag
# or an unfinished phase is retried the next day.
#
# Manual use:  .\monthly-article.ps1                     previous month, toronto
#              .\monthly-article.ps1 -Month 2026-08      a given month (no day gate)
#
# Outcomes (END line + logs\article-runs.csv): not-yet, done, waiting, offline,
# written, failed, publish-failed, error.

param(
    [string]$City = 'toronto',
    [string]$Month,
    [int]$FromDay = 3
)

$projectDir = $PSScriptRoot
Set-Location $projectDir
$env:PYTHONUNBUFFERED = '1'

$logDir  = "$projectDir\logs"
$logFile = "$logDir\article.log"
$runsCsv = "$logDir\article-runs.csv"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }

$claude = "$env:USERPROFILE\.local\bin\claude.exe"
# What the headless run may do without asking: this repo's files, the store,
# and the web for step 5b. Print mode denies anything else.
$claudeTools = 'Skill,Bash,Read,Write,Edit,Grep,Glob,WebSearch,WebFetch'

function Log([string]$msg) {
    Add-Content $logFile $msg
    Write-Host $msg
}

function Invoke-Logged([string]$commandLine) {
    cmd /c "$commandLine 2>&1" | ForEach-Object { Add-Content $logFile $_; Write-Host $_ }
}

function Test-Online {
    foreach ($ip in '1.1.1.1', '8.8.8.8', '9.9.9.9') {
        $tcp = [System.Net.Sockets.TcpClient]::new()
        try {
            if ($tcp.ConnectAsync($ip, 443).Wait(4000) -and $tcp.Connected) { return $true }
        } catch {} finally { $tcp.Dispose() }
    }
    return $false
}

function Wait-Online([int]$Minutes) {
    $deadline = (Get-Date).AddMinutes($Minutes)
    while (-not (Test-Online)) {
        if ((Get-Date) -ge $deadline) { return $false }
        Start-Sleep -Seconds 30
    }
    return $true
}

$runStart = Get-Date
$startLine = "START $(Get-Date -Format o) city=$City"
Set-Content $logFile $startLine
Write-Host $startLine

# One END line and one CSV row per run, whatever the outcome.
function Finish([string]$month, [string]$phase, [string]$outcome, [int]$exitCode) {
    Log "END $(Get-Date -Format o) month=$month phase=$phase outcome=$outcome"
    $row = [pscustomobject]@{
        started  = $runStart.ToString('o')
        finished = (Get-Date).ToString('o')
        city     = $City
        month    = $month
        phase    = $phase
        outcome  = $outcome
    }
    if (Test-Path $runsCsv) { $row | Export-Csv $runsCsv -NoTypeInformation -Append }
    else                    { $row | Export-Csv $runsCsv -NoTypeInformation }
    exit $exitCode
}

# Fixed calendar day: nothing happens before the 3rd. Later days only matter
# when the run on the 3rd left the month unwritten (waiting/offline/failed).
if (-not $Month -and (Get-Date).Day -lt $FromDay) {
    Log "NOT-YET day $((Get-Date).Day) < $FromDay"
    Finish '' 'gate' 'not-yet' 0
}

# Never overlap the noon update's git add/commit/push in the same tree: wait
# while a daily-update.ps1 process is alive. A live process, not update.log's
# END line: a run killed by its time limit never writes END (2026-09-08).
function Test-UpdateRunning {
    $procs = Get-CimInstance Win32_Process -Filter "Name = 'powershell.exe' OR Name = 'pwsh.exe'" -ErrorAction SilentlyContinue
    return @($procs | Where-Object { $_.CommandLine -like '*daily-update.ps1*' }).Count -gt 0
}
$deadline = (Get-Date).AddMinutes(90)
while (Test-UpdateRunning) {
    if ((Get-Date) -ge $deadline) {
        Log "UPDATE-STILL-RUNNING $(Get-Date -Format o) giving up for today"
        Finish '' 'gate' 'waiting' 0
    }
    Start-Sleep -Seconds 60
}

# The decision: which month, is it complete, is it flagged, what is missing.
$dueArgs = "--city $City"
if ($Month) { $dueArgs += " --month $Month" }
$dueOut  = cmd /c "python tools\article_due.py $dueArgs 2>&1"
$dueExit = $LASTEXITCODE
Log "DUE exit=$dueExit $dueOut"
try { $due = $dueOut | ConvertFrom-Json } catch { $due = $null }
$month = if ($due) { $due.month } else { $Month }

function Publish-Articles([string]$month) {
    # Commit whatever is in articles\ (all three files, plus the README row).
    # Returns $true when the tree is clean afterwards.
    Invoke-Logged "git add articles"
    if ($LASTEXITCODE -ne 0) { return $false }
    git diff --cached --quiet
    if ($LASTEXITCODE -eq 0) { return $true }   # nothing to commit
    Invoke-Logged "git commit -m `"monthly article: $City $month`""
    if ($LASTEXITCODE -ne 0) { return $false }
    Invoke-Logged "git push"
    return ($LASTEXITCODE -eq 0)
}

switch ($dueExit) {
    2 {
        # Written already. A commit or push that failed on an earlier run
        # still needs finishing, so this is not a pure no-op.
        $dirty = @(git status --porcelain -- articles).Count -gt 0
        if ($dirty) {
            Log "DONE-UNCOMMITTED $month publishing"
            if (Publish-Articles $month) { Finish $month 'publish' 'written' 0 }
            Finish $month 'publish' 'publish-failed' 1
        }
        Finish $month 'check' 'done' 0
    }
    3 { Log "WAITING $month $($due.reason)"; Finish $month 'check' 'waiting' 0 }
    0 { }
    default { Finish $month 'check' 'error' 1 }
}

if (-not (Wait-Online -Minutes 10)) {
    Log "OFFLINE $(Get-Date -Format o)"
    Finish $month 'check' 'offline' 0
}

# Runs one headless Claude phase. The prompt goes in through stdin from a file
# (a console stdin can make -p wait for input under Task Scheduler); output
# is teed to the log. Returns claude's exit code.
function Invoke-Claude([string]$phase, [string]$prompt) {
    $promptFile = "$logDir\article-prompt-$phase.txt"
    Set-Content -Path $promptFile -Value $prompt -Encoding UTF8
    Log "PHASE $phase $(Get-Date -Format o)"
    Invoke-Logged "type `"$promptFile`" | `"$claude`" -p --permission-mode dontAsk --allowedTools $claudeTools"
    return $LASTEXITCODE
}

$missing = @($due.missing)
$slug = $City

# Phase 1: the offline variant, from the store alone.
if ($missing -contains 'offline') {
    $prompt = @"
Invoke the monthly-article skill (Skill tool) and follow it for city '$slug', month $month.
Write ONLY the offline variant: articles/offline/$slug-$month.md. Do steps 1-5 and 6-8 of the loop for that variant.
Do NOT run step 5b (no web research, no WebSearch/WebFetch) and do NOT write the researched variant or research notes.
Do NOT git commit or push: the scheduled task that launched you commits afterwards.
If 'python run.py flags' shows an open flag for $slug dated inside $month, write nothing and reply WAITING with the reason.
When done, reply with the path of the file you wrote.
"@
    $code = Invoke-Claude 'offline' $prompt
    if ($code -ne 0 -or -not (Test-Path "articles\offline\$slug-$month.md")) {
        Log "FAILED offline exit=$code"
        Finish $month 'offline' 'failed' 1
    }
}

# Phase 2: research, then the researched variant as its own piece.
if (($missing -contains 'research') -or ($missing -contains 'researched')) {
    $prompt = @"
Invoke the monthly-article skill (Skill tool) and follow it for city '$slug', month $month.
The offline variant already exists at articles/offline/$slug-$month.md; read it, and re-run steps 3 and 5 so your numbers come from the brief and the store, not from that draft.
Now do step 5b exactly as references/research.md describes: research the month's named things, file the findings in articles/research/$slug-$month.md, then write the researched variant articles/researched/$slug-$month.md as its own piece (steps 6-8), with sourced links and the record's silences stated as silences.
Then add the $month row to the months table in articles/README.md, matching the existing rows.
Do NOT git commit or push: the scheduled task that launched you commits afterwards.
When done, reply with the paths you wrote.
"@
    $code = Invoke-Claude 'researched' $prompt
    $ok = ($code -eq 0) -and (Test-Path "articles\research\$slug-$month.md") -and (Test-Path "articles\researched\$slug-$month.md")
    if (-not $ok) {
        Log "FAILED researched exit=$code"
        Finish $month 'researched' 'failed' 1
    }
}

if (Publish-Articles $month) { Finish $month 'publish' 'written' 0 }
Finish $month 'publish' 'publish-failed' 1
