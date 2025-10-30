@echo off

if not exist ".venv" (
    echo Creating new virtual environment...
    uv venv --python 3.11.9
    echo Installing backend dependencies for the first time...
    echo Installing/Updating backend packages...
    uv pip install --python .venv .
    uv pip install --python .venv .[dev]
) else (
    echo Virtual environment already exists, removing and recreating to avoid corruption...
    rmdir /s /q .venv
    echo Creating new virtual environment...
    uv venv --python 3.11.9
    echo Installing backend dependencies...
    echo Installing/Updating backend packages...
    uv pip install --python .venv .
    uv pip install --python .venv .[dev]
)

echo Checking environment file...
if not exist ".vscode" mkdir .vscode

echo Creating .vscode\settings.json...
(
echo {
echo     "python.defaultInterpreterPath": "./.venv/Scripts/python.exe",
echo     "python.terminal.activateEnvironment": true,
echo     "python.analysis.extraPaths": [
echo         "${workspaceFolder}"
echo     ],
echo     "python.envFile": "${workspaceFolder}/.env"
echo }
) > .vscode\settings.json

echo Checking environment file...
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo ✅ .env file created - please edit if needed
) else (
    echo ✅ .env file already exists
)

echo.
echo Setup complete!
echo ✅ VS Code settings configured automatically
echo ✅ Virtual environment ready
echo ✅ SQLite Cloud dependency installed
