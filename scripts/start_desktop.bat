@echo off
REM Start PyQt5 Desktop Application
echo Starting Chemical Visualizer Desktop App...
cd %~dp0..
cd chemical_visualizer
call ..\.venv\Scripts\activate.bat
python desktop_app.py
