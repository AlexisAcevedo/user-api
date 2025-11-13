# 🎯 Guía Completa - Sistema de Autenticación FastAPI + Frontend

Bienvenido a tu sistema de autenticación completo. Este documento te guiará a través de cómo ejecutar, usar y personalizar tu aplicación.

## 📋 Contenido

1. [Inicio Rápido](#-inicio-rápido)
2. [Estructura del Proyecto](#-estructura-del-proyecto)
3. [API - Documentación](#-api---documentación)
4. [Frontend - Guía de Uso](#-frontend---guía-de-uso)
5. [Troubleshooting](#-troubleshooting)

---

## 🚀 Inicio Rápido

### Opción 1: Ejecutar Todo de Una Vez (Windows)

#### Con Batch (.bat)
```bash
# Haz doble clic en:
start-all.bat
```

#### Con PowerShell
```powershell
# Ejecuta en PowerShell como administrador:
.\start-all.ps1
```

### Opción 2: Ejecutar Manualmente en Dos Terminales

#### Terminal 1 - API
```bash
cd "e:\Alexis\python\gemini api"
uvicorn main:app --reload
```

#### Terminal 2 - Frontend
```bash
cd "e:\Alexis\python\gemini api"
python serve_frontend.py
```

### Opción 3: Ejecutar Solo la API (sin Frontend)
```bash
cd "e:\Alexis\python\gemini api"
uvicorn main:app --reload
```

---

## 📁 Estructura del Proyecto

```
gemini api/
├── 📄 main.py                 # Aplicación FastAPI principal
├── 📄 auth.py                 # Lógica de autenticación (JWT, hashing)
├── 📄 models.py               # Modelos de base de datos (SQLAlchemy)
├── 📄 schemas.py              # Esquemas de validación (Pydantic)
├── 📄 crud.py                 # Operaciones CRUD de base de datos
├── 📄 database.py             # Configuración de base de datos
├── 📄 logging_config.py        # Configuración de logging
├── 📄 conftest.py             # Configuración de pytest
├── 📄 test_main.py            # Suite de tests (17 tests)
├── 📄 serve_frontend.py        # Servidor para el frontend
├── 📄 start-all.bat           # Script para iniciar todo (Windows .bat)
├── 📄 start-all.ps1           # Script para iniciar todo (PowerShell)
├── 📄 requirements.txt         # Dependencias de Python
├── 📄 .env                     # Variables de entorno (gitignored)
│
├── 📁 frontend/               # Frontend web
│   ├── 📄 index.html          # Estructura HTML
│   ├── 📄 styles.css          # Estilos CSS (responsivo)
│   ├── 📄 main.js             # Lógica JavaScript (consumo API)
│   └── 📄 README.md           # Documentación del frontend
│
├── 📁 logs/                   # Archivos de log (autogenerados)
│   └── 📄 api_YYYY-MM-DD.log
│
├── 📁 __pycache__/            # Cache de Python (ignorar)
│
├── 📄 INSTRUCCIONES-DOCKER.md # Documentación Docker
├── 📄 IMPROVEMENTS.md         # Historial de mejoras
└── 📄 README.md              # README original
```

---

## 🔵 API - Documentación

### URLs Importantes

| Concepto | URL |
|----------|-----|
| API | http://127.0.0.1:8000 |
| API Docs (Swagger) | http://127.0.0.1:8000/docs |
| API ReDoc | http://127.0.0.1:8000/redoc |

### Endpoints Disponibles

#### Health Check
```
GET /health
Respuesta: { "status": "ok", "message": "API is running" }
Sin autenticación requerida
```

#### Registrar Nuevo Usuario
```
POST /register
Body: {
  "username": "usuario_nuevo",
  "password": "contraseña_segura"
}
Respuesta: { "id": 1, "username": "usuario_nuevo", "created_at": "..." }
Sin autenticación requerida
Rate Limit: 5 solicitudes por minuto
```

#### Iniciar Sesión
```
POST /token
Content-Type: application/x-www-form-urlencoded
Body: username=usuario&password=contraseña
Respuesta: {
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "expires_in": 1800,
  "token_type": "bearer"
}
Sin autenticación requerida
Rate Limit: 10 solicitudes por minuto
```

#### Obtener Datos del Usuario
```
GET /users/me
Headers: Authorization: Bearer {access_token}
Respuesta: { "id": 1, "username": "usuario", "created_at": "..." }
Requiere token de acceso válido
```

#### Renovar Tokens
```
POST /refresh
Headers: Authorization: Bearer {refresh_token}
Respuesta: {
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "expires_in": 1800,
  "token_type": "bearer"
}
Requiere token de refresh válido
```

### Configuración de Seguridad

**Algoritmo JWT:** HS256  
**Secret Key:** Guardado en `.env` (variable `SECRET_KEY`)  
**Access Token Expiry:** 30 minutos (configurable en `.env`)  
**Refresh Token Expiry:** 7 días (configurable en `.env`)  
**Hashing de Contraseña:** Argon2-cffi  

### Rate Limiting

| Endpoint | Límite |
|----------|--------|
| POST /register | 5 solicitudes / minuto |
| POST /token | 10 solicitudes / minuto |
| Otros endpoints | Sin límite |

---

## 🟠 Frontend - Guía de Uso

### Acceder al Frontend

```
http://127.0.0.1:8001
```

### Funcionalidades

#### 1️⃣ Registrar Nuevo Usuario

**Pasos:**
1. Abre http://127.0.0.1:8001
2. Ve a la pestaña "Registrarse"
3. Completa los campos:
   - Usuario (mínimo 3 caracteres)
   - Contraseña (mínimo 6 caracteres)
   - Confirmar contraseña
4. Haz clic en "Registrarse"

**Validaciones:**
- ✓ Usuario único (no duplicados)
- ✓ Longitud mínima de usuario (3 caracteres)
- ✓ Longitud mínima de contraseña (6 caracteres)
- ✓ Las contraseñas deben coincidir

**Mensajes:**
- Verde: Registro exitoso
- Rojo: Error (usuario duplicado, validación, etc.)

#### 2️⃣ Iniciar Sesión

**Pasos:**
1. Ve a la pestaña "Iniciar Sesión"
2. Ingresa usuario y contraseña
3. Haz clic en "Iniciar Sesión"

**Qué sucede:**
- ✓ Se obtienen los tokens (access + refresh)
- ✓ Se guarda la sesión en localStorage
- ✓ Se abre el dashboard automáticamente

#### 3️⃣ Dashboard - Panel de Control

Una vez autenticado, verás:

**📊 Información del Usuario**
- Nombre de usuario
- ID del usuario
- Fecha de registro

**🔑 Información de Tokens**
- Access Token (JWT) - es el que se usa para acceder a endpoints protegidos
- Refresh Token - se usa para renovar el access token cuando expira
- Tiempo restante de expiración

**⚙️ Acciones**
- **Obtener Datos**: Hace una solicitud GET a `/users/me` con tu access token
- **Renovar Token**: Obtiene nuevos tokens usando el refresh token

**🧪 Pruebas de Endpoints**
- **GET /health**: Verifica si la API está en línea
- **GET /users/me**: Prueba acceder a tu información protegida

#### 4️⃣ Cerrar Sesión

**Pasos:**
1. Haz clic en el botón "Cerrar Sesión" (rojo)
2. Confirma que deseas cerrar sesión
3. Serás redirigido al formulario de login

**Qué sucede:**
- ✓ Se borra la sesión del localStorage
- ✓ Se limpian los tokens de la memoria
- ✓ Se vuelve al estado no autenticado

---

## 🧪 Testing

### Ejecutar Todos los Tests

```bash
cd "e:\Alexis\python\gemini api"
pytest test_main.py -v
```

### Resultados Esperados

```
17 passed in 0.87s
```

**Cobertura de Tests:**

| Categoría | Tests | Descripción |
|-----------|-------|-------------|
| Health Check | 1 | Verifica que la API está en línea |
| Registro | 5 | Validación de registro (usuario, contraseña, duplicados) |
| Autenticación | 7 | Login, tokens, endpoints protegidos |
| Hashing | 2 | Seguridad de contraseñas (Argon2) |
| Edge Cases | 2 | Casos especiales (caracteres especiales, longitud máxima) |

---

## 🔧 Configuración

### Variables de Entorno (.env)

```env
# Base de datos
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname

# JWT
SECRET_KEY=tu-clave-secreta-super-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Cambiar Puerto de la API

**En `main.py` o al ejecutar:**
```bash
uvicorn main:app --port 8000 --reload
```

### Cambiar Puerto del Frontend

**En `serve_frontend.py`, modifica:**
```python
PORT = 8001  # Cambiar aquí
```

---

## 🐛 Troubleshooting

### Error: "API offline"

**Problema:** El frontend muestra "🔴 API Offline"

**Soluciones:**
1. Verifica que la API está corriendo: `uvicorn main:app --reload`
2. Verifica que está en http://127.0.0.1:8000
3. Revisa si hay un firewall bloqueando el puerto 8000
4. Abre la consola del navegador (F12) para ver errores

### Error: CORS

**Problema:** `CORS policy: Access to XMLHttpRequest ... has been blocked`

**Solución:**
1. Verifica que `CORSMiddleware` está configurado en `main.py`
2. Verifica que http://127.0.0.1:8001 está en `allow_origins`
3. Reinicia la API

### Error: "Credenciales inválidas"

**Problema:** El login falla aunque el usuario existe

**Causas posibles:**
- Contraseña incorrecta
- Usuario no existe
- Base de datos no tiene el usuario

**Solución:**
1. Verifica que registraste el usuario primero
2. Verifica que la contraseña es correcta
3. Revisa los logs: `logs/api_YYYY-MM-DD.log`

### Error: "El usuario ya existe"

**Problema:** No puedo registrar un usuario porque ya existe

**Solución:**
- Elige otro nombre de usuario
- O borra el usuario de la base de datos si estás en desarrollo

### Tokens expirando rápido

**Problema:** El token de acceso expira en 30 minutos

**Soluciones:**
1. Usa "Renovar Token" en el dashboard
2. O cambia `ACCESS_TOKEN_EXPIRE_MINUTES` en `.env` (valor en minutos)

### Base de datos: "Error de conexión"

**Problema:** No puede conectar a PostgreSQL

**Soluciones:**
1. Verifica que PostgreSQL está corriendo
2. Verifica que la `DATABASE_URL` en `.env` es correcta
3. Verifica usuario y contraseña
4. Verifica que la base de datos existe

---

## 🔐 Seguridad

### Mejores Prácticas Implementadas

✅ Contraseñas hasheadas con Argon2  
✅ JWT para autenticación stateless  
✅ Tokens con expiración configurable  
✅ Refresh tokens separados de access tokens  
✅ Rate limiting para endpoints críticos  
✅ CORS configurado  
✅ Variables sensibles en `.env` (no en código)  
✅ Logging detallado de eventos  
✅ Validación de entrada en frontend y backend  

### Recomendaciones para Producción

⚠️ **NO** usar estos valores en producción:
- `SECRET_KEY` debe ser una clave criptográficamente segura
- Cambiar `allow_origins` de CORS a dominios específicos
- Cambiar `DATABASE_URL` a una base de datos remota segura
- Habilitar HTTPS (usar certificados SSL)
- Almacenar tokens en httpOnly cookies en lugar de localStorage

---

## 📚 Recursos y Enlaces

### Documentación Oficial

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Pydantic v2](https://docs.pydantic.dev/latest/)
- [Python JWT](https://pyjwt.readthedocs.io/)
- [Passlib](https://passlib.readthedocs.io/)

### Conceptos

- [JWT (JSON Web Token)](https://jwt.io/)
- [OAuth 2.0](https://oauth.net/2/)
- [Rate Limiting](https://en.wikipedia.org/wiki/Rate_limiting)
- [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

### Herramientas Útiles

- [Postman](https://www.postman.com/) - Para probar la API
- [JWT Debugger](https://jwt.io/) - Para inspeccionar tokens
- [DB Browser SQLite](https://sqlitebrowser.org/) - Para ver la base de datos

---

## 🎉 ¡Listo!

¡Tu sistema de autenticación está completamente operativo! 

**Próximos pasos:**
1. ✅ Ejecuta `start-all.bat` o `start-all.ps1`
2. ✅ Abre http://127.0.0.1:8001 en tu navegador
3. ✅ Registra un nuevo usuario
4. ✅ Inicia sesión
5. ✅ ¡Explora las funcionalidades!

---

## 📞 Soporte

Si encuentras problemas:

1. Revisa los **logs** en `logs/api_YYYY-MM-DD.log`
2. Abre la **consola del navegador** (F12)
3. Revisa esta **Guía de Troubleshooting**
4. Verifica que todos los **servicios están corriendo**

---

**Creado con ❤️ usando FastAPI, SQLAlchemy, Pydantic, JWT y Vanilla JavaScript**

*Última actualización: 12 de Noviembre de 2025*
