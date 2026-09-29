@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 server.py
  goto :end
)
where python >nul 2>nul
if %errorlevel%==0 (
  python server.py
  goto :end
)
echo Python 3 was not found. Install it from https://www.python.org/downloads/windows/
echo During installation, enable "Add python.exe to PATH".
pause
:end
endlocal
