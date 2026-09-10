# Hourly flag review, 18:00-22:00: mirror the open flag queue to GitHub
# issues, file what the operator answered there, let headless Claude triage
# the rest, then re-render, push and close what is settled. Called by the
# kk-ontario-flags scheduled task; safe to run by hand.
#
#   open     one issue per open flag-day (ledger or vault) that has none
#   apply    the operator's business / vault / hold answers, filed directly
#   claude   technical/bug answers that need a config rule, and days nobody
#            has looked at -- the review-flags skill, in print mode
#   publish  render filed cities, commit flags.toml + datasets + docs, push,
#            reply on each issue with the commit, close it
#
# Skipped whole (exit 0, SKIP line) when offline, when the noon update or the
# article task is mid-run (both commit from this tree), or when a previous
# pass of this script has not finished. Outcomes (END line + runs CSV):
# done, nothing, offline, busy, failed.

param([switch]$NoClaude)

$projectDir = $PSScriptRoot
Set-Location $projectDir
$env:PYTHONUNBUFFERED = '1'
$env:PYTHONIOENCODING = 'utf-8'

$logDir  = "$projectDir\logs"
$logFile = "$logDir\flags-review.log"
$runsCsv = "$logDir\flags-review-runs.csv"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }

$claude = "$env:USERPROFILE\.local\bin\claude.exe"
# This repo's files, the store, gh through tools/flag_issues.py, and the web
# for a proposal that wants a municipal news page. Print mode denies the rest.
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

# A log whose last START has no END after it is a run still going (or one
# killed by its time limit, which looks the same and is just as unsafe to
# commit over -- it clears on that task's next run).
function Test-Unfinished([string]$log, [int]$staleHours) {
    if (-not (Test-Path $log)) { return $false }
    $lines = Get-Content $log
    $start = ($lines | Select-String -Pattern '^START ' | Select-Object -Last 1)
    $end   = ($lines | Select-String -Pattern '^END '   | Select-Object -Last 1)
    if (-not $start) { return $false }
    if ($end -and $end.LineNumber -gt $start.LineNumber) { return $false }
    # Killed runs never write END; past the task's own time limit, it is over.
    $stamp = ($start.Line -split ' ')[1]
    try { $t = [datetime]::Parse($stamp) } catch { return $true }
    return ((Get-Date) - $t).TotalHours -lt $staleHours
}

$runStart = Get-Date
function Finish([string]$phase, [string]$outcome, [int]$exitCode) {
    Log "END $(Get-Date -Format o) phase=$phase outcome=$outcome"
    $row = [pscustomobject]@{
        started  = $runStart.ToString('o')
        finished = (Get-Date).ToString('o')
        phase    = $phase
        outcome  = $outcome
    }
    if (Test-Path $runsCsv) { $row | Export-Csv $runsCsv -NoTypeInformation -Append }
    else                    { $row | Export-Csv $runsCsv -NoTypeInformation }
    exit $exitCode
}

# The previous pass of this script is the first thing to check -- before we
# overwrite its log.
if (Test-Unfinished $logFile 1) {
    Add-Content $logFile "SKIP $(Get-Date -Format o) previous pass unfinished"
    exit 0
}
Set-Content $logFile "START $(Get-Date -Format o)"
Write-Host "START $(Get-Date -Format o)"

if (Test-Unfinished "$logDir\update.log" 3)  { Log "BUSY update";  Finish 'check' 'busy' 0 }
if (Test-Unfinished "$logDir\article.log" 5) { Log "BUSY article"; Finish 'check' 'busy' 0 }
if (-not (Test-Online)) { Log "OFFLINE"; Finish 'check' 'offline' 0 }

# The daily run pushes from this same tree, so there is nothing to pull. A
# stale git lock would stall publish the way it stalled the 08-05 daily run;
# sweep the hour-old ones, as daily-update.ps1 does.
$gitDir = Join-Path $projectDir '.git'
foreach ($lock in @(Get-ChildItem $gitDir -Filter '*.lock' -Recurse -Force -File -ErrorAction SilentlyContinue)) {
    if (((Get-Date) - $lock.LastWriteTime).TotalMinutes -gt 60) {
        Log "STALE-LOCK removing $($lock.FullName.Substring($projectDir.Length + 1))"
        Remove-Item -Force $lock.FullName
    }
}

Log "OPEN $(Get-Date -Format o)"
Invoke-Logged "python tools\flag_issues.py open"
if ($LASTEXITCODE -ne 0) { Log "FAILED open exit=$LASTEXITCODE"; Finish 'open' 'failed' 1 }

Log "APPLY $(Get-Date -Format o)"
Invoke-Logged "python tools\flag_issues.py apply"
if ($LASTEXITCODE -ne 0) { Log "FAILED apply exit=$LASTEXITCODE"; Finish 'apply' 'failed' 1 }

# Anything still in the inbox is Claude's: technical/bug answers wanting a
# rule, and days nobody has looked at. Four per pass: a triage can mean a
# config edit plus a store backfill on a large city, and a pass killed at its
# time limit leaves that half-applied. The next hour takes the rest.
$inbox = python tools\flag_issues.py inbox --json --limit 4 | ConvertFrom-Json
$count = @($inbox).Count
Log "INBOX $count item(s) for Claude"
if ($count -gt 0 -and -not $NoClaude) {
    $prompt = @"
Invoke the review-flags skill (Skill tool) and follow its GitHub section.
Run ``python tools/flag_issues.py inbox --limit 4`` and work those items in that order; leave the rest for the next hour.

- kind=operator: the operator already ruled technical or bug on the issue (their note, and a ``rule`` hint if they gave one, are in the inbox). Make the rule real exactly as the skill's step 5 says (config edit, backfill if ignore_fields/keep_fields changed), then file with
  ``python tools/flag_issues.py file <number> --from-comment <comment_id> --verdict <verdict> --note "<their note>" --rule "<what you changed>"`` (add ``--vault <real|schema|artifact>`` only if their comment said so).
- kind=triage: run ``python .claude/skills/review-flags/brief.py <slug> <date>`` and decide per the skill's table. If it is plainly technical or bug (one field recoded 1:1, a value-preserving restyle, a field appearing or vanishing everywhere, a replayed batch the vault also called artifact), make the rule real and file it with ``file --verdict ... --rule ... --note ...``; add ``--vault schema`` or ``--vault artifact`` when the vault flagged the same day and the brief supports it. If it could be business, or you are not sure, do NOT file: post ``python tools/flag_issues.py propose <number> --verdict <your reading> --note "<evidence, and the one thing that would settle it>"``. For a vault-only item, the same with ``--vault`` instead of ``--verdict``; never file ``real``.
- You cannot file ``business`` or vault ``real``; the tool refuses them without the owner's comment. Never edit flags.toml by hand; ``file`` edits it.
- Do NOT run ``run.py report``, and do NOT git commit or push: the script that launched you renders, commits and closes the issues afterwards.
- Keep every note to the point: what it was, which rows, why that verdict.
When done, reply with one line per issue: number, what you did.
"@
    $promptFile = "$logDir\flags-review-prompt.txt"
    Set-Content -Path $promptFile -Value $prompt -Encoding UTF8
    Log "CLAUDE $(Get-Date -Format o)"
    Invoke-Logged "type `"$promptFile`" | `"$claude`" -p --permission-mode dontAsk --allowedTools $claudeTools"
    if ($LASTEXITCODE -ne 0) { Log "CLAUDE-FAILED exit=$LASTEXITCODE" }
}

Log "PUBLISH $(Get-Date -Format o)"
Invoke-Logged "python tools\flag_issues.py publish"
if ($LASTEXITCODE -ne 0) { Log "FAILED publish exit=$LASTEXITCODE"; Finish 'publish' 'failed' 1 }

Finish 'publish' 'done' 0
