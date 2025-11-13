# Script para instalar Docker Desktop en Windows
# Ejecutar como Administrador: Click derecho -> "Ejecutar con PowerShell como administrador"

Write-Host "=== Instalación de Docker Desktop ===" -ForegroundColor Cyan
Write-Host ""

# Verificar si ya está instalado Docker
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "Docker ya está instalado!" -ForegroundColor Green
    docker --version
    exit 0
}

# Paso 1: Instalar WSL2
Write-Host "Paso 1: Instalando WSL2..." -ForegroundColor Yellow
try {
    wsl --install
    Write-Host "WSL2 instalado. Por favor, reinicia tu computadora y luego ejecuta este script nuevamente." -ForegroundColor Yellow
    Write-Host "Después del reinicio, ejecuta: winget install Docker.DockerDesktop" -ForegroundColor Yellow
    exit 0
} catch {
    Write-Host "Error al instalar WSL2. Intentando método alternativo..." -ForegroundColor Red
    
    # Método alternativo usando dism
    dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
    dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
    
    Write-Host "Características habilitadas. Por favor, reinicia tu computadora." -ForegroundColor Yellow
    Write-Host "Después del reinicio, ejecuta: wsl --set-default-version 2" -ForegroundColor Yellow
    Write-Host "Y luego: winget install Docker.DockerDesktop" -ForegroundColor Yellow
    exit 0
}

# Paso 2: Instalar Docker Desktop (solo si WSL2 ya está instalado)
Write-Host ""
Write-Host "Paso 2: Instalando Docker Desktop..." -ForegroundColor Yellow
try {
    winget install Docker.DockerDesktop --accept-package-agreements --accept-source-agreements
    Write-Host "Docker Desktop instalado correctamente!" -ForegroundColor Green
    Write-Host "Por favor, inicia Docker Desktop desde el menú de inicio." -ForegroundColor Yellow
} catch {
    Write-Host "Error al instalar Docker Desktop. Intenta instalarlo manualmente desde:" -ForegroundColor Red
    Write-Host "https://www.docker.com/products/docker-desktop/" -ForegroundColor Cyan
}

