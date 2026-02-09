@echo off
REM Start React Frontend Development Server
echo.
echo ╔════════════════════════════════════════════════╗
echo ║  Starting React Frontend...                    ║
echo ╚════════════════════════════════════════════════╝
echo.

cd %~dp0..
cd react_frontend

if not exist "node_modules" (
    echo Installing npm packages...
    call npm install -q
)

echo ✅ Starting development server on http://localhost:3002
echo Press Ctrl+C to stop
echo.

call npm start -- --port 3002 --host 127.0.0.1
