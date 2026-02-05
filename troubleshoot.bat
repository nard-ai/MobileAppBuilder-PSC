@echo off
REM Beginner's Troubleshooting Script
setlocal enabledelayedexpansion

echo.
echo 🔍 Troubleshooting Helper
echo ========================

:menu
echo.
echo What problem are you having?
echo.
echo 1. 🐳 Docker problems
echo 2. 🌐 Server not starting  
echo 3. 🔗 Client can't connect
echo 4. 🏗️  Build failures
echo 5. 💾 EXPO_TOKEN issues
echo 6. 📱 Client won't run
echo 7. ✅ Test everything
echo 0. Exit
echo.
set /p choice="Enter choice (0-7): "

if "%choice%"=="1" goto docker_help
if "%choice%"=="2" goto server_help  
if "%choice%"=="3" goto client_help
if "%choice%"=="4" goto build_help
if "%choice%"=="5" goto token_help
if "%choice%"=="6" goto app_help
if "%choice%"=="7" goto test_all
if "%choice%"=="0" goto exit
echo Invalid choice!
goto menu

:docker_help
echo.
echo 🐳 Docker Troubleshooting
echo =========================
echo.
echo Checking Docker status...
docker --version >nul 2>&1
if !ERRORLEVEL! equ 0 (
    echo ✅ Docker is installed
    docker info >nul 2>&1
    if !ERRORLEVEL! equ 0 (
        echo ✅ Docker is running
        echo.
        echo Your Docker seems fine. Try running your server setup again.
    ) else (
        echo ❌ Docker not running
        echo.
        echo 🔧 Fix this by:
        echo   1. Open Docker Desktop from Start menu
        echo   2. Wait for it to fully start (whale icon stops animating)
        echo   3. Try again
    )
) else (
    echo ❌ Docker not installed
    echo.
    echo 🔧 Fix this by:
    echo   1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop
    echo   2. Install it
    echo   3. Restart your computer
    echo   4. Start Docker Desktop
)
pause
goto menu

:server_help
echo.
echo 🌐 Server Troubleshooting  
echo =========================
echo.
echo Testing server connection...
curl -s http://localhost:3000/api/status >nul 2>&1
if !ERRORLEVEL! equ 0 (
    echo ✅ Server is running and responding
    echo.
    echo Your server is working fine!
) else (
    echo ❌ Server not responding
    echo.
    echo 🔧 Try these fixes:
    echo   1. Run server_setup.bat and choose option 1
    echo   2. Check if Docker Desktop is running
    echo   3. Check if port 3000 is free
    echo.
    echo Checking Docker containers...
    docker ps | findstr mobile-app-builder
    if !ERRORLEVEL! equ 0 (
        echo ✅ Container is running
    ) else (
        echo ❌ Container not running
        echo Try: server_setup.bat → option 1
    )
)
pause
goto menu

:client_help
echo.
echo 🔗 Client Connection Troubleshooting
echo ===================================
echo.
echo 1. Testing local server connection...
curl -s http://localhost:3000/api/status >nul 2>&1
if !ERRORLEVEL! equ 0 (
    echo ✅ Local server OK
) else (
    echo ❌ Local server not responding
    echo   → Start your server first: server_setup.bat → option 1
)

echo.
echo 2. Check if client config exists...
if exist "client_config.json" (
    echo ✅ Client config found
    echo Configuration:
    type client_config.json
) else (
    echo ❌ Client config missing
    echo   → Run the client once to create default config
)

echo.
echo 3. If using ngrok, make sure:
echo   - ngrok window is still open
echo   - URL starts with https://
echo   - Test URL in browser first
echo.
pause
goto menu

:build_help
echo.
echo 🏗️ Build Troubleshooting
echo =======================
echo.
echo 1. Checking EXPO_TOKEN...
if "%EXPO_TOKEN%"=="" (
    echo ❌ EXPO_TOKEN not set
    echo.
    echo 🔧 Fix this by:
    echo   1. Get token from: https://expo.dev/accounts/settings/access-tokens
    echo   2. Set it: setx EXPO_TOKEN "your_token_here"
    echo   3. Restart command prompt
) else (
    echo ✅ EXPO_TOKEN is set
    echo Token: %EXPO_TOKEN:~0,20%... (truncated for security)
)

echo.
echo 2. Testing EAS CLI access...
docker exec mobile-app-builder-server eas whoami 2>nul
if !ERRORLEVEL! equ 0 (
    echo ✅ EAS authentication working
) else (
    echo ❌ EAS authentication failed
    echo   → Check your EXPO_TOKEN is valid
)

echo.
echo 3. Common build failures:
echo   - Invalid EXPO_TOKEN → Get new token from Expo
echo   - Network issues → Check internet connection  
echo   - App.json errors → Check app configuration
echo.
pause
goto menu

:token_help
echo.
echo 💾 EXPO_TOKEN Setup Help
echo =======================
echo.
echo Current status:
if "%EXPO_TOKEN%"=="" (
    echo ❌ EXPO_TOKEN not set
) else (
    echo ✅ EXPO_TOKEN is set: %EXPO_TOKEN:~0,20%...
)

echo.
echo 🔧 How to set EXPO_TOKEN:
echo.
echo Method 1 (Quick):
echo   1. Open Command Prompt
echo   2. Type: setx EXPO_TOKEN "your_token_here"  
echo   3. Close and reopen Command Prompt
echo.
echo Method 2 (Permanent):
echo   1. Press Win+R, type: sysdm.cpl
echo   2. Advanced tab → Environment Variables
echo   3. New user variable: EXPO_TOKEN
echo   4. Value: your token
echo.
echo Get your token from:
echo https://expo.dev/accounts/settings/access-tokens
echo.
pause
goto menu

:app_help
echo.
echo 📱 Client App Troubleshooting
echo ============================
echo.
echo 1. Checking if executable exists...
if exist "dist\MobileAppBuilder.exe" (
    echo ✅ Client executable found
    for %%I in ("dist\MobileAppBuilder.exe") do echo    Size: %%~zI bytes
) else (
    echo ❌ Client executable not found
    echo   → Run: build_client.bat → option 1
)

echo.
echo 2. Testing Python (needed for building client)...
python --version >nul 2>&1
if !ERRORLEVEL! equ 0 (
    echo ✅ Python available
    python --version
) else (
    echo ❌ Python not found
    echo   → Install from: https://www.python.org/downloads/
    echo   → Make sure to check "Add Python to PATH"
)

echo.
echo 3. If client crashes on startup:
echo   - Run in Command Prompt: python client_lightweight.py
echo   - Check error messages
echo   - Antivirus might be blocking it
echo.
pause
goto menu

:test_all
echo.
echo ✅ Complete System Test
echo ======================
echo.
echo Running comprehensive tests...
echo.

echo 1. Docker check...
docker info >nul 2>&1
if !ERRORLEVEL! equ 0 (
    echo    ✅ Docker running
) else (
    echo    ❌ Docker not running
)

echo 2. Server check...
curl -s http://localhost:3000/api/status >nul 2>&1  
if !ERRORLEVEL! equ 0 (
    echo    ✅ Server responding
) else (
    echo    ❌ Server not responding
)

echo 3. EXPO_TOKEN check...
if "%EXPO_TOKEN%"=="" (
    echo    ❌ EXPO_TOKEN not set
) else (
    echo    ✅ EXPO_TOKEN set
)

echo 4. Client executable check...
if exist "dist\MobileAppBuilder.exe" (
    echo    ✅ Client built
) else (
    echo    ❌ Client not built
)

echo 5. Python check...
python --version >nul 2>&1
if !ERRORLEVEL! equ 0 (
    echo    ✅ Python available
) else (
    echo    ❌ Python not found
)

echo.
echo Test complete! Fix any ❌ items above.
pause
goto menu

:exit
echo.
echo 💡 Remember:
echo   - Check requirements first: check_requirements.bat
echo   - Read the beginner guide: BEGINNER_GUIDE.md  
echo   - Server must be running before testing client
echo   - Keep ngrok window open for external access
echo.
echo 👋 Good luck with your setup!
exit /b 0