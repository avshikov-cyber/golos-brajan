@echo off
chcp 65001 >nul
cd /d "%~dp0"
python GOLOS_CHROM_WITH_BRAIN.py
pause