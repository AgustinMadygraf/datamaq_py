"""
Decoradores reutilizables para manejo de errores y logging.
"""
import functools
import logging

def handle_errors(logger=None):
    """Decorador para capturar y loguear excepciones en funciones críticas."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log = logger
            # Si el logger no se pasa, buscar en self.logger si es método de instancia
            if log is None and args and hasattr(args[0], 'logger'):
                log = getattr(args[0], 'logger')
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log:
                    log.error(f"Error en {func.__name__}: {e}")
                else:
                    logging.error(f"Error en {func.__name__}: {e}")
                raise
        return wrapper
    return decorator


def log_execution(logger=None):
    """Decorador para loguear entrada y salida de funciones."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log = logger
            if log is None and args and hasattr(args[0], 'logger'):
                log = getattr(args[0], 'logger')
            if log:
                log.info(f"Entrando a {func.__name__}")
            result = func(*args, **kwargs)
            if log:
                log.info(f"Saliendo de {func.__name__}")
            return result
        return wrapper
    return decorator
