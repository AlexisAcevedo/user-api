# 🚀 Subir a GitHub - Guía Rápida (3 Pasos)

## OPCIÓN A: Script Automático (Recomendado) ⭐

### Paso 1: Ejecuta el Script

**En PowerShell:**
```powershell
cd "E:\Alexis\python\gemini api"
.\push-to-github.ps1
```

**O en CMD/Batch:**
```bash
cd E:\Alexis\python\gemini api
push-to-github.bat
```

El script te guiará automáticamente. Solo responde las preguntas.

### Paso 2: Crea Repositorio en GitHub

1. Abre: https://github.com/new
2. **Nombre**: `gemini-api` (o el que quieras)
3. **Descripción**: `FastAPI Authentication System with Docker Support`
4. **Privacidad**: Elige Public o Private
5. **NO inicialices** con README, .gitignore, o licencia
6. Click en "Create repository"

### Paso 3: Copia el Comando de Push

El script te dirá qué comando ejecutar. Será algo como:

```bash
git push -u origin main
```

**Si pide autenticación:**
- **HTTPS**: Necesitas un token personal de GitHub
- **SSH**: Necesitas una SSH key configurada

---

## OPCIÓN B: Manual (Si prefieres control)

### Paso 1: Preparar Proyecto

```bash
# Ir a la carpeta del proyecto
cd "E:\Alexis\python\gemini api"

# Crear .env desde plantilla (SI NO EXISTE)
copy .env.example .env

# Editar .env con tus valores reales
notepad .env
```

### Paso 2: Inicializar Git

```bash
# Inicializar repositorio
git init

# Configurar usuario
git config user.name "Tu Nombre"
git config user.email "tu@email.com"

# Verificar que .env NO está tracked
git status
# .env debe aparecer como "Untracked files", NO bajo "Changes to be committed"
```

### Paso 3: Hacer Primer Commit

```bash
# Agregar archivos
git add .

# Crear commit
git commit -m "Initial commit: FastAPI authentication with Docker support"

# Renombrar rama a main
git branch -M main
```

### Paso 4: Conectar a GitHub

```bash
# Reemplaza TU_USUARIO y gemini-api con tus datos
git remote add origin https://github.com/TU_USUARIO/gemini-api.git

# Pushear
git push -u origin main
```

---

## 🔐 Verificación de Seguridad

Antes de cualquier paso, verifica:

```bash
# 1. Verificar .env NO está tracked
git ls-files | findstr ".env"
# Resultado: DEBE ESTAR VACÍO

# 2. Ver qué se va a commitear
git status
# .env debe estar en "Untracked files"
```

Si algo está mal, aquí está el script de verificación:

```bash
python check_security.py
```

---

## 📋 Autenticación en GitHub

### Opción HTTPS (Token)

```bash
# 1. Generar token en GitHub:
#    Settings > Developer settings > Personal access tokens > Generate new token
#    - Dale acceso a: repo, write:repo_hook
#    - Copia el token

# 2. Al pushear, pega el token como contraseña
#    Username: tu_usuario
#    Password: tu_token
```

### Opción SSH (Recomendada)

```bash
# 1. Generar SSH key (si no tienes)
ssh-keygen -t ed25519 -C "tu@email.com"
# Presiona Enter en todos los prompts

# 2. Agregar a SSH agent
eval $(ssh-agent -s)
ssh-add ~/.ssh/id_ed25519

# 3. Copiar clave pública a GitHub
type %USERPROFILE%\.ssh\id_ed25519.pub
# Copia el contenido y pégalo en:
# GitHub > Settings > SSH and GPG keys > New SSH key

# 4. Cambiar URL del remote (opcional)
git remote set-url origin git@github.com:TU_USUARIO/gemini-api.git

# 5. Pushear
git push -u origin main
```

---

## ✅ Checklist Final

Antes de hacer push:

- [ ] `.env` creado (copia de `.env.example`)
- [ ] `.env` editado con tus valores reales
- [ ] Git inicializado (`git init`)
- [ ] Usuario configurado (`git config user.name`)
- [ ] Primer commit hecho (`git commit`)
- [ ] Remote agregado (`git remote add origin`)
- [ ] Rama renombrada a main (`git branch -M main`)
- [ ] Repositorio creado en GitHub (vacío)
- [ ] Token o SSH key configurado
- [ ] `git status` muestra .env como untracked

---

## 🚨 Errores Comunes

### Error: "fatal: not a git repository"
**Solución:**
```bash
git init
```

### Error: "fatal: No such remote 'origin'"
**Solución:**
```bash
git remote add origin https://github.com/TU_USUARIO/gemini-api.git
```

### Error: "remote origin already exists"
**Solución:**
```bash
git remote set-url origin https://github.com/TU_USUARIO/gemini-api.git
```

### Error: "Permission denied" (SSH)
**Solución:**
```bash
# Verificar SSH key
ssh -T git@github.com

# Regenear si es necesario
ssh-keygen -t ed25519 -C "tu@email.com"
```

### Error: "rejected ... (branch is ahead of what you can fast-forward)"
**Solución:**
```bash
git push --force-with-lease origin main
# O pull primero:
git pull origin main
```

---

## 📞 Después de Subir

1. **Verifica tu repositorio:**
   https://github.com/TU_USUARIO/gemini-api

2. **Configura GitHub (opcional pero recomendado):**
   - Settings > Branch protection rules
   - Require pull request reviews
   - Require status checks to pass

3. **Compartir:**
   - Dale a tus amigos el link de GitHub
   - Copia el link "Clone with HTTPS/SSH"

4. **Clonar en otra máquina:**
   ```bash
   git clone https://github.com/TU_USUARIO/gemini-api.git
   cd gemini-api
   copy .env.example .env
   # Editar .env con credenciales
   docker-compose up -d
   ```

---

## ✨ Resumen

**Lo más fácil:**
```bash
.\push-to-github.ps1
```

**Lo más rápido:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/TU_USUARIO/gemini-api.git
git push -u origin main
```

---

**¡Eso es todo! Tu proyecto está en GitHub 🎉**
