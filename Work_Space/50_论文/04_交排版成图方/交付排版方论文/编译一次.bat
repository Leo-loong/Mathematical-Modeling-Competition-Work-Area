@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================================
echo   编译一次（相当于 Word 的"另存为 PDF"），约 1-2 分钟
echo ============================================================
xelatex -interaction=nonstopmode -synctex=1 main.tex >nul
xelatex -interaction=nonstopmode -synctex=1 main.tex >nul
echo.
echo ---- 编译结果 ----
findstr /C:"Output written" /C:"Missing character" /C:"Overfull \hbox" main.log
echo.
echo 自检要点：正文 = 30 页（红线 小于等于 30）；Overfull 0 处；Missing character 0 处
echo 若提示无法写入 main.pdf：关掉正在看它的阅读器（WPS/Acrobat 会锁文件）
pause
