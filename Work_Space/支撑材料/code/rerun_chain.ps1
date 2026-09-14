# Q4 修复后全链重跑（E7b/E8b -> 主求解 -> E5 -> E1），串行后台执行
# 用法：在 code/ 目录下执行（路径自适应，不含绝对路径）
$code = $PSScriptRoot
$parent = Split-Path -Parent $PSScriptRoot
$logs = Join-Path $parent 'logs'
if (-not (Test-Path $logs)) { $logs = $parent }   # 交付副本内日志与 code/ 同级
Set-Location $code
python q4_w6_e78b.py --go *> "$logs/rerun_e78b.txt"
python q4_solver.py --go *> "$logs/rerun_solve.txt"
python q4_w6_e5.py --go *> "$logs/rerun_e5.txt"
python q4_w6_e15.py e1 *> "$logs/rerun_e1.txt"
"CHAIN DONE" | Out-File "$logs/rerun_chain_done.txt" -Encoding utf8
