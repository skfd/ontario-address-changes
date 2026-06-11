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

    for ($k = 1; $k -lt $parts.Count; $k += 2) {
        $slug  = $parts[$k]
        $body  = $parts[$k + 1]
        $lines = $body -split "[`r`n]+" | Where-Object { $_.Trim() -ne '' }
        if ($lines) { $detail = $lines[-1].Trim() } else { $detail = '(starting...)' }
        $stage = Get-Stage $detail

        # The last section in the file is the one currently in progress.
        $active = ($k -eq $parts.Count - 2)
        $mark   = if ($active) { '>' } else { ' ' }
        Write-Host ("{0} {1,-16} [{2,-11}] {3}" -f $mark, $slug, $stage, $detail)
    }

    Write-Host ("-" * 72)
    Write-Host ("{0} of {1} datasets seen in this run." -f $sectionCount, $total)
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
