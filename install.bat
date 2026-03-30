@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "TASK_NAME=wallChange"
set "PYTHON=python"

if "%1"=="uninstall" goto uninstall

:: Install — create a Windows Task Scheduler task that runs at logon
echo Installing wallChange...

schtasks /create /tn "%TASK_NAME%" /tr "\"%PYTHON%\" \"%SCRIPT_DIR%wallchange.py\"" /sc onlogon /rl limited /f
if %errorlevel% neq 0 (
    echo Failed to create scheduled task.
    echo Try running this script as administrator.
    exit /b 1
)

:: Also start it now
echo Starting wallChange...
schtasks /run /tn "%TASK_NAME%"

echo.
echo wallChange installed and started.
echo It will auto-start after every logon.
goto end

:uninstall
echo Uninstalling wallChange...

:: Stop the running task
taskkill /f /fi "WINDOWTITLE eq wallChange*" >nul 2>&1
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1

echo wallChange removed.

:end
endlocal
