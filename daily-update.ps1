# Daily refresh: update all datasets in parallel, then commit and push the
# regenerated site. Called by the kk-ontario-update scheduled task.
# Commits docs/ even when some cities failed (their reports are simply stale);
# exits with update's code so the task's retry still fires for the failures.

$projectDir = $PSScriptRoot
Set-Location $projectDir

# First log line is the run anchor progress.ps1 uses for elapsed/ETA.
Write-Output "START $(Get-Date -Format o) jobs=6"

python run.py update --all --jobs 6
$updateExit = $LASTEXITCODE

git add docs
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    git commit -m "daily update $(Get-Date -Format yyyy-MM-dd)"
    git push
}

exit $updateExit
