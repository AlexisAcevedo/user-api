@echo off
REM Script para iniciar la API y el Frontend en Windows
REM Abre dos ventanas de terminal: una para la API y otra para el Frontend

cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║     Sistema de Autenticacion - Inicio Rapido              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Iniciando servicios...
echo.

REM Obtener el directorio actual
setlocal enabledelayedexpansion
set "SCRIPT_DIR=%~dp0"

REM Iniciar API en una nueva ventana
echo [1/2] Iniciando API en http://127.0.0.1:8000 ...
start "API - FastAPI" cmd /k "cd /d "%SCRIPT_DIR%" && uvicorn main:app --reload"

REM Esperar un poco para que la API se inicie
timeout /t 3 /nobreak

REM Iniciar Frontend en otra ventana
echo [2/2] Iniciando Frontend en http://127.0.0.1:8001 ...
start "Frontend - Web Server" cmd /k "cd /d "%SCRIPT_DIR%" && python serve_frontend.py"

REM Mensaje final
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              Servicios iniciados correctamente             ║
echo ╠══════════════════════════════════════════════════════════════╣
echo ║                                                              ║
echo ║  🔵 API       → http://127.0.0.1:8000                     ║
echo ║  🟢 API Docs  → http://127.0.0.1:8000/docs              ║
echo ║  🟠 Frontend  → http://127.0.0.1:8001                     ║
echo ║                                                              ║
echo ║  Nota: Cierra ambas ventanas para detener los servicios   ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

pause
