@echo off
REM Script simplificado para subir a GitHub (sin parámetros)
REM Uso: push-to-github.bat

setlocal enabledelayedexpansion

cls
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║         SUBIR PROYECTO A GITHUB - ASISTENTE SEGURO           ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM 1. Verificar git
echo [1/5] Verificando git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Git no está instalado
    echo   Descárgalo de: https://git-scm.com/download/win
    pause
    exit /b 1
)
echo ✓ Git encontrado

REM 2. Crear .env si no existe
echo.
echo [2/5] Verificando archivo .env...
if not exist ".env" (
    echo ⚠ .env no existe
    if exist ".env.example" (
        echo   Creando desde .env.example...
        copy ".env.example" ".env" >nul
        echo ✓ .env creado
        echo.
        echo   ⚠️  IMPORTANTE: Edita .env con tus credenciales reales
        echo   Abre el archivo .env y actualiza:
        echo   - DATABASE_URL
        echo   - SECRET_KEY
        echo.
        echo Presiona Enter cuando hayas editado .env...
        pause >nul
    )
)

REM 3. Verificar seguridad
echo.
echo [3/5] Verificando seguridad...
git ls-files | findstr /r "\.env$" >nul 2>&1
if not errorlevel 1 (
    echo ✗ .env está tracked en git (RIESGO)
    echo   Ejecuta: git rm --cached .env
    pause
    exit /b 1
)
echo ✓ .env no está en git

REM 4. Obtener información
echo.
echo [4/5] Información de GitHub...
set /p GitHubUsername="Ingresa tu usuario de GitHub: "
set /p RepoName="Nombre del repositorio (defecto: gemini-api): "
if "!RepoName!"=="" set RepoName=gemini-api

echo ✓ Usuario: %GitHubUsername%
echo ✓ Repositorio: %RepoName%
echo.

REM 5. Inicializar git si es necesario
if exist ".git" (
    echo ⚠ Git ya está inicializado
    set /p reinit="¿Reinicializar? (s/n): "
    if /i "!reinit!"=="s" (
        rmdir /s /q ".git" >nul
        git init >nul
        echo ✓ Git reinicializado
    )
) else (
    git init >nul
    echo ✓ Git inicializado
)

REM Configurar usuario
for /f "delims=" %%i in ('git config user.name') do set GitName=%%i
if "!GitName!"=="" (
    set /p GitName="Ingresa tu nombre completo: "
    git config user.name "!GitName!"
)

for /f "delims=" %%i in ('git config user.email') do set GitEmail=%%i
if "!GitEmail!"=="" (
    set /p GitEmail="Ingresa tu correo de GitHub: "
    git config user.email "!GitEmail!"
)

echo ✓ Usuario: !GitName! ^<!GitEmail!^>

REM 6. Mostrar lo que se committeará
echo.
echo [5/5] Archivos a commitear:
git status --short

REM 7. Confirmar
echo.
set /p confirm="¿Continuar? (s/n): "
if /i not "!confirm!"=="s" (
    echo Cancelado
    exit /b 0
)

REM 8. Agregar archivos
echo.
echo Agregando archivos...
git add . >nul
echo ✓ Archivos agregados

REM 9. Crear commit
echo Creando commit...
git commit -m "Initial commit: FastAPI authentication with Docker support" >nul
echo ✓ Commit creado

REM 10. Configurar rama y remote
echo Configurando git...
git branch -M main >nul
echo ✓ Rama configurada como 'main'

set "RepoURL=https://github.com/!GitHubUsername!/!RepoName!.git"
git remote add origin "!RepoURL!" >nul 2>&1
if errorlevel 1 (
    git remote set-url origin "!RepoURL!" >nul
)
echo ✓ Remote agregado: !RepoURL!

REM 11. Resumen
cls
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                    ✓ LISTO PARA GITHUB                        ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo PRÓXIMOS PASOS:
echo.
echo 1. Crea un repositorio vacío en GitHub:
echo    → https://github.com/new
echo    → Nombre: %RepoName%
echo    → NO inicialices con README
echo    → Crea el repositorio
echo.
echo 2. Luego pushea (ejecuta en PowerShell o CMD):
echo    git push -u origin main
echo.
echo 3. Si pide autenticación:
echo    - HTTPS: usa un token personal de GitHub
echo    - SSH: asegúrate de tener una SSH key agregada
echo.
echo 4. Verifica tu repositorio en:
echo    https://github.com/%GitHubUsername%/%RepoName%
echo.
echo ¿Deseas pushear ahora? (s/n)
set /p pushNow="Opción: "

if /i "!pushNow!"=="s" (
    echo.
    echo Pusheando a GitHub...
    git push -u origin main
    if errorlevel 0 (
        echo.
        echo ✓ ¡Repositorio subido exitosamente!
        echo.
        echo Tu proyecto está en: https://github.com/%GitHubUsername%/%RepoName%
    )
) else (
    echo.
    echo Puedes pushear después con:
    echo   git push -u origin main
)

echo.
pause
