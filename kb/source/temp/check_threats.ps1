$ErrorActionPreference = 'SilentlyContinue'
$out = New-Object System.Collections.Generic.List[string]

try {
    $dets = Get-MpThreatDetection -ErrorAction Stop | Sort-Object InitialDetectionTime -Descending | Select-Object -First 15
    foreach ($d in $dets) {
        $out.Add("TIME : " + $d.InitialDetectionTime)
        $out.Add("  PROC : " + (($d.ProcessName | Select-Object -First 2) -join ','))
        $out.Add("  RES  : " + (($d.Resources | Select-Object -First 3) -join ' | '))
        $out.Add("  ACTION: " + $d.ThreatStatusID)
    }
} catch {
    $out.Add("Detection ERR: " + $_.Exception.Message)
}

$out.Add("========== THREATS ==========")
try {
    $ts = Get-MpThreat -ErrorAction Stop | Select-Object -First 15
    foreach ($t in $ts) {
        $out.Add("THREAT: " + $t.ThreatName + "  (Sev=" + $t.SeverityID + ")")
        $out.Add("  RES: " + (($t.Resources | Select-Object -First 3) -join ' | '))
    }
} catch {
    $out.Add("Threat ERR: " + $_.Exception.Message)
}

$out | Out-String -Width 200
