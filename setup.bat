@echo off

if not exist ".venv" (
    echo Creating new virtual environment...
    uv venv --python 3.11.9
    echo Installing dependencies for the first time...
) else (
    echo Virtual environment already exists, checking for updates...
)

echo Activating venv...
call .venv\Scripts\activate

echo Installing/Updating packages...
uv pip install .
uv pip install .[dev]
pip install -e .

echo Checking database file...
if not exist "data\czsu_data.db" (
    echo WARNING: Database file not found at data\czsu_data.db
    echo Please copy the database file from the main project:
    echo   copy ..\data\czsu_data.db .\data\
) else (
    echo ✅ Database file found
)

echo Setting up VS Code workspace...
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
echo.
echo To run the server:
echo   python main.py
echo.
pause