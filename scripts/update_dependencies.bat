@echo off
REM Update all dependencies to latest versions
echo Updating Chemical Visualizer Dependencies...
echo ============================================
echo.

cd %~dp0..

REM Update Backend
echo [1/3] Updating Backend Dependencies...
cd chemical_visualizer
call ..\.venv\Scripts\activate.bat
pip install --upgrade -r requirements.txt
pip install --upgrade -r desktop_requirements.txt
cd ..
echo Backend updated!
echo.

REM Update Frontend
echo [2/3] Updating Frontend Dependencies...
cd react_frontend
call npm update
cd ..
echo Frontend updated!
echo.

REM Show versions
echo [3/3] Installed Versions:
echo.
echo Python Packages:
call .venv\Scripts\activate.bat
pip list | findstr "Django djangorestframework pandas PyQt5"
echo.
echo Node Packages:
cd react_frontend
call npm list react axios chart.js --depth=0
cd ..
echo.
echo Update complete!
pause
