# 使用 Windows 内置 OCR（zh-Hans-CN）识别 PNG，输出带坐标的行文本 TSV
# 用法: powershell -File winocr.ps1 [批号] [并发无关，单进程顺序]
param([int]$Shard = -1, [int]$Shards = 1, [string]$PngDir = "", [string]$TsvDir = "")

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
if ($PngDir -eq "") { $PngDir = Join-Path $root "ocr_png" }
if ($TsvDir -eq "") { $TsvDir = Join-Path $root "ocr_tsv" }
$pngDir = $PngDir
$tsvDir = $TsvDir
if (-not (Test-Path $tsvDir)) { New-Item -ItemType Directory -Path $tsvDir | Out-Null }

Add-Type -AssemblyName System.Runtime.WindowsRuntime

$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType = WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Globalization.Language, Windows.Foundation, ContentType = WindowsRuntime]

$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
        $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and
        $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'
    })[0]

function Await($op, $type) {
    $m = $asTaskGeneric.MakeGenericMethod($type)
    $t = $m.Invoke($null, @($op))
    $t.Wait(-1) | Out-Null
    return $t.Result
}

$lang = New-Object Windows.Globalization.Language "zh-Hans-CN"
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($lang)
if ($null -eq $engine) { Write-Output "NO_ENGINE"; exit 1 }

$enc = New-Object System.Text.UTF8Encoding($false)
$files = Get-ChildItem -Path $pngDir -Filter *.png -File | Sort-Object Name
$idx = 0
$done = 0
foreach ($f in $files) {
    if ($Shards -gt 1) {
        if (($idx % $Shards) -ne $Shard) { $idx++; continue }
    }
    $idx++
    $out = Join-Path $tsvDir ($f.BaseName + ".tsv")
    if (Test-Path $out) { $done++; continue }
    try {
        $sf = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($f.FullName)) ([Windows.Storage.StorageFile])
        $st = Await ($sf.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
        $dec = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($st)) ([Windows.Graphics.Imaging.BitmapDecoder])
        $bmp = Await ($dec.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
        $res = Await ($engine.RecognizeAsync($bmp)) ([Windows.Media.Ocr.OcrResult])
        $lines = New-Object System.Collections.Generic.List[string]
        foreach ($ln in $res.Lines) {
            $r = $ln.BoundingRect
            $t = $ln.Text -replace "`t", " " -replace "`r", "" -replace "`n", ""
            $lines.Add(("{0}`t{1}`t{2}`t{3}`t{4}" -f [int]$r.X, [int]$r.Y, [int]($r.X + $r.Width), [int]($r.Y + $r.Height), $t))
        }
        [System.IO.File]::WriteAllLines($out, $lines, $enc)
        $st.Dispose()
        $done++
        if (($done % 10) -eq 0) { Write-Output ("done " + $done + " last=" + $f.Name) }
    } catch {
        Write-Output ("ERR " + $f.Name + " : " + $_.Exception.Message)
    }
}
Write-Output ("FINISHED shard=" + $Shard + " processed=" + $done)
