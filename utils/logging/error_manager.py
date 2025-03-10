"""
Path: utils/logging/error_manager.py
Gestiona los errores críticos de la aplicación.
"""

import sys
import traceback
from typing import Dict, Any, Optional
from utils.logging.simple_logger import get_logger

# Instancia global del gestor de errores
_ERROR_MANAGER_INSTANCE = None

class ErrorManager:
    """
    Clase que gestiona los errores críticos de la aplicación.
    """
    
    def __init__(self, logger=None):
        self.logger = logger or get_logger()
        
    def critical_error(self, exception: Exception, context: Optional[Dict[str, Any]] = None) -> None:
        """
        Registra un error crítico y prepara el sistema para finalizar.
        
        Args:
            exception: La excepción que generó el error
            context: Información adicional sobre el contexto del error
        """
        self.logger.critical(f"ERROR CRÍTICO: {exception}")
        
        # Registrar el traceback completo
        exc_trace = traceback.format_exc()
        self.logger.critical(f"Traceback:\n{exc_trace}")
        
        # Registrar el contexto si está disponible
        if context:
            context_str = ", ".join(f"{k}={v}" for k, v in context.items())
            self.logger.critical(f"Contexto del error: {context_str}")


def get_error_manager() -> ErrorManager:
    """
    Obtiene o crea una instancia del gestor de errores.
    
    Returns:
        Instancia del gestor de errores
    """
    global _ERROR_MANAGER_INSTANCE
    if _ERROR_MANAGER_INSTANCE is None:
        _ERROR_MANAGER_INSTANCE = ErrorManager()
    return _ERROR_MANAGER_INSTANCE


def init_error_manager(logger=None) -> None:
    """
    Inicializa el gestor de errores con un logger específico.
    
    Args:
        logger: Logger que utilizará el gestor de errores
    """
    global _ERROR_MANAGER_INSTANCE
    _ERROR_MANAGER_INSTANCE = ErrorManager(logger)


def critical_error(exception: Exception, context: Optional[Dict[str, Any]] = None) -> None:
    """
    Registra un error crítico a través del gestor de errores.
    
    Args:
        exception: La excepción que generó el error
        context: Información adicional sobre el contexto del error
    """
    get_error_manager().critical_error(exception, context)
