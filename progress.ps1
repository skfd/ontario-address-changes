# Shows progress of an update run by parsing its log.
# Works on both the combined `update --all` log and a per-city scheduled log,
# since run.py banners every city with "=== <slug> ===".
#
#   .\progress.ps1                 # snapshot of the newest log in logs\
#   .\progress.ps1 -Follow 3       # refresh every 3 seconds
#   .\progress.ps1 -Log logs\toronto.log

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

function Get-Stage {
    param([string]$line)
    switch -Regex ($line) {
        'ERROR'            { return 'ERROR' }
        '^querying|^fetched'{ return 'fetching' }
        '^downloading'     { return 'downloading' }
        '^parsed'          { return 'parsed' }
        '^snapshot '       { return 'imported' }
        'already imported' { return 'up-to-date' }
        'need \d+ to diff' { return 'baseline' }
        'no changes'       { return 'no changes' }
        '^diff '           { return 'diffed' }
        'wrote site'       { return 'reported' }
        default            { return 'running' }
    }
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

    # run.py prints "wrote site for N dataset(s)" once every city is done, before
    # the commit/push output. Its presence means nothing is still running.
    $runDone = $raw -match 'wrote site for \d+ dataset'

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

    Write-Host ("Log: {0}" -f $path)
    Write-Host ("Updated: {0:HH:mm:ss}   datasets in registry: {1}" -f $mtime, $total)
    Write-Host ("-" * 72)

    # Split on the "=== slug ===" banner; capturing group keeps the slug in results.
    $parts = [regex]::Split($raw, '={3}\s*(\S+)\s*={3}')
    $sectionCount = [math]::Floor(($parts.Count - 1) / 2)
    if ($sectionCount -le 0) {
        Write-Host "(no city sections yet)"
        return
    }

    $completed = [System.Collections.Generic.HashSet[string]]::new()
    for ($k = 1; $k -lt $parts.Count; $k += 2) {
        $slug  = $parts[$k]
        [void]$completed.Add($slug)
        $body  = $parts[$k + 1]
        # The report summary and git commit/push trail the last city's banner with
        # no banner of their own; drop them so they aren't read as that city's stage.
        $body  = ($body -split 'wrote site for \d+ dataset', 2)[0]
        $lines = @($body -split "[`r`n]+" | Where-Object { $_.Trim() -ne '' })
        if ($lines) { $detail = $lines[-1].Trim() } else { $detail = '(starting...)' }
        $stage = Get-Stage $detail

        # Until the run finishes, the last section is the one still in progress.
        $active = (-not $runDone) -and ($k -eq $parts.Count - 2)
        $mark   = if ($active) { '>' } else { ' ' }
        Write-Host ("{0} {1,-16} [{2,-11}] {3}" -f $mark, $slug, $stage, $detail)
    }

    Write-Host ("-" * 72)
    Write-Host ("{0} of {1} datasets seen in this run." -f $sectionCount, $total)

    # In parallel mode run.py prints a city's block only when it finishes, so the
    # number of sections == cities completed. ETA assumes a steady throughput.
    if (-not $startTime) {
        Write-Host "ETA: no START header in log (launch via daily-update.ps1 for ETA)."
        return
    }

    $done = $completed.Count
    $finished = ($done -ge $total)
    # While running, measure to now; once finished, freeze at last log write.
    $endRef  = if ($finished) { $mtime } else { Get-Date }
    $elapsed = $endRef - $startTime

    $fmt = { param($ts) "{0:00}:{1:00}:{2:00}" -f [int]$ts.TotalHours, $ts.Minutes, $ts.Seconds }

    if ($finished) {
        Write-Host ("Done. Elapsed {0} (finished {1:HH:mm:ss})." -f (& $fmt $elapsed), $mtime)
        return
    }

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

    $remaining = $null
    $source    = ''
    if ($median.Count -gt 0) {
        # Sum the expected time of cities not yet seen this run; unknown cities use
        # the overall median. With N workers the floor is the single longest pole.
        $fallback = ($median.Values | Sort-Object | Select-Object -Index ([int]($median.Count/2)))
        $allSlugs = Get-ChildItem "$PSScriptRoot\datasets\*.toml" | ForEach-Object { $_.BaseName }
        $pending  = @($allSlugs | Where-Object { -not $completed.Contains($_) })
        if ($pending.Count -gt 0) {
            $exp = $pending | ForEach-Object { if ($median.ContainsKey($_)) { $median[$_] } else { $fallback } }
            $sum = ($exp | Measure-Object -Sum).Sum
            $max = ($exp | Measure-Object -Maximum).Maximum
            $secs = [math]::Max($sum / $jobs, $max)
            $remaining = [TimeSpan]::FromSeconds($secs)
            $source = "history, {0} pending" -f $pending.Count
        }
    }

    if (-not $remaining -and $done -gt 0) {
        # No usable history yet: flat elapsed/done average.
        $remaining = [TimeSpan]::FromSeconds(($elapsed.TotalSeconds / $done) * ($total - $done))
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

if ($Follow -gt 0) {
    while ($true) {
        Clear-Host
        Show-Progress
        Start-Sleep -Seconds $Follow
    }
} else {
    Show-Progress
}
