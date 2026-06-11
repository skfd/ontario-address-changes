# Removes all per-city tasks (kk-*) plus the legacy OntarioAddressChanges task.

$prefix = "kk"

$tasks = Get-ScheduledTask | Where-Object {
    $_.TaskName -like "$prefix-*" -or $_.TaskName -eq "OntarioAddressChanges"
}

if (-not $tasks) {
    Write-Host "No matching scheduled tasks found."
    return
}

foreach ($t in $tasks) {
    Unregister-ScheduledTask -TaskName $t.TaskName -Confirm:$false
    Write-Host "Removed '$($t.TaskName)'."
}
