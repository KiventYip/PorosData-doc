@echo off
echo =========================================
echo   PorosData Documentation Server
echo   Enhanced Responsive Layout
echo =========================================
echo.
echo Server will start on: http://localhost:8080
echo.
echo Layout Features:
echo - Responsive design for all screen sizes
echo - Centered content with optimal width usage
echo - Mobile-friendly navigation
echo - Improved readability on wide screens
echo.
cd "docs_sphinx\_build\html"
python -m http.server 8080 --bind 127.0.0.1
pause