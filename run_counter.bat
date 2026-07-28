@echo off
setlocal EnableExtensions

cd /d "%~dp0"

where py >nul 2>&1
if %errorlevel%==0 (
    set "PYTHON_LAUNCHER=py"
) else (
    where python >nul 2>&1
    if %errorlevel%==0 (
        set "PYTHON_LAUNCHER=python"
    ) else (
        echo Python was not found. Downloading and installing Python...
        set "PYTHON_INSTALLER=%TEMP%\python-installer.exe"
        powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.5/python-3.12.5-amd64.exe' -OutFile '%PYTHON_INSTALLER%'"
        if errorlevel 1 (
            echo Failed to download Python installer.
            pause
            exit /b 1
        )

        "%PYTHON_INSTALLER%" /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1
        if errorlevel 1 (
            echo Python installation failed.
            pause
            exit /b 1
        )

        set "PYTHON_LAUNCHER=python"
    )
)

%PYTHON_LAUNCHER% -m pip --version >nul 2>&1
if errorlevel 1 (
    echo pip was not found. Bootstrapping pip...
    %PYTHON_LAUNCHER% -m ensurepip --upgrade
    if errorlevel 1 (
        echo Failed to bootstrap pip.
        pause
        exit /b 1
    )
)

if exist requirements.txt (
    echo Installing requirements...
    %PYTHON_LAUNCHER% -m pip install --upgrade pip
    %PYTHON_LAUNCHER% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install requirements.
        pause
        exit /b 1
    )
)

echo Starting app...
%PYTHON_LAUNCHER% testDM.py
pause
