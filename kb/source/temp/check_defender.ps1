$ErrorActionPreference = 'SilentlyContinue'
Write-Output "===== DEFENDER SERVICES ====="
Get-Service WinDefend, WdNisSvc, WdNisDrv, SecurityHealthService |
    Select-Object Name, Status, StartType | Format-Table -AutoSize | Out-String -Width 120

Write-Output "===== DEFENDER STATUS ====="
$c = Get-MpComputerStatus
Write-Output ("AMRunningMode        : " + $c.AMRunningMode)
Write-Output ("AntivirusEnabled     : " + $c.AntivirusEnabled)
Write-Output ("RealTimeProtection   : " + $c.RealTimeProtectionEnabled)
Write-Output ("BehaviorMonitor      : " + $c.BehaviorMonitorEnabled)
Write-Output ("SigLastUpdated       : " + $c.AntivirusSignatureLastUpdated)

Write-Output "===== THIRD-PARTY AV ====="
Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntiVirusProduct |
    Select-Object displayName, productState | Format-Table -AutoSize | Out-String -Width 120

Write-Output "===== RECENT SUSPICIOUS PROCESSES (non-Microsoft, running now) ====="
Get-Process | Where-Object { $_.Path -and $_.Path -notlike "C:\Windows\*" -and
    $_.Path -notlike "C:\Program Files*" -and $_.Path -notlike "*\Python*" } |
    Select-Object -First 20 ProcessName, Id, Path | Format-Table -AutoSize | Out-String -Width 160
