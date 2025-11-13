"""
Script para agregar la columna created_at a la tabla users
"""
import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

# Cargar variables de entorno
load_dotenv()

async def fix_database():
    """Agrega la columna created_at a la tabla users"""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ Error: DATABASE_URL no está configurada en .env")
        return
    
    print(f"🔄 Conectando a base de datos: {database_url}")
    
    try:
        # Crear engine
        engine = create_async_engine(database_url)
        
        async with engine.begin() as conn:
            # Agregar columna
            await conn.execute(text('''
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            '''))
            
            # Actualizar filas existentes con el timestamp actual
            await conn.execute(text('''
                UPDATE users 
                SET created_at = CURRENT_TIMESTAMP 
                WHERE created_at IS NULL
            '''))
            
            print("✅ Columna created_at agregada/actualizada exitosamente")
            
            # Verificar la estructura de la tabla
            result = await conn.execute(text('''
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'users'
                ORDER BY ordinal_position
            '''))
            
            print("\n📋 Estructura actual de la tabla users:")
            for row in result:
                nullable = "NULL" if row[2] == "YES" else "NOT NULL"
                print(f"   - {row[0]}: {row[1]} ({nullable})")
        
        await engine.dispose()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(fix_database())
