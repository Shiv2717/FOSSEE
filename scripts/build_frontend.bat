@echo off
REM Build React frontend for production
echo Building React Frontend for Production...
cd %~dp0..
cd react_frontend
echo.
echo Installing/updating dependencies...
call npm install
echo.
echo Building optimized production bundle...
call npm run build
echo.
echo Build complete! Files are in react_frontend/build/
echo.
echo To serve the production build:
echo   - Use a web server (nginx, Apache)
echo   - Or install serve: npm install -g serve
echo   - Then run: serve -s build -l 3000
echo.
pause
