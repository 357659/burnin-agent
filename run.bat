@echo off

cd /d "%~dp0"

echo ==========================================
echo          BURN-IN AGENT
echo ==========================================
echo.

python -m streamlit run frontend/app.py

pause