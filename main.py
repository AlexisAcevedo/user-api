# main.py
"""
API de Autenticación de Usuarios con FastAPI.
Proporciona endpoints para registro, login y acceso a datos de usuario autenticado.
"""
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de entorno desde el archivo .env

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from slowapi import Limiter
from slowapi.util import get_remote_address

from logging_config import setup_logging, get_logger

# Configurar logging
setup_logging()
logger = get_logger(__name__)

import crud, models, schemas
from auth import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_current_user_from_refresh_token,
    verify_password,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)
from database import engine, get_db

# --- CONFIGURACIÓN DE RATE LIMITING ---
limiter = Limiter(key_func=get_remote_address)


async def create_db_and_tables():
    """Crea las tablas de la base de datos al iniciar la aplicación."""
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


app = FastAPI(
    title="API de Autenticación de Usuarios",
    description="API simple y segura para autenticar usuarios con JWT",
    version="1.0.0",
)

# Agregar rate limiter a la app
app.state.limiter = limiter

# Configurar CORS para permitir que el frontend acceda a la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001", "http://localhost:8001", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- EXCEPTION HANDLERS PERSONALIZADOS ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Maneja errores de validación de Pydantic y devuelve mensajes claros al usuario.
    """
    errors = exc.errors()
    error_messages = []
    
    for error in errors:
        field = error['loc'][-1]
        msg = error['msg']
        
        # Mensajes personalizados para campos específicos
        if field == 'password':
            if 'at least 8 characters' in msg:
                error_messages.append('La contraseña debe tener al menos 8 caracteres')
            elif 'at most 72 characters' in msg:
                error_messages.append('La contraseña no puede exceder 72 caracteres')
            else:
                error_messages.append(f'Error en la contraseña: {msg}')
        elif field == 'username':
            if 'at least 3 characters' in msg:
                error_messages.append('El usuario debe tener al menos 3 caracteres')
            elif 'at most 50 characters' in msg:
                error_messages.append('El usuario no puede exceder 50 caracteres')
            else:
                error_messages.append(f'Error en el usuario: {msg}')
        else:
            error_messages.append(f'Error en {field}: {msg}')
    
    return {
        "detail": " | ".join(error_messages) if error_messages else "Error de validación"
    }


@app.on_event("startup")
async def on_startup():
    """Evento que se ejecuta al iniciar la aplicación."""
    await create_db_and_tables()


@app.get("/health", tags=["health"])
async def health_check():
    """Verifica que la API está funcionando correctamente."""
    logger.info("Health check ejecutado")
    return {"status": "ok", "message": "API running"}


@app.post(
    "/register",
    response_model=schemas.UserInDB,
    status_code=status.HTTP_201_CREATED,
    tags=["auth"],
    summary="Registrar un nuevo usuario",
    responses={
        201: {"description": "Usuario registrado exitosamente"},
        400: {"description": "El nombre de usuario ya existe"},
    },
)
@limiter.limit("5/minute")  # Máximo 5 registros por minuto por IP
async def register(request: Request, user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Registra un nuevo usuario en la base de datos.
    
    - **username**: Nombre de usuario único (3-50 caracteres)
    - **password**: Contraseña segura (8-72 caracteres)
    
    **Rate Limit**: 5 registros por minuto por IP
    """
    logger.info(f"Intento de registro para usuario: {user.username}")
    db_user = await crud.get_user_by_username(db, username=user.username)
    if db_user:
        logger.warning(f"Intento de registrar usuario duplicado: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado",
        )
    new_user = await crud.create_user(db=db, user=user)
    logger.info(f"Usuario registrado exitosamente: {user.username}")
    return new_user


@app.post(
    "/token",
    response_model=schemas.Token,
    tags=["auth"],
    summary="Obtener token de acceso",
    responses={
        200: {"description": "Token obtenido exitosamente"},
        401: {"description": "Credenciales incorrectas"},
    },
)
@limiter.limit("10/minute")  # Máximo 10 intentos de login por minuto por IP
async def login_for_access_token(
    request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    """
    Obtiene un token JWT para acceder a endpoints protegidos.
    
    - **username**: Nombre de usuario registrado
    - **password**: Contraseña del usuario
    
    **Rate Limit**: 10 intentos por minuto por IP (previene fuerza bruta)
    """
    logger.info(f"Intento de login para usuario: {form_data.username}")
    user = await crud.get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Login fallido para usuario: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )
    logger.info(f"Login exitoso para usuario: {form_data.username}")
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@app.get(
    "/users/me",
    response_model=schemas.UserInDB,
    tags=["users"],
    summary="Obtener información del usuario autenticado",
    responses={
        200: {"description": "Información del usuario obtenida exitosamente"},
        401: {"description": "Token inválido o no proporcionado"},
        404: {"description": "Usuario no encontrado"},
    },
)
async def read_users_me(
    current_user: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """
    Devuelve la información del usuario actualmente autenticado.
    Requiere un token JWT válido en el header `Authorization: Bearer <token>`.
    """
    logger.info(f"Acceso a /users/me por: {current_user}")
    user = await crud.get_user_by_username(db, username=current_user)
    if user is None:
        logger.warning(f"Usuario no encontrado: {current_user}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return user


@app.post(
    "/refresh",
    response_model=schemas.Token,
    tags=["auth"],
    summary="Refrescar token de acceso",
    responses={
        200: {"description": "Token refrescado exitosamente"},
        401: {"description": "Token de refresco inválido o expirado"},
    },
)
async def refresh_token(current_user: str = Depends(get_current_user_from_refresh_token)):
    """
    Obtiene un nuevo access token usando un refresh token válido.
    
    El refresh token debe ser enviado en el header `Authorization: Bearer <refresh_token>`.
    Los refresh tokens son válidos por 7 días.
    """
    logger.info(f"Token refrescado para usuario: {current_user}")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        data={"sub": current_user}, expires_delta=refresh_token_expires
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }