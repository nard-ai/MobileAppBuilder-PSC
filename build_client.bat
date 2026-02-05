@echo off
REM Build Lightweight Client for POS Computers
setlocal enabledelayedexpansion

echo.
echo 📱 Mobile App Builder - Client Builder
echo =====================================

REM Check Python
python --version >nul 2>&1
if !ERRORLEVEL! neq 0 (
    echo ❌ Python not found. Please install Python 3.7+ first.
    pause
    exit /b 1
)
echo ✅ Python is available

REM Check if client source exists
if not exist "client_lightweight.py" (
    echo ❌ client_lightweight.py not found!
    pause
    exit /b 1
)

:menu
echo.
echo 🔧 Client Build Options:
echo.
echo 1. 🏗️  Build Portable Executable (Recommended)
echo 2. 📦 Build with Icon and Metadata
echo 3. 🧪 Test Client Locally
echo 4. 📋 Install Client Dependencies
echo 5. 🧹 Clean Build Files
echo 0. 🚪 Exit
echo.
set /p choice="Enter choice (0-5): "

if "%choice%"=="1" goto build_exe
if "%choice%"=="2" goto build_advanced
if "%choice%"=="3" goto test_client
if "%choice%"=="4" goto install_deps
if "%choice%"=="5" goto clean
if "%choice%"=="0" goto exit
echo Invalid choice!
goto menu

:install_deps
echo.
echo 📦 Installing Client Dependencies...
echo ==================================
echo Installing PyInstaller...
pip install pyinstaller

echo Installing client requirements...
pip install requests websocket-client tkinter

echo ✅ Dependencies installed!
pause
goto menu

:build_exe
echo.
echo 🏗️  Building Portable Executable...
echo =================================

echo Installing/updating PyInstaller...
pip install --upgrade pyinstaller

echo.
echo 🔨 Building executable...
pyinstaller --onefile --windowed --name="MobileAppBuilder" --distpath="dist" --workpath="build_temp" client_lightweight.py

if !ERRORLEVEL! equ 0 (
    echo.
    echo ✅ Build successful!
    echo.
    echo 📁 Built files location:
    echo   Executable: .\dist\MobileAppBuilder.exe
    echo   Size: 
    if exist "dist\MobileAppBuilder.exe" (
        for %%I in ("dist\MobileAppBuilder.exe") do echo     %%~zI bytes
    )
    echo.
    echo 🎯 Distribution Instructions:
    echo   1. Copy MobileAppBuilder.exe to POS computers
    echo   2. No installation required - just double-click to run
    echo   3. Configure server URL in the client settings
    echo.
    set /p open="Open dist folder? (y/N): "
    if /i "!open!"=="y" (
        explorer dist
    )
) else (
    echo ❌ Build failed! Check the output above for errors.
)

pause
goto menu

:build_advanced
echo.
echo 📦 Building Advanced Executable with Icon...
echo ===========================================

REM Check for icon file
if not exist "assets\pscLogo.png" (
    echo ⚠️  Icon file not found at assets\pscLogo.png
    echo Building without custom icon...
    set icon_param=
) else (
    echo ✅ Using custom icon from assets\pscLogo.png
    set icon_param=--icon="assets\pscLogo.png"
)

echo.
echo 🔨 Building advanced executable...
pyinstaller --onefile --windowed --name="MobileAppBuilder-POS" !icon_param! --distpath="dist" --workpath="build_temp" --add-data="client_config.json;." client_lightweight.py

if !ERRORLEVEL! equ 0 (
    echo.
    echo ✅ Advanced build successful!
    echo.
    echo 📁 Built files location:
    echo   Executable: .\dist\MobileAppBuilder-POS.exe
    echo.
) else (
    echo ❌ Advanced build failed!
)

pause
goto menu

:test_client
echo.
echo 🧪 Testing Client Locally...
echo ===========================
echo.
echo Make sure your server is running first!
echo.
set /p confirm="Server running? Continue with test? (y/N): "
if /i not "%confirm%"=="y" (
    goto menu
)

echo.
echo 🚀 Starting client in test mode...
python client_lightweight.py

goto menu

:clean
echo.
echo 🧹 Cleaning Build Files...
echo =========================

echo Removing build directories...
if exist "build_temp\" (
    rmdir /s /q "build_temp"
    echo ✅ Removed build_temp\
)
if exist "dist\" (
    rmdir /s /q "dist"
    echo ✅ Removed dist\
)
if exist "*.spec" (
    del /q "*.spec"
    echo ✅ Removed spec files
)

echo ✅ Clean complete!
pause
goto menu

:exit
echo.
echo 📋 Summary:
echo ==========
if exist "dist\MobileAppBuilder.exe" (
    echo ✅ Portable client ready at: .\dist\MobileAppBuilder.exe
    echo 📤 Ready for distribution to POS computers
) else (
    echo ⚠️  No executable found. Run option 1 to build.
)
echo.
echo 🎯 Next Steps:
echo   1. Test the executable on your computer first
echo   2. Copy to POS computers via USB, network, or email
echo   3. Provide POS staff with your server URL
echo   4. Staff just double-click MobileAppBuilder.exe to run
echo.
echo 👋 Goodbye!
exit /b 0