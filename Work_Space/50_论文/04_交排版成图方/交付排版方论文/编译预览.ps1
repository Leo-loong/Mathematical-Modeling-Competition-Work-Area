# Save-and-compile preview (Word-like live preview)
# Usage: double-click 编译预览.bat  (or run: powershell -File 编译预览.ps1)
# NOTE: keep this file ASCII-only -- Windows PowerShell 5.1 reads .ps1 as ANSI when it has no BOM,
#       so non-ASCII text here would break the script.
$ErrorActionPreference = 'SilentlyContinue'
Set-Location -Path $PSScriptRoot
chcp 65001 | Out-Null

Write-Host ''
Write-Host '  Watching: main.tex / preamble.tex / sections\*.tex / frontmatter\*.tex' -ForegroundColor Cyan
Write-Host '  On save -> xelatex runs twice (about 1-2 min). Stop with Ctrl+C.' -ForegroundColor Cyan
Write-Host '  Tip: view the PDF in TeXworks (it does not lock the file). WPS/Acrobat lock main.pdf and break the build.' -ForegroundColor DarkGray
Write-Host ''

function Get-Stamp {
    $f = @()
    $f += Get-Item 'main.tex', 'preamble.tex' -ErrorAction SilentlyContinue
    $f += Get-ChildItem 'sections\*.tex' -ErrorAction SilentlyContinue
    $f += Get-ChildItem 'frontmatter\*.tex' -ErrorAction SilentlyContinue
    ($f | Sort-Object FullName | ForEach-Object { $_.LastWriteTime.Ticks }) -join ','
}

$last = Get-Stamp
while ($true) {
    Start-Sleep -Milliseconds 900
    $now = Get-Stamp
    if ($now -ne $last) {
        $last = $now
        Write-Host ('[{0}] changed -> compiling...' -f (Get-Date -Format 'HH:mm:ss')) -ForegroundColor Yellow
        & xelatex -interaction=nonstopmode -synctex=1 main.tex | Out-Null
        & xelatex -interaction=nonstopmode -synctex=1 main.tex | Out-Null
        $line = (Select-String -Path 'main.log' -Pattern 'Output written' | Select-Object -Last 1).Line
        $miss = (Select-String -Path 'main.log' -Pattern 'Missing character' | Measure-Object).Count
        $ovf = (Select-String -Path 'main.log' -Pattern 'Overfull \\hbox' | Measure-Object).Count
        Write-Host ('    {0}  | missing {1}  | overfull {2}' -f $line.Trim(), $miss, $ovf) -ForegroundColor Green
    }
}
