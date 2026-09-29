@echo off
setlocal
where ollama >nul 2>nul
if errorlevel 1 (
  echo Ollama was not found.
  echo 1. Install Ollama from https://ollama.com/download/windows
  echo 2. Close and reopen this window, then run this setup again.
  pause
  exit /b 1
)
echo Downloading the default local coding model qwen2.5-coder:1.5b.
echo This is about 1 GB and requires an internet connection once.
ollama pull qwen2.5-coder:1.5b
if errorlevel 1 (
  echo Model download failed. Check your internet connection and try again.
  pause
  exit /b 1
)
echo Model is ready. Double-click run_windows.bat to start ContentCraft.
pause
endlocal
