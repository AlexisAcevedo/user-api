# schemas.py
"""
Esquemas Pydantic para validación de datos.
Define los modelos de entrada y salida de la API.
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class Token(BaseModel):
    """Esquema para la respuesta de tokens JWT."""
    access_token: str = Field(..., description="Token JWT de acceso")
    refresh_token: str = Field(..., description="Token JWT de refresco")
    token_type: str = Field(default="bearer", description="Tipo de token")
    expires_in: int = Field(..., description="Tiempo en segundos hasta expiración del access token")

class UserBase(BaseModel):
    """Base para esquemas de usuario."""
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario único")

class UserCreate(UserBase):
    """Esquema para crear un nuevo usuario."""
    password: str = Field(..., min_length=8, max_length=72, description="Contraseña del usuario")

class UserInDB(UserBase):
    """Esquema para devolver información del usuario desde la base de datos."""
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)