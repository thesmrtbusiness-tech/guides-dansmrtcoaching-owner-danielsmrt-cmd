@echo off
rem Run this once. It puts a "Finals" shortcut on the desktop.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0make-shortcut.ps1"
if errorlevel 1 (echo Could not create the shortcut. & pause & exit /b 1)
echo Done. Double-click "Finals" on your desktop to start.
pause
