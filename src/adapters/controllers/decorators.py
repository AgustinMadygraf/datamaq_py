"""
Decoradores para logging y manejo centralizado de errores en adaptadores/controladores.
"""
import functools
from src.crosscutting.logging.dependency_injection import get_logger

logger = get_logger()

def log_and_handle_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.debug(f"Entrando en {func.__name__}")
            result = func(*args, **kwargs)
            logger.debug(f"Saliendo de {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Error en {func.__name__}: {e}")
            raise
    return wrapper
