@echo off
REM Central Server Setup and Management Script
setlocal enabledelayedexpansion

echo.
echo 🏭 Mobile App Builder - Central Server Setup
echo ============================================

REM Check Docker
docker info >nul 2>&1
if !ERRORLEVEL! neq 0 (
    echo ❌ Docker not running. Please start Docker Desktop first.
    echo.
    echo 📋 To install Docker Desktop:
    echo   1. Download from: https://www.docker.com/products/docker-desktop
    echo   2. Install and start Docker Desktop
    echo   3. Run this script again
    pause
    exit /b 1
)
echo ✅ Docker is running

REM Check for EXPO_TOKEN
if "%EXPO_TOKEN%"=="" (
    echo.
    echo ⚠️  EXPO_TOKEN environment variable not set
    echo.
    echo 📋 To set up EXPO_TOKEN:
    echo   1. Visit: https://expo.dev/accounts/[your-account]/settings/access-tokens
    echo   2. Create a new token
    echo   3. Set environment variable: set EXPO_TOKEN=your_token_here
    echo   4. Run this script again
    echo.
    set /p continue="Do you want to continue without EXPO_TOKEN? (y/N): "
    if /i not "!continue!"=="y" (
        exit /b 1
    )
)

:menu
echo.
echo 🔧 Central Server Management:
echo.
echo 1. 🚀 Start Server (First Time Setup)
echo 2. ▶️  Start Server (Existing)
echo 3. ⏹️  Stop Server
echo 4. 🔄 Restart Server
echo 5. 📊 View Server Status
echo 6. 📜 View Server Logs
echo 7. 🌐 Setup ngrok Tunnel
echo 8. 🧹 Clean Up (Remove containers and images)
echo 0. 🚪 Exit
echo.
set /p choice="Enter choice (0-8): "

if "%choice%"=="1" goto first_start
if "%choice%"=="2" goto start
if "%choice%"=="3" goto stop
if "%choice%"=="4" goto restart
if "%choice%"=="5" goto status
if "%choice%"=="6" goto logs
if "%choice%"=="7" goto ngrok
if "%choice%"=="8" goto cleanup
if "%choice%"=="0" goto exit
echo Invalid choice!
goto menu

:first_start
echo.
echo 🚀 Setting up Central Server (First Time)...
echo ==========================================
echo.
echo 📦 Building Docker image...
docker-compose build mobile-app-builder-server
if !ERRORLEVEL! neq 0 (
    echo ❌ Docker build failed!
    pause
    goto menu
)

echo.
echo ▶️  Starting server...
docker-compose up -d mobile-app-builder-server
if !ERRORLEVEL! neq 0 (
    echo ❌ Failed to start server!
    pause
    goto menu
)

echo.
echo ✅ Server started successfully!
echo.
echo 🌐 Server is running on:
echo   Local:    http://localhost:3000
echo   Network:  http://[your-computer-ip]:3000
echo.
echo ⏰ Waiting for server to initialize...
timeout /t 5 /nobreak >nul

call :check_health
goto menu

:start
echo.
echo ▶️  Starting Central Server...
docker-compose up -d mobile-app-builder-server
if !ERRORLEVEL! neq 0 (
    echo ❌ Failed to start server!
    pause
    goto menu
)

echo ✅ Server started!
call :check_health
goto menu

:stop
echo.
echo ⏹️  Stopping Central Server...
docker-compose stop mobile-app-builder-server
echo ✅ Server stopped!
pause
goto menu

:restart
echo.
echo 🔄 Restarting Central Server...
docker-compose restart mobile-app-builder-server
echo ✅ Server restarted!
call :check_health
goto menu

:status
echo.
echo 📊 Server Status:
echo ================
docker-compose ps mobile-app-builder-server
echo.
echo 🌐 API Health Check:
curl -s http://localhost:3000/api/status 2>nul
if !ERRORLEVEL! equ 0 (
    echo ✅ API is responding
) else (
    echo ❌ API not responding
)
echo.
pause
goto menu

:logs
echo.
echo 📜 Server Logs (Press Ctrl+C to return to menu):
echo ==============================================
docker-compose logs -f mobile-app-builder-server
goto menu

:ngrok
echo.
echo 🌐 Setting up ngrok tunnel...
echo ============================
echo.
echo 📋 Prerequisites:
echo   1. Install ngrok from https://ngrok.com/
echo   2. Sign up for free account
echo   3. Run: ngrok authtoken [your-token]
echo.
echo 🚀 Starting ngrok tunnel...
echo.
start "ngrok tunnel" ngrok http 3000
echo.
echo ✅ ngrok tunnel started in a new window
echo.
echo 📋 Instructions:
echo   1. Check the ngrok window for your public URL (https://xxxxx.ngrok.io)
echo   2. Give this URL to POS computers for the client settings
echo   3. Keep this script and ngrok running for the tunnel to work
echo.
pause
goto menu

:cleanup
echo.
echo 🧹 Cleaning up Docker resources...
echo =================================
set /p confirm="This will remove all containers and images. Continue? (y/N): "
if /i not "%confirm%"=="y" (
    goto menu
)

echo Stopping containers...
docker-compose down

echo Removing images...
docker rmi -f mobile-app-builder-server 2>nul

echo Cleaning up volumes...
docker volume prune -f

echo ✅ Cleanup complete!
pause
goto menu

:check_health
echo 🔍 Checking server health...
timeout /t 3 /nobreak >nul
curl -s http://localhost:3000/api/status >nul 2>&1
if !ERRORLEVEL! equ 0 (
    echo ✅ Server is healthy and responding
    echo.
    echo 🎯 Next Steps:
    echo   1. Set up ngrok tunnel (option 7) for external access
    echo   2. Build client executable: run build_client.bat
    echo   3. Distribute client to POS computers
    echo.
) else (
    echo ⚠️  Server may still be starting up...
    echo   Run option 6 to check logs if issues persist
    echo.
)
goto :eof

:exit
echo.
echo 👋 Goodbye!
exit /b 0