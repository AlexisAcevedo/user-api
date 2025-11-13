"""
Módulo de logging estructurado para la aplicación.
Configura logs con formato estructurado y niveles apropiados.
"""
import logging
import logging.handlers
import os
from datetime import datetime

# Crear directorio de logs si no existe
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Nombre del archivo de log con timestamp
LOG_FILE = os.path.join(LOG_DIR, f"api_{datetime.now().strftime('%Y-%m-%d')}.log")

# Formato detallado para los logs
LOG_FORMAT = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def setup_logging():
    """Configura el logging estructurado para toda la aplicación."""
    
    # Logger raíz
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # Handler para archivo (rotando cada 10MB, máximo 10 archivos)
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(LOG_FORMAT)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(LOG_FORMAT)
    
    # Agregar handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    return root_logger


# Loggers específicos para módulos
def get_logger(name: str) -> logging.Logger:
    """Obtiene un logger configurado para un módulo específico."""
    return logging.getLogger(name)
