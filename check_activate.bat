@echo off
echo Checking Python environment...

REM Check if virtual environment is activated
if defined VIRTUAL_ENV (
    echo ✅ Virtual environment is active
    echo Location: %VIRTUAL_ENV%
    
    REM Display Python version
    python --version
    
    REM Display pip version
    pip --version
    
    echo.
    echo Required packages:
    pip freeze | findstr "asyncua"
    pip freeze | findstr "pandas"
) else (
    echo ❌ Virtual environment is NOT active
    echo.
    echo To activate, run:
    echo .\venv\Scripts\activate
)

pause