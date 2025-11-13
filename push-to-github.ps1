# Script para subir el proyecto a GitHub de manera segura
# Uso: .\push-to-github.ps1 -GitHubUsername "tu_usuario" -RepoName "gemini-api"

param(
    [string]$GitHubUsername = "",
    [string]$RepoName = "gemini-api",
    [string]$CommitMessage = "Initial commit: FastAPI authentication with Docker support"
)

# Colores
$Green = [System.ConsoleColor]::Green
$Red = [System.ConsoleColor]::Red
$Yellow = [System.ConsoleColor]::Yellow
$Cyan = [System.ConsoleColor]::Cyan

function Write-Header {
    param([string]$Text)
    Write-Host "`n╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor $Cyan
    Write-Host "║ $Text" -ForegroundColor $Cyan
    Write-Host "╚═══════════════════════════════════════════════════════════════╝`n" -ForegroundColor $Cyan
}

function Write-Success {
    param([string]$Text)
    Write-Host "✓ $Text" -ForegroundColor $Green
}

function Write-Error-Custom {
    param([string]$Text)
    Write-Host "✗ $Text" -ForegroundColor $Red
}

function Write-Warning-Custom {
    param([string]$Text)
    Write-Host "⚠ $Text" -ForegroundColor $Yellow
}

# Verificar si git está instalado
Write-Header "1. VERIFICANDO REQUISITOS"

try {
    $gitVersion = git --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Git instalado: $gitVersion"
    } else {
        Write-Error-Custom "Git no está instalado"
        Write-Host "Descárgalo de: https://git-scm.com/download/win"
        exit 1
    }
} catch {
    Write-Error-Custom "Git no encontrado"
    exit 1
}

# Verificar si .env existe
if (-not (Test-Path ".env")) {
    Write-Warning-Custom ".env no encontrado"
    Write-Host "Creando desde .env.example..."
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Success ".env creado desde plantilla"
        Write-Host "`n⚠️  IMPORTANTE: Edita .env con tus credenciales reales"
        Write-Host "   - DATABASE_URL"
        Write-Host "   - SECRET_KEY"
        Write-Host "`nPresiona Enter cuando hayas editado .env..."
        Read-Host
    } else {
        Write-Error-Custom ".env.example no encontrado"
        exit 1
    }
}

# Verificar seguridad
Write-Header "2. VERIFICANDO SEGURIDAD"

$envTracked = git ls-files | Select-String "\.env$"
if ($envTracked) {
    Write-Error-Custom ".env está tracked en git (RIESGO DE SEGURIDAD)"
    Write-Host "Ejecuta: git rm --cached .env"
    exit 1
} else {
    Write-Success ".env no está tracked en git"
}

# Verificar .gitignore
if (Test-Path ".gitignore") {
    $gitignoreContent = Get-Content ".gitignore" | Out-String
    if ($gitignoreContent -match "^\.env$") {
        Write-Success ".env está en .gitignore"
    } else {
        Write-Warning-Custom ".env podría no estar en .gitignore"
    }
} else {
    Write-Error-Custom ".gitignore no encontrado"
    exit 1
}

# Pedir información de GitHub
Write-Header "3. INFORMACIÓN DE GITHUB"

if ([string]::IsNullOrEmpty($GitHubUsername)) {
    $GitHubUsername = Read-Host "Ingresa tu usuario de GitHub"
}
Write-Success "Usuario: $GitHubUsername"
Write-Success "Repositorio: $RepoName"

$repoURL = "https://github.com/$GitHubUsername/$RepoName.git"
Write-Host "`nURL del repositorio: $repoURL`n"

# Verificar si git ya está inicializado
Write-Header "4. INICIALIZANDO GIT"

if (Test-Path ".git") {
    Write-Warning-Custom "Git ya está inicializado"
    $reinit = Read-Host "¿Deseas reinicializar? (s/n)"
    if ($reinit.ToLower() -eq "s") {
        Remove-Item -Recurse -Force ".git"
        Write-Success "Git reincializado"
    }
} else {
    git init
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Git inicializado"
    } else {
        Write-Error-Custom "Error al inicializar git"
        exit 1
    }
}

# Configurar git user
$userName = git config user.name
$userEmail = git config user.email

if ([string]::IsNullOrEmpty($userName)) {
    $userName = Read-Host "Ingresa tu nombre completo"
    git config user.name $userName
}

if ([string]::IsNullOrEmpty($userEmail)) {
    $userEmail = Read-Host "Ingresa tu correo de GitHub"
    git config user.email $userEmail
}

Write-Success "Usuario: $userName <$userEmail>"

# Verificar estado
Write-Header "5. VERIFICANDO ARCHIVOS A COMMITEAR"

$status = git status --short
$envFile = $status | Select-String "\.env"

if ($envFile) {
    Write-Error-Custom ".env sería commiteado (RIESGO)"
    Write-Host "`nArchivos que serían commiteados:"
    Write-Host $status
    exit 1
} else {
    Write-Success ".env NO será commiteado ✓"
    Write-Host "`nArchivos que serán commiteados:"
    Write-Host $status
}

$proceed = Read-Host "`n¿Continuar? (s/n)"
if ($proceed.ToLower() -ne "s") {
    Write-Host "Cancelado"
    exit 0
}

# Agregar archivos
Write-Header "6. AGREGANDO ARCHIVOS"

git add .
if ($LASTEXITCODE -eq 0) {
    Write-Success "Archivos agregados"
} else {
    Write-Error-Custom "Error al agregar archivos"
    exit 1
}

# Crear commit
Write-Header "7. CREANDO COMMIT"

git commit -m $CommitMessage
if ($LASTEXITCODE -eq 0) {
    Write-Success "Commit creado"
} else {
    Write-Error-Custom "Error al crear commit"
    exit 1
}

# Renombrar rama a main
Write-Header "8. CONFIGURANDO RAMA"

git branch -M main
if ($LASTEXITCODE -eq 0) {
    Write-Success "Rama renombrada a 'main'"
} else {
    Write-Error-Custom "Error al renombrar rama"
    exit 1
}

# Agregar remote
Write-Header "9. CONECTANDO A GITHUB"

$existingRemote = git remote get-url origin 2>&1
if ($LASTEXITCODE -eq 0 -and $existingRemote -ne "fatal: No such remote") {
    Write-Warning-Custom "Remote 'origin' ya existe"
    $updateRemote = Read-Host "¿Actualizar URL? (s/n)"
    if ($updateRemote.ToLower() -eq "s") {
        git remote set-url origin $repoURL
        Write-Success "URL de remote actualizada"
    }
} else {
    git remote add origin $repoURL
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Remote agregado"
    } else {
        Write-Error-Custom "Error al agregar remote"
        exit 1
    }
}

# Instrucciones finales
Write-Header "10. INSTRUCCIONES FINALES"

Write-Host "Los cambios están listos para pushear. Debes:

1. Crear un repositorio vacío en GitHub:
   → Abre: https://github.com/new
   → Nombre: $RepoName
   → NO inicialices con README
   → Crea el repositorio

2. Luego ejecuta uno de estos comandos:

   Con HTTPS (requiere token):
   " -ForegroundColor $Cyan

Write-Host "   git push -u origin main`n" -ForegroundColor $Green

Write-Host "   Con SSH (requiere key configurada):
   git remote set-url origin git@github.com:$GitHubUsername/$RepoName.git
   git push -u origin main`n" -ForegroundColor $Green

Write-Host "3. Si pide autenticación:
   - Para HTTPS: usa tu token de GitHub (Settings > Developer settings > Tokens)
   - Para SSH: asegúrate de haber generado y agregado una SSH key

4. Verifica tu repositorio en:
   https://github.com/$GitHubUsername/$RepoName`n" -ForegroundColor $Cyan

Write-Host "¿Deseas pushear ahora? (s/n)"
$pushNow = Read-Host

if ($pushNow.ToLower() -eq "s") {
    Write-Header "PUSHEANDO A GITHUB"
    
    try {
        git push -u origin main
        if ($LASTEXITCODE -eq 0) {
            Write-Success "¡Repositorio subido exitosamente!"
            Write-Host "`n✨ Tu proyecto está ahora en GitHub:"
            Write-Host "   https://github.com/$GitHubUsername/$RepoName`n" -ForegroundColor $Green
        } else {
            Write-Error-Custom "Error al pushear"
            Write-Host "`nPuede ser por autenticación. Sigue las instrucciones de GitHub.`n"
        }
    } catch {
        Write-Error-Custom "Error: $_"
    }
} else {
    Write-Host "`nPuedes pushear después ejecutando:"
    Write-Host "git push -u origin main" -ForegroundColor $Yellow
}
