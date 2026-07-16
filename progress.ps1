# Shows progress of an update run by parsing its log.
# run.py in parallel mode prints each city's block only when it finishes, so
# mid-run the log can only tell us done/failed/pending counts - no live stages.
#
#   .\progress.ps1                 # snapshot of the newest log in logs\
#   .\progress.ps1 -Follow 3       # refresh every 3 seconds
#   .\progress.ps1 -Log logs\update.log

param(
    [string]$Log,
    [int]$Follow = 0
)

$logDir = "$PSScriptRoot\logs"

function Resolve-Log {
    if ($Log) {
        if ([System.IO.Path]::IsPathRooted($Log)) { return $Log }
        return Join-Path $PSScriptRoot $Log
    }
    $f = Get-ChildItem "$logDir\*.log" -ErrorAction SilentlyContinue |
         Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($f) { return $f.FullName }
    return $null
}

# One short cause per failed city, condensed from its ERROR line.
function Get-ErrorSummary {
    param([string]$body)
    $errLine = @($body -split "[`r`n]+" | Where-Object { $_ -match 'ERROR' }) | Select-Object -First 1
    if (-not $errLine) { return 'failed (no ERROR line in log)' }
    $hostName = if ($errLine -match "host='([^']+)'") { $matches[1] } else { '' }
    $cause = if ($errLine -match 'Caused by (\w+?)(?:Error)?\(') { $matches[1] }
             elseif ($errLine -match 'Read timed out')           { 'ReadTimeout' }
             else {
                 $msg = ($errLine -replace '^\s*ERROR \([^)]+\):\s*', '').Trim()
                 if ($msg.Length -gt 70) { $msg.Substring(0, 70) + '...' } else { $msg }
             }
    if ($hostName) { return "$cause  $hostName" }
    return $cause
}

function Show-Progress {
    $path = Resolve-Log
    if (-not $path -or -not (Test-Path $path)) {
        Write-Host "No log files found in $logDir."
        return
    }

    $raw   = Get-Content -Raw -LiteralPath $path
    $total = (Get-ChildItem "$PSScriptRoot\datasets\*.toml" -ErrorAction SilentlyContinue).Count
    $mtime = (Get-Item $path).LastWriteTime

    # daily-update.ps1 writes "START <iso8601> jobs=<N>" as the log's first line.
    $startTime = $null
    $jobs      = 6
    $firstLine = ($raw -split "[`r`n]+", 2)[0]
    if ($firstLine -match '^START\s+(\S+)(?:\s+jobs=(\d+))?') {
        try {
            $startTime = [datetime]::Parse(
                $matches[1], $null,
                [System.Globalization.DateTimeStyles]::RoundtripKind)
        } catch { $startTime = $null }
        if ($matches[2]) { $jobs = [int]$matches[2] }
    }

    Write-Host ("Log: {0}  (updated {1:HH:mm:ss})" -f $path, $mtime)
    Write-Host ""

    # Split on the "=== slug ===" banner; capturing group keeps the slug in results.
    $parts = [regex]::Split($raw, '={3}\s*(\S+)\s*={3}')
    if ($parts.Count -lt 3) {
        # A fully skipped run never prints a city banner, only OFFLINE/METERED lines.
        if ($raw -match '(?m)^(OFFLINE|METERED) ') {
            $why = if ($matches[1] -eq 'METERED') { 'metered connection' } else { 'no internet' }
            if ($raw -match '(?m)^END ') {
                Write-Host "Run skipped: $why (treated like the laptop being off)."
                Write-Host "Rerun manually once on a usable network: .\daily-update.ps1"
            } else {
                Write-Host "Skipping so far: $why (attempts continue 15 min apart)."
            }
            Show-History -Total $total
        } else {
            Write-Host "(no city sections yet)"
        }
        return
    }

    # Retry attempts reprint a city's banner; keep only its last section.
    $sections = [ordered]@{}
    for ($k = 1; $k -lt $parts.Count; $k += 2) {
        # "wrote site for N dataset(s)" and the git output trail the last city's
        # banner with no banner of their own; drop them from that city's body.
        $sections[$parts[$k]] = ($parts[$k + 1] -split 'wrote site for \d+ dataset', 2)[0]
    }
    $ok     = [System.Collections.Generic.List[string]]::new()
    $failed = [System.Collections.Generic.List[object]]::new()
    foreach ($e in $sections.GetEnumerator()) {
        if ($e.Value -match 'ERROR|update failed') {
            $failed.Add([pscustomobject]@{ Slug = $e.Key; Why = Get-ErrorSummary $e.Value })
        } else {
            $ok.Add($e.Key)
        }
    }

    $seen    = $ok.Count + $failed.Count
    $pending = [math]::Max($total - $seen, 0)
    # daily-update.ps1 writes an END line when the run (incl. retries) is over;
    # a RETRY line without it means an attempt is still in flight. Logs without
    # retries fall back to "wrote site" (prints once every city is done) or,
    # with zero successes, all-cities-seen.
    $finished = if ($raw -match '(?m)^END ') { $true }
                elseif ($raw -match '(?m)^RETRY ') { $false }
                else { ($raw -match 'wrote site for \d+ dataset') -or ($seen -ge $total) }

    $status = if (-not $finished) {
                  if ($raw -match '(?m)^RETRY ') { 'Retrying failures' } else { 'Running' }
              }
              # daily-update.ps1 stamps exit=offline/metered when the machine
              # had no usable network -- failures below are noise, not real.
              elseif ($raw -match '(?m)^END .*exit=offline') { 'Run offline (treated like laptop off)' }
              elseif ($raw -match '(?m)^END .*exit=metered') { 'Run skipped (metered connection)' }
              elseif ($failed.Count)   { 'Run finished with failures' }
              else                     { 'Run OK' }
    Write-Host ("{0}: {1} ok, {2} failed, {3} pending (of {4})" -f `
        $status, $ok.Count, $failed.Count, $pending, $total)

    # --- elapsed / ETA ---------------------------------------------------
    $fmt = { param($ts) "{0:00}:{1:00}:{2:00}" -f [int]$ts.TotalHours, $ts.Minutes, $ts.Seconds }
    if ($startTime) {
        # While running, measure to now; once finished, freeze at last log write.
        $endRef  = if ($finished) { $mtime } else { Get-Date }
        $elapsed = $endRef - $startTime
        if ($finished) {
            Write-Host ("Elapsed {0} (finished {1:HH:mm:ss})" -f (& $fmt $elapsed), $mtime)
        } else {
            # Per-city median seconds from history (run.py appends logs\timings.csv).
            $median = @{}
            $csv = "$PSScriptRoot\logs\timings.csv"
            if (Test-Path $csv) {
                Import-Csv $csv | Group-Object slug | ForEach-Object {
                    $v = @($_.Group.seconds | ForEach-Object { [double]$_ } | Sort-Object)
                    $n = $v.Count
                    $median[$_.Name] = if ($n % 2) { $v[($n-1)/2] } else { ($v[$n/2-1] + $v[$n/2]) / 2 }
                }
            }

            $seenSlugs = [System.Collections.Generic.HashSet[string]]::new()
            $ok     | ForEach-Object { [void]$seenSlugs.Add($_) }
            $failed | ForEach-Object { [void]$seenSlugs.Add($_.Slug) }

            $remaining = $null
            $source    = ''
            if ($median.Count -gt 0) {
                # Sum the expected time of cities not yet seen this run; unknown
                # cities use the overall median. With N workers the floor is the
                # single longest pole.
                $fallback = ($median.Values | Sort-Object | Select-Object -Index ([int]($median.Count/2)))
                $allSlugs = Get-ChildItem "$PSScriptRoot\datasets\*.toml" | ForEach-Object { $_.BaseName }
                $notSeen  = @($allSlugs | Where-Object { -not $seenSlugs.Contains($_) })
                if ($notSeen.Count -gt 0) {
                    $exp = $notSeen | ForEach-Object { if ($median.ContainsKey($_)) { $median[$_] } else { $fallback } }
                    $sum = ($exp | Measure-Object -Sum).Sum
                    $max = ($exp | Measure-Object -Maximum).Maximum
                    $remaining = [TimeSpan]::FromSeconds([math]::Max($sum / $jobs, $max))
                    $source = 'history'
                }
            }
            if (-not $remaining -and $seen -gt 0) {
                # No usable history yet: flat elapsed/done average.
                $remaining = [TimeSpan]::FromSeconds(($elapsed.TotalSeconds / $seen) * $pending)
                $source = 'flat avg'
            }

            if ($remaining) {
                $eta = (Get-Date) + $remaining
                Write-Host ("Elapsed {0}  |  ETA ~{1} remaining  |  finish ~{2:HH:mm:ss}  ({3})" -f `
                    (& $fmt $elapsed), (& $fmt $remaining), $eta, $source)
            } else {
                Write-Host ("Elapsed {0}. ETA: estimating (no cities finished yet)..." -f (& $fmt $elapsed))
            }
        }
    } elseif (-not $finished) {
        Write-Host "ETA: no START header in log (launch via daily-update.ps1 for ETA)."
    }

    # --- failures --------------------------------------------------------
    if ($failed.Count -gt 0) {
        Write-Host ""
        Write-Host "Failures:"
        $show = $failed | Select-Object -First 15
        foreach ($f in $show) {
            Write-Host ("  {0,-20} {1}" -f $f.Slug, $f.Why)
        }
        if ($failed.Count -gt 15) {
            Write-Host ("  ... ({0} more; see {1})" -f ($failed.Count - 15), $path)
        }
    }

    Show-History -Total $total
    Show-TaskVerdict -Finished $finished -FailedCount $failed.Count
}

# Last 7 days: successes/day from timings.csv, commit from git history, run
# outcome from runs.csv (written by daily-update.ps1 since 2026-07-16).
function Show-History {
    param([int]$Total)

    $okPerDay = @{}
    $csv = "$PSScriptRoot\logs\timings.csv"
    if (Test-Path $csv) {
        Import-Csv $csv | ForEach-Object {
            $d = ($_.finished_iso -split 'T')[0]
            if ($okPerDay.ContainsKey($d)) { $okPerDay[$d]++ } else { $okPerDay[$d] = 1 }
        }
    }

    $committed = @{}
    git -C $PSScriptRoot log --since=8.days --format=%s 2>$null | ForEach-Object {
        if ($_ -match '^daily update (\d{4}-\d\d-\d\d)') { $committed[$matches[1]] = $true }
    }

    $runs = @{}
    $runsCsv = "$PSScriptRoot\logs\runs.csv"
    if (Test-Path $runsCsv) {
        Import-Csv $runsCsv | ForEach-Object {
            $runs[($_.started -split 'T')[0]] = $_   # last run of the day wins
        }
    }

    Write-Host ""
    Write-Host "Last 7 days:"
    for ($i = 6; $i -ge 0; $i--) {
        $day = (Get-Date).Date.AddDays(-$i).ToString('yyyy-MM-dd')
        $okN = 0
        if ($okPerDay.ContainsKey($day)) { $okN = $okPerDay[$day] }
        $commit = if ($committed.ContainsKey($day)) { 'committed' } else { 'no commit' }
        $note = ''
        if ($runs.ContainsKey($day)) {
            $r = $runs[$day]
            $note = if ($r.exit -eq 'offline') { 'offline (like laptop off)' }
                    elseif ($r.exit -eq 'metered') { 'skipped (metered connection)' }
                    elseif ([int]$r.exit -eq 0) { "run ok ({0} attempt(s))" -f $r.attempts }
                    else { "run FAILED after {0} attempt(s)" -f $r.attempts }
        } elseif ($okN -eq 0) {
            $note = 'no run recorded'
        }
        Write-Host ("  {0}  {1,3}/{2} ok  {3,-10} {4}" -f $day, $okN, $Total, $commit, $note)
    }
}

# Answers "do I need to rerun manually?" from the scheduled task's state.
function Show-TaskVerdict {
    param([bool]$Finished, [int]$FailedCount)

    Write-Host ""
    $info = $null
    try { $info = Get-ScheduledTaskInfo -TaskName 'kk-ontario-update' -ErrorAction Stop } catch {}
    if (-not $info) {
        Write-Host "Task kk-ontario-update not registered (run schedule-add.ps1)."
        return
    }
    Write-Host ("Task: last run {0:yyyy-MM-dd HH:mm} (exit {1}), next run {2:yyyy-MM-dd HH:mm}." -f `
        $info.LastRunTime, $info.LastTaskResult, $info.NextRunTime)

    if (-not $Finished) {
        Write-Host "-> Run still in progress (daily-update.ps1 retries failures itself, 15 min apart)."
    } elseif ($FailedCount -gt 0) {
        Write-Host "-> Retries exhausted; the task will NOT run again before its next trigger."
        Write-Host "   Rerun manually: .\daily-update.ps1  (updated cities short-circuit, so it's cheap)"
    } else {
        Write-Host "-> All good; nothing to do."
    }
}

if ($Follow -gt 0) {
    while ($true) {
        Clear-Host
        Show-Progress
        Start-Sleep -Seconds $Follow
    }
} else {
    Show-Progress
}
