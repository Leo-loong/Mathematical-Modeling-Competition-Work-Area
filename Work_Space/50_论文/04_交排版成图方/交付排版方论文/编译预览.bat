@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================================
echo   保存即编译预览（相当于 Word 的实时预览）
echo   关闭本窗口即停止
echo ============================================================
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0编译预览.ps1"
pause
