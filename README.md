# API de Autenticación de Usuarios con FastAPI

Una API REST segura y moderna para autenticación de usuarios con JWT, construida con FastAPI y PostgreSQL.

## 🚀 Características

- ✅ Registro e inicio de sesión de usuarios
- ✅ Autenticación con tokens JWT (Access + Refresh)
- ✅ Hashing seguro de contraseñas con Argon2
- ✅ Base de datos PostgreSQL asincrónica
- ✅ Documentación interactiva con Swagger
- ✅ Validación de datos con Pydantic
- ✅ Manejo de errores robusto
- ✅ Rate Limiting para prevenir ataques de fuerza bruta
- ✅ Logging estructurado con rotación de archivos
- ✅ Tests automatizados con pytest
- ✅ **Docker y Docker Compose** para containerización
- ✅ Frontend web interactivo (HTML/CSS/JS)

## 📋 Requisitos

- Python 3.10+
- PostgreSQL 12+
- pip

## � Inicio Rápido con Docker

**Recomendado para desarrollo y producción**

### Requisitos
- Docker 20.10+
- Docker Compose 1.29+

### Pasos

1. **Crear archivo de configuración**
   ```bash
   copy .env.example .env
   ```

2. **Actualizar variables sensibles** (opcional)
   ```bash
   # Edita .env y cambia:
   # - SECRET_KEY (genera uno nuevo si quieres)
   # - Contraseña de base de datos
   # - CORS_ORIGINS para tu dominio
   ```

3. **Iniciar servicios**
   ```bash
   docker-compose up -d
   ```

4. **Acceder a la aplicación**
   - Frontend: http://localhost
   - API Swagger: http://localhost/docs
   - pgAdmin: http://localhost:5050

### Comandos Útiles

```bash
# Ver estado de servicios
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f api

# Detener servicios
docker-compose down

# Ejecutar tests dentro de Docker
docker-compose exec api pytest test_main.py -v
```

**Para documentación completa de Docker, ver `DOCKER-GUIDE.md`**

---

## �🔧 Instalación Local (Sin Docker)

### 1. Clonar el repositorio

```bash
cd "e:\Alexis\python\gemini api"
```

### 2. Crear un entorno virtual

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # En PowerShell
# O: venv\Scripts\activate.bat  # En CMD
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL="postgresql+asyncpg://postgres:tu_contraseña@localhost:5432/fastapi_db"
SECRET_KEY="tu_clave_secreta_aqui"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES="30"
```

### 5. Crear la base de datos (si no existe)

```bash
psql -U postgres
CREATE DATABASE fastapi_db;
\q
```

### 6. Ejecutar la aplicación

```bash
uvicorn main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`

## 📖 Endpoints

### Health Check
- **GET** `/health` - Verifica que la API está funcionando

### Autenticación
- **POST** `/register` - Registrar nuevo usuario
  ```json
  {
    "username": "usuario",
    "password": "contraseña_segura"
  }
  ```

- **POST** `/token` - Obtener tokens JWT (access + refresh)
  ```json
  {
    "username": "usuario",
    "password": "contraseña_segura"
  }
  ```
  Respuesta:
  ```json
  {
    "access_token": "...",
    "refresh_token": "...",
    "token_type": "bearer",
    "expires_in": 1800
  }
  ```

- **POST** `/refresh` - Refrescar access token
  - Requiere: `Authorization: Bearer <refresh_token>`
  - Devuelve: Nuevo access_token y refresh_token

### Usuarios
- **GET** `/users/me` - Obtener información del usuario autenticado
  - Requiere: `Authorization: Bearer <token>`

## 🔐 Seguridad

- Las contraseñas se hashean con **Argon2**, el algoritmo recomendado por OWASP
- Los access tokens expiran automáticamente después de 30 minutos
- Los refresh tokens tienen validez de 7 días
- **Rate Limiting**:
  - Registro: 5 intentos por minuto por IP
  - Login: 10 intentos por minuto por IP
- Las variables sensibles se cargan desde variables de entorno
- El archivo `.env` está incluido en `.gitignore`
- Logging estructurado de todos los eventos de seguridad

## 📚 Documentación Interactiva

Una vez que la aplicación está corriendo, accede a:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 🗂️ Estructura del Proyecto

```
gemini api/
├── main.py              # Aplicación principal y endpoints
├── auth.py              # Autenticación y tokens JWT
├── database.py          # Configuración de base de datos
├── models.py            # Modelos de SQLAlchemy
├── schemas.py           # Esquemas Pydantic
├── crud.py              # Operaciones de base de datos
├── requirements.txt     # Dependencias del proyecto
├── .env                 # Variables de entorno (no commitear)
├── .gitignore           # Archivos a ignorar en Git
└── README.md            # Este archivo
```

## 🧪 Pruebas Manuales

### 1. Registrar un usuario

```bash
curl -X POST "http://127.0.0.1:8000/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"securepass123"}'
```

### 2. Obtener tokens

```bash
curl -X POST "http://127.0.0.1:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=securepass123"
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 3. Acceder a datos protegidos

```bash
curl -X GET "http://127.0.0.1:8000/users/me" \
  -H "Authorization: Bearer <tu_access_token_aqui>"
```

### 4. Refrescar el access token

```bash
curl -X POST "http://127.0.0.1:8000/refresh" \
  -H "Authorization: Bearer <tu_refresh_token_aqui>"
```

## 🧪 Ejecutar Tests Automatizados

```bash
# Correr todos los tests
pytest test_main.py -v

# Correr con cobertura
pytest test_main.py --cov

# Correr tests específicos
pytest test_main.py -k "test_register" -v
```

Incluye tests para:
- ✅ Registro de usuarios
- ✅ Login y validación de credenciales
- ✅ Generación de tokens
- ✅ Acceso a endpoints protegidos
- ✅ Hashing y verificación de contraseñas
- ✅ Casos edge (caracteres especiales, etc.)

## 🐛 Solución de Problemas

### Error de conexión a PostgreSQL
- Verifica que PostgreSQL está corriendo: `net start postgresql-x64-15`
- Revisa que la cadena `DATABASE_URL` en `.env` es correcta
- Confirma que la base de datos existe: `psql -U postgres -l`

### Error de TOKEN inválido
- Verifica que incluiste el token en el header: `Authorization: Bearer <token>`
- Confirma que el token no ha expirado (tienen validez de 30 minutos)

### Puerto 8000 ya está en uso
```bash
# Usa un puerto diferente
uvicorn main:app --reload --port 8001
```

## 📝 Notas de Desarrollo

- El modo `--reload` recarga automáticamente la app cuando hay cambios
- Los logs de SQLAlchemy están habilitados (`echo=True`) para debugging
- En producción, desactiva `echo=True` en `database.py`

## 🚀 Despliegue en Producción

1. Genera una nueva `SECRET_KEY`:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. Desactiva el modo debug:
   - Cambia `echo=True` a `echo=False` en `database.py`
   - Actualiza `SECRET_KEY` en `.env`

3. Usa un servidor ASGI en producción (Gunicorn + Uvicorn):
   ```bash
   pip install gunicorn
   gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
   ```

## 📄 Licencia

Este proyecto está disponible bajo la licencia MIT.

## 👤 Autor

Desarrollado como ejemplo de autenticación segura con FastAPI.
