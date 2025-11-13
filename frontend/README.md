# 🎨 Frontend - Sistema de Autenticación

Frontend moderno y responsivo para consumir la API de autenticación de usuarios con FastAPI.

## 📋 Características

- ✅ Registro de nuevos usuarios
- ✅ Inicio de sesión con JWT
- ✅ Renovación automática de tokens (refresh tokens)
- ✅ Visualización de información del usuario
- ✅ Cierre de sesión seguro
- ✅ Persistencia de sesión (localStorage)
- ✅ Interfaz responsiva (mobile-friendly)
- ✅ Pruebas de endpoints en tiempo real
- ✅ Monitoreo de salud de la API

## 🚀 Inicio Rápido

### 1. Asegurate que la API esté corriendo

```bash
cd "e:\Alexis\python\gemini api"
uvicorn main:app --reload
```

La API estará disponible en: `http://127.0.0.1:8000`

### 2. Inicia el servidor del frontend

En otra terminal:

```bash
cd "e:\Alexis\python\gemini api"
python serve_frontend.py
```

El frontend estará disponible en: `http://127.0.0.1:8001`

### 3. Abre el navegador

Accede a `http://127.0.0.1:8001` en tu navegador preferido.

## 📁 Estructura de Archivos

```
frontend/
├── index.html          # Estructura HTML principal
├── styles.css          # Estilos CSS (diseño responsivo)
├── main.js             # Lógica JavaScript (consumo de API)
└── README.md           # Este archivo
```

## 🎯 Funcionalidades Principales

### Registro de Usuario

1. Dirígete a la pestaña "Registrarse"
2. Ingresa un usuario (mínimo 3 caracteres)
3. Ingresa una contraseña (mínimo 6 caracteres)
4. Confirma la contraseña
5. Haz clic en "Registrarse"

**Validaciones:**
- Usuario debe tener al menos 3 caracteres
- Contraseña debe tener al menos 6 caracteres
- Las contraseñas deben coincidir
- Usuario no puede estar duplicado

### Inicio de Sesión

1. Dirígete a la pestaña "Iniciar Sesión"
2. Ingresa tu usuario
3. Ingresa tu contraseña
4. Haz clic en "Iniciar Sesión"

**Al iniciar sesión:**
- Se guardan los tokens (access + refresh)
- Se muestra la información del usuario
- Se abre el dashboard

### Dashboard

Una vez autenticado, tendrás acceso a:

#### 📊 Información del Usuario
- Usuario
- ID de usuario
- Fecha de registro

#### 🔑 Información de Tokens
- Access Token (JWT)
- Refresh Token
- Tiempo de expiración

#### ⚙️ Acciones
- **Obtener Datos del Usuario**: Hace una petición GET a `/users/me`
- **Renovar Token**: Obtiene nuevos tokens usando el refresh token

#### 🧪 Pruebas de Endpoints
- **GET /health**: Verifica que la API está en línea
- **GET /users/me**: Obtiene los datos del usuario autenticado

## 🔐 Seguridad

### Almacenamiento de Tokens

Los tokens se almacenan en `localStorage` del navegador. Esto es conveniente para desarrollo, pero en producción considere:

- Usar `sessionStorage` (se borra al cerrar el navegador)
- Almacenar en cookies HTTP-only (más seguras)
- Implementar una política de CSRF

### Headers de Seguridad

- Authorization: Bearer {token}
- Content-Type: application/json
- CORS configurado en la API

## 🌐 Consumo de API

Todos los endpoints de la API están documentados en:

```
http://127.0.0.1:8000/docs
```

### Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Verifica que la API esté en línea |
| POST | `/register` | Registra un nuevo usuario |
| POST | `/token` | Obtiene tokens de acceso (login) |
| GET | `/users/me` | Obtiene datos del usuario autenticado |
| POST | `/refresh` | Obtiene nuevos tokens |

## 💾 Persistencia de Datos

El frontend mantiene la sesión usando `localStorage`:

```javascript
// Datos guardados
{
  isAuthenticated: true,
  user: { ... },
  accessToken: "...",
  refreshToken: "...",
  tokenExpiry: "..."
}
```

**Al recargar la página:**
- Se restaura automáticamente la sesión
- Se verifica si el token ha expirado
- Si expiró, se limpia el localStorage

## 📱 Responsive Design

El frontend es completamente responsivo y funciona en:

- 🖥️ Escritorio (1920px+)
- 💻 Laptop (1024px - 1920px)
- 📱 Tablet (768px - 1024px)
- 📱 Mobile (< 768px)

## 🐛 Troubleshooting

### "Error de conexión. Verifica que la API esté en línea."

**Solución:**
1. Verifica que la API está corriendo: `http://127.0.0.1:8000`
2. Verifica que no hay un firewall bloqueando la conexión
3. Revisa la consola del navegador (F12 → Console) para errores

### CORS Error

**Mensaje:** `Access to XMLHttpRequest at 'http://127.0.0.1:8000/...' from origin 'http://127.0.0.1:8001' has been blocked by CORS policy`

**Solución:**
1. Verifica que CORS esté habilitado en `main.py`
2. Verifica que la URL del frontend está en `allow_origins`
3. Reinicia la API

### Tokens expirando rápido

**Causa:** El token tiene un tiempo de expiración muy corto (30 minutos por defecto)

**Solución:**
1. Usa "Renovar Token" en el dashboard para obtener nuevos tokens
2. O modifica `ACCESS_TOKEN_EXPIRE_MINUTES` en `.env`

### Contraseña no se guarda correctamente

**Causa:** Probablemente está usando la contraseña de ejemplo

**Solución:**
1. Intenta con una contraseña más larga
2. Evita contraseñas muy simples
3. Revisa la consola para errores de validación

## 🎨 Personalización

### Cambiar colores

Edita las variables CSS en `styles.css`:

```css
:root {
    --primary-color: #2563eb;
    --danger-color: #ef4444;
    --success-color: #10b981;
    /* ... más colores */
}
```

### Cambiar URL de la API

Edita `main.js`:

```javascript
const API_URL = 'http://127.0.0.1:8000';  // Cambiar aquí
```

### Agregar más campos al registro

1. Edita `index.html` (agregar input)
2. Edita `main.js` (leer valor y enviarlo)
3. Edita `schemas.py` en la API (agregar campo)

## 📚 Recursos

- [FastAPI Documentación](https://fastapi.tiangolo.com/)
- [JWT en FastAPI](https://fastapi.tiangolo.com/advanced/security/oauth2-jwt/)
- [CORS en FastAPI](https://fastapi.tiangolo.com/tutorial/cors/)
- [Fetch API](https://developer.mozilla.org/es/docs/Web/API/Fetch_API)

## 🤝 Contribuciones

Si encuentras bugs o tienes sugerencias, puedes:

1. Abrir un issue
2. Enviar un pull request
3. Contactar al desarrollador

## 📄 Licencia

Este proyecto está bajo licencia MIT.

---

**Creado con ❤️ usando FastAPI + Vanilla JavaScript**
