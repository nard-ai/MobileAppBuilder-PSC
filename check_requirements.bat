@echo off
REM Beginner's System Check Script
echo.
echo 🎓 Beginner's Guide: System Requirements Check
echo =============================================

echo.
echo 📋 Checking your computer setup...
echo.

REM Check Docker Desktop
echo 1. Checking Docker Desktop...
docker --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo    ✅ Docker is installed
    docker info >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        echo    ✅ Docker is running
    ) else (
        echo    ❌ Docker is installed but not running
        echo    👉 Please start Docker Desktop from your Start menu
    )
) else (
    echo    ❌ Docker Desktop not found
    echo    👉 Download from: https://www.docker.com/products/docker-desktop
    echo    👉 Install it, then restart this check
)

echo.
echo 2. Checking Python...
python --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo    ✅ Python is installed
    python --version
) else (
    echo    ❌ Python not found
    echo    👉 Download from: https://www.python.org/downloads/
    echo    👉 Make sure to check "Add Python to PATH" during installation
)

echo.
echo 3. Checking Node.js...
node --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo    ✅ Node.js is installed
    node --version
) else (
    echo    ⚠️  Node.js not found (optional for your computer)
    echo    👉 This is OK - Docker container will handle Node.js
)

echo.
echo 4. Checking your project folder...
if exist "server_api.py" (
    echo    ✅ Project files found
) else (
    echo    ❌ Project files not found
    echo    👉 Make sure you're in the correct folder
    echo    👉 You should see files like server_api.py and docker-compose.yml
)

echo.
echo 5. Checking EXPO_TOKEN...
if "%EXPO_TOKEN%"=="" (
    echo    ⚠️  EXPO_TOKEN not set (required for building apps)
    echo    👉 We'll help you set this up in the next steps
) else (
    echo    ✅ EXPO_TOKEN is set
)

echo.
echo 📋 Summary:
echo ===========
echo If you see any ❌ red marks above, please fix those first.
echo If you see only ✅ green marks, you're ready to continue!
echo.
pause