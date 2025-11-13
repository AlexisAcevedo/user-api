# Script PowerShell para iniciar la API y el Frontend
# Ejecutar: .\start-all.ps1
# Nota: Puede necesitar ejecutar: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Clear-Host

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     🚀 Sistema de Autenticación - Inicio Rápido              ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Iniciando servicios..." -ForegroundColor Yellow
Write-Host ""

# Iniciar API en una nueva ventana PowerShell
Write-Host "[1/2] Iniciando API en http://127.0.0.1:8000 ..." -ForegroundColor Green
$apiProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ScriptDir'; uvicorn main:app --reload" `
    -WindowStyle Normal `
    -PassThru

# Esperar a que la API se inicie
Start-Sleep -Seconds 3

# Iniciar Frontend en otra ventana PowerShell
Write-Host "[2/2] Iniciando Frontend en http://127.0.0.1:8001 ..." -ForegroundColor Green
$frontendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ScriptDir'; python serve_frontend.py" `
    -WindowStyle Normal `
    -PassThru

# Mensaje final
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║          ✓ Servicios iniciados correctamente                ║" -ForegroundColor Cyan
Write-Host "╠════════════════════════════════════════════════════════════════╣" -ForegroundColor Cyan
Write-Host "║                                                                ║" -ForegroundColor Cyan
Write-Host "║  🔵 API       → http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "║  🟢 API Docs  → http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host "║  🟠 Frontend  → http://127.0.0.1:8001" -ForegroundColor Cyan
Write-Host "║                                                                ║" -ForegroundColor Cyan
Write-Host "║  ⚠️  Presiona Ctrl+C en esta ventana para detener todos    ║" -ForegroundColor Yellow
Write-Host "║                                                                ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Esperar a que el usuario presione Ctrl+C
try {
    [System.Console]::ReadKey($true)
} catch {
    # Si ocurre un error, ignorarlo
}

# Limpiar procesos si el usuario los cierra manualmente
Write-Host ""
Write-Host "🛑 Deteniendo servicios..." -ForegroundColor Red

if ($apiProcess -and -not $apiProcess.HasExited) {
    Stop-Process -InputObject $apiProcess -Force -ErrorAction SilentlyContinue
}

if ($frontendProcess -and -not $frontendProcess.HasExited) {
    Stop-Process -InputObject $frontendProcess -Force -ErrorAction SilentlyContinue
}

Write-Host "✓ Servicios detenidos" -ForegroundColor Green
Write-Host ""
