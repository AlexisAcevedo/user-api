# crud.py
"""
Operaciones CRUD (Create, Read, Update, Delete) para usuarios.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models, schemas
from auth import get_password_hash

async def get_user_by_username(db: AsyncSession, username: str):
    """Obtiene un usuario por su nombre de usuario."""
    result = await db.execute(select(models.User).filter(models.User.username == username))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    """Crea un nuevo usuario en la base de datos."""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user