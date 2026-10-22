# Monthly articles: from the 3rd of each month, write the previous month's
# newsletter piece for every city whose licence allows it, render the site
# copy, commit and push - one city at a time, so a run that dies keeps what
# it finished. A month in which nothing changed is written by
# tools\article_quiet.py from a fixed shape; a month with changes goes through
# a headless Claude run of the monthly-article skill (research notes, then
# the article). Called daily at 15:00 by the kk-ontario-article scheduled
# task (4 h limit): the Claude runs are capped per day by count and by
# wall-clock budget, so a month with thirty busy cities takes about a week
# of daily runs, and every run after the month is written exits at once.
#
# Manual use:  .\monthly-article.ps1                       previous month, every city
#              .\monthly-article.ps1 -City milton           one city
#              .\monthly-article.ps1 -Month 2026-08         a given month (no day gate)
#              .\monthly-article.ps1 -MaxClaude 12 -BudgetMinutes 300   a bigger batch
#
# Per-city outcomes (logs\article-runs.csv): quiet, written, failed,
# publish-failed, deferred (over the day's cap), waiting (open flag or
# incomplete month). Run outcomes (END line): not-yet, waiting, offline,
# error, or a summary of the per-city counts.

param(
    [string]$City,
    [string]$Month,
    [int]$FromDay = 3,
    [int]$MaxClaude = 6,
    [int]$BudgetMinutes = 150
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
$startLine = "START $(Get-Date -Format o) city=$(if ($City) { $City } else { 'all' })"
Set-Content $logFile $startLine
Write-Host $startLine

# One CSV row per city-month the run touched (and one for a run that never
# got that far), one END line per run.
function Record([string]$city, [string]$month, [string]$phase, [string]$outcome, [datetime]$since) {
    $row = [pscustomobject]@{
        started  = $since.ToString('o')
        finished = (Get-Date).ToString('o')
        city     = $city
        month    = $month
        phase    = $phase
        outcome  = $outcome
    }
    if (Test-Path $runsCsv) { $row | Export-Csv $runsCsv -NoTypeInformation -Append }
    else                    { $row | Export-Csv $runsCsv -NoTypeInformation }
}

function Finish([string]$month, [string]$phase, [string]$outcome, [int]$exitCode) {
    Log "END $(Get-Date -Format o) month=$month phase=$phase outcome=$outcome"
    exit $exitCode
}

# Fixed calendar day: nothing happens before the 3rd. Later days only matter
# while cities are left unwritten (deferred/waiting/failed).
if (-not $Month -and -not $City -and (Get-Date).Day -lt $FromDay) {
    Log "NOT-YET day $((Get-Date).Day) < $FromDay"
    Record '' '' 'gate' 'not-yet' $runStart
    Finish '' 'gate' 'not-yet' 0
}

# Never overlap the noon update's git add/commit/push in the same tree: wait
# while a daily-update.ps1 process is alive. A live process, not update.log's
# END line: a run killed by its time limit never writes END (2026-09-08).
# Checked again before every publish, because a batch can straddle the next
# noon run.
function Test-UpdateRunning {
    $procs = Get-CimInstance Win32_Process -Filter "Name = 'powershell.exe' OR Name = 'pwsh.exe'" -ErrorAction SilentlyContinue
    return @($procs | Where-Object { $_.CommandLine -like '*daily-update.ps1*' }).Count -gt 0
}

function Wait-UpdateDone([int]$Minutes) {
    $deadline = (Get-Date).AddMinutes($Minutes)
    while (Test-UpdateRunning) {
        if ((Get-Date) -ge $deadline) { return $false }
        Start-Sleep -Seconds 60
    }
    return $true
}

if (-not (Wait-UpdateDone 90)) {
    Log "UPDATE-STILL-RUNNING $(Get-Date -Format o) giving up for today"
    Record '' '' 'gate' 'waiting' $runStart
    Finish '' 'gate' 'waiting' 0
}

function Publish-Articles([string]$city, [string]$month) {
    # Render articles\ to docs\articles\ (the site copy), then commit both:
    # the Markdown files plus the README row, and the HTML pages. Returns
    # $true when the tree is clean afterwards.
    if (-not (Wait-UpdateDone 60)) { Log "PUBLISH-BLOCKED update running"; return $false }
    Invoke-Logged "python tools\render_articles.py"
    if ($LASTEXITCODE -ne 0) { Log "RENDER-FAILED articles exit=$LASTEXITCODE"; return $false }
    Invoke-Logged "git add articles docs\articles"
    if ($LASTEXITCODE -ne 0) { return $false }
    git diff --cached --quiet
    if ($LASTEXITCODE -eq 0) { return $true }   # nothing to commit
    $label = if ($city) { "$city $month" } else { "leftovers" }
    Invoke-Logged "git commit -m `"monthly article: $label`""
    if ($LASTEXITCODE -ne 0) { return $false }
    Invoke-Logged "git push"
    return ($LASTEXITCODE -eq 0)
}

# A commit or push that failed on an earlier run still needs finishing.
if (@(git status --porcelain -- articles).Count -gt 0) {
    Log "DIRTY articles from an earlier run: publishing"
    if (-not (Publish-Articles '' '')) { Record '' '' 'publish' 'publish-failed' $runStart }
}

# The decision: which city-months are complete, unflagged and unwritten.
$dueArgs = if ($City) { "--city $City" } else { "--all" }
if ($Month) { $dueArgs += " --month $Month" }
$dueOut = cmd /c "python tools\article_due.py $dueArgs 2>&1"
Log "DUE exit=$LASTEXITCODE $dueOut"
try { $due = @($dueOut | ConvertFrom-Json) } catch { $due = $null }
if ($null -eq $due) {
    Record $City $Month 'check' 'error' $runStart
    Finish $Month 'check' 'error' 1
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

$counts = @{}
function Count([string]$outcome) { $counts[$outcome] = 1 + [int]$counts[$outcome] }
$claudeRuns = 0

foreach ($item in $due) {
    $slug = $item.city; $month = $item.month
    $since = Get-Date
    # (if/elseif, not switch: `continue` inside a switch block leaves the
    # switch, not the foreach, and a done city would fall through to Claude.)
    if ($item.status -eq 'done') { continue }
    elseif ($item.status -eq 'waiting') {
        Log "WAITING $slug $month $($item.reason)"
        Record $slug $month 'check' 'waiting' $since; Count 'waiting'; continue
    }
    elseif ($item.status -ne 'due') {
        Log "ERROR $slug $month $($item.reason)"
        Record $slug $month 'check' 'error' $since; Count 'error'; continue
    }

    if ($item.quiet) {
        # Nothing changed: a fixed shape, no Claude.
        Invoke-Logged "python tools\article_quiet.py --city $slug --month $month"
        if ($LASTEXITCODE -ne 0) { Log "QUIET-FAILED $slug $month exit=$LASTEXITCODE"; Record $slug $month 'quiet' 'failed' $since; Count 'failed'; continue }
        if (Publish-Articles $slug $month) { Record $slug $month 'publish' 'quiet' $since; Count 'quiet' }
        else { Record $slug $month 'publish' 'publish-failed' $since; Count 'publish-failed' }
        continue
    }

    # A month with changes: the skill, headless. Capped per day so the batch
    # fits the task's time limit; what is left over is picked up tomorrow.
    $elapsed = ((Get-Date) - $runStart).TotalMinutes
    if ($claudeRuns -ge $MaxClaude -or $elapsed -ge $BudgetMinutes) {
        Log "DEFERRED $slug $month (runs=$claudeRuns elapsed=$([int]$elapsed)m)"
        Record $slug $month 'check' 'deferred' $since; Count 'deferred'; continue
    }
    if (-not (Wait-Online -Minutes 10)) {
        Log "OFFLINE $(Get-Date -Format o)"
        Record $slug $month 'check' 'offline' $since
        Finish $month 'check' 'offline' 0
    }

    $prompt = @"
Invoke the monthly-article skill (Skill tool) and follow it for city '$slug', month $month.
Do steps 1-5 of the loop so your numbers come from the brief and the store: 'python tools/month_digest.py --city $slug --month $month'.
If 'python run.py flags' shows an open flag for $slug dated inside $month, write nothing and reply WAITING with the reason.
Then do step 5b exactly as references/research.md describes: research the month's named things, file the findings in articles/research/$slug-$month.md, then write the article articles/researched/$slug-$month.md (steps 6-8), with sourced links and the record's silences stated as silences.
The attribution footer is the 'attribution line' printed in the brief's header, verbatim, plus the 'site' link; do not compose a licence line of your own.
Then add the $month row for $slug to the months table in articles/README.md: '| $month | $slug | <net> | <lead> |', keeping the table ordered by month then city.
Do NOT git commit or push: the script that launched you commits afterwards.
When done, reply with the paths you wrote.
"@
    $claudeRuns++
    $code = Invoke-Claude "$slug-$month" $prompt
    $ok = ($code -eq 0) -and (Test-Path "articles\research\$slug-$month.md") -and (Test-Path "articles\researched\$slug-$month.md")
    if (-not $ok) {
        Log "FAILED $slug $month exit=$code"
        Record $slug $month 'article' 'failed' $since; Count 'failed'
        continue
    }
    if (Publish-Articles $slug $month) { Record $slug $month 'publish' 'written' $since; Count 'written' }
    else { Record $slug $month 'publish' 'publish-failed' $since; Count 'publish-failed' }
}

$summary = ($counts.GetEnumerator() | Sort-Object Name | ForEach-Object { "$($_.Name)=$($_.Value)" }) -join ' '
if (-not $summary) { $summary = 'done' }
Finish $Month 'batch' $summary $(if ($counts['failed'] -or $counts['publish-failed'] -or $counts['error']) { 1 } else { 0 })
