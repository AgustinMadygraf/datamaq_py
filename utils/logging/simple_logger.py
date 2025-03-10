"""
Path: utils/logging/simple_logger.py
Módulo que proporciona un sistema de logging simplificado con soporte para modo verbose.
"""

import sys
import time
import traceback
from datetime import datetime
from typing import Dict, Any, Optional, Union

# Variable global para controlar el modo verbose
_DEBUG_VERBOSE = False

# Diccionario para almacenar una única instancia del logger
_LOGGER_INSTANCE = None

class SimpleLogger:
    """
    Implementación simplificada de logger que muestra mensajes en consola
    y opcionalmente puede guardar logs en archivo.
    """
    
    # Niveles de log
    LEVELS = {
        "DEBUG": 10,
        "INFO": 20,
        "WARNING": 30,
        "ERROR": 40,
        "CRITICAL": 50
    }
    
    # Colores para cada nivel
    COLORS = {
        "DEBUG": "\033[94m",     # Azul
        "INFO": "\033[92m",      # Verde
        "WARNING": "\033[93m",   # Amarillo
        "ERROR": "\033[91m",     # Rojo
        "CRITICAL": "\033[91m\033[1m",  # Rojo brillante
        "RESET": "\033[0m"       # Reset
    }
    
    def __init__(self, name: str = "DataMaq", log_to_file: bool = False, log_file: str = "datamaq.log"):
        self.name = name
        self.log_to_file = log_to_file
        self.log_file = log_file
    
    def _log(self, level: str, message: str, *args, exc_info: bool = False, extra_data: Optional[Dict[str, Any]] = None, **kwargs) -> None:
        """
        Registra un mensaje con el nivel especificado.
        
        Args:
            level: Nivel del log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            message: Mensaje a registrar
            args: Argumentos para formatear el mensaje (usando %)
            exc_info: Si es True, añade información de la excepción
            extra_data: Datos adicionales para el log
            kwargs: Argumentos adicionales (para compatibilidad con otros loggers)
        """
        # Verificar si debemos mostrar mensajes DEBUG
        if level == "DEBUG" and not _DEBUG_VERBOSE:
            return
        
        # Formatear el mensaje si se proporcionaron argumentos
        if args:
            try:
                message = message % args
            except:
                message = f"{message} {args}"
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {level:8s} - {message}"
        
        # Agregar datos extra si existen
        if extra_data:
            log_message += f" | {extra_data}"
        
        # Imprimir en consola con color
        color = self.COLORS.get(level, self.COLORS["RESET"])
        print(f"{color}{log_message}{self.COLORS['RESET']}")
        
        # Añadir información de la excepción si se solicita
        if exc_info:
            exception_info = traceback.format_exc()
            print(f"{color}{exception_info}{self.COLORS['RESET']}")
            
            # También guardar la excepción en el archivo de log
            if self.log_to_file:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"{exception_info}\n")
        
        # Guardar en archivo si está habilitado
        if self.log_to_file:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"{log_message}\n")
    
    def debug(self, message: str, *args, **kwargs) -> None:
        """Registra un mensaje de nivel DEBUG."""
        self._log("DEBUG", message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs) -> None:
        """Registra un mensaje de nivel INFO."""
        self._log("INFO", message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs) -> None:
        """Registra un mensaje de nivel WARNING."""
        self._log("WARNING", message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs) -> None:
        """Registra un mensaje de nivel ERROR."""
        self._log("ERROR", message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs) -> None:
        """Registra un mensaje de nivel CRITICAL."""
        self._log("CRITICAL", message, *args, **kwargs)


def set_debug_verbose(enabled: bool = True) -> None:
    """
    Activa o desactiva el modo verbose para logs de depuración.
    
    Args:
        enabled: True para activar, False para desactivar
    """
    global _DEBUG_VERBOSE
    _DEBUG_VERBOSE = enabled


def is_debug_verbose() -> bool:
    """
    Devuelve si el modo verbose está activo.
    
    Returns:
        True si el modo verbose está activo, False en caso contrario
    """
    return _DEBUG_VERBOSE


def get_logger(name: str = "DataMaq") -> SimpleLogger:
    """
    Obtiene o crea una instancia del logger.
    
    Args:
        name: Nombre del logger
    
    Returns:
        Instancia del logger
    """
    global _LOGGER_INSTANCE
    if _LOGGER_INSTANCE is None:
        _LOGGER_INSTANCE = SimpleLogger(name)
    return _LOGGER_INSTANCE
