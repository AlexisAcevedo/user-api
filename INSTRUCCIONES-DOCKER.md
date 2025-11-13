# Instrucciones para Instalar Docker y Ejecutar la Aplicación

## Requisitos Previos

Docker Desktop requiere WSL2 (Windows Subsystem for Linux 2) en Windows.

## Opción 1: Instalación Automática (Recomendada)

1. **Abre PowerShell como Administrador:**
   - Presiona `Win + X`
   - Selecciona "Windows PowerShell (Administrador)" o "Terminal (Administrador)"

2. **Ejecuta el script de instalación:**
   ```powershell
   cd "E:\Alexis\python\gemini api"
   .\instalar-docker.ps1
   ```

3. **Reinicia tu computadora** cuando se te solicite

4. **Después del reinicio:**
   - Abre Docker Desktop desde el menú de inicio
   - Espera a que Docker se inicie completamente (verás el ícono de Docker en la bandeja del sistema)

5. **Ejecuta la aplicación:**
   ```powershell
   docker compose up --build -d
   ```

## Opción 2: Instalación Manual

### Paso 1: Instalar WSL2

Abre PowerShell como Administrador y ejecuta:

```powershell
wsl --install
```

Reinicia tu computadora.

### Paso 2: Instalar Docker Desktop

1. Descarga Docker Desktop desde: https://www.docker.com/products/docker-desktop/
2. Ejecuta el instalador
3. Sigue las instrucciones del instalador
4. Reinicia tu computadora si es necesario
4. Abre Docker Desktop y espera a que se inicie

### Paso 3: Ejecutar la Aplicación

Una vez que Docker Desktop esté corriendo:

```powershell
cd "E:\Alexis\python\gemini api"
docker compose up --build -d
```

## Verificar la Instalación

Para verificar que Docker está funcionando:

```powershell
docker --version
docker compose version
```

## Comandos Útiles

```powershell
# Ver los contenedores en ejecución
docker compose ps

# Ver los logs
docker compose logs -f

# Detener los contenedores
docker compose down

# Detener y eliminar volúmenes
docker compose down -v
```

## Acceso a la Aplicación

Una vez que los contenedores estén corriendo:

- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Base de datos**: localhost:5432

