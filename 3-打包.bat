@echo off
REM 切换到当前工作目录
cd /d %~dp0

REM 使用 .conda 目录中的 Python 解释器执行 zip.py 脚本
.\conda\python.exe .\py\zip.py

pause