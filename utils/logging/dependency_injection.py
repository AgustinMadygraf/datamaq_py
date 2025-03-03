"""
Path: utils/logging/dependency_injection.py
Contenedor de dependencias para inyección de dependencias.
Facilita el acceso a servicios centralizados como el logger.
"""

import os
import logging
from utils.logging.logger_configurator import (
    LoggerConfigurator, 
    get_logger as get_base_logger,
    log_debug as log_debug_base,
    set_debug_verbose,
    get_debug_verbose
)
from utils.logging.logger_factory import LoggerFactory
from utils.logging.info_error_filter import InfoErrorFilter
from utils.logging.exclude_http_logs_filter import ExcludeHTTPLogsFilter

# Definir la ruta al archivo JSON
JSON_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'utils',
    'logging',
    'logging.json'
)

# Crear una instancia del configurador
configurator = LoggerConfigurator()

# Registrar filtros para el caso de configuración manual
configurator.register_filter(InfoErrorFilter)
configurator.register_filter(ExcludeHTTPLogsFilter)

# Configurar el logger - primero intentar desde JSON, fallback a configuración manual
if os.path.exists(JSON_CONFIG_PATH):
    logger = configurator.configure_from_json(JSON_CONFIG_PATH)
else:
    logger = configurator.configure()

def get_logger(name: str = "datamaq") -> logging.Logger:
    """
    Retorna un logger configurado.
    Si se solicita el logger predeterminado, devuelve el logger principal.
    De lo contrario, busca o crea un logger con el nombre especificado.
    
    Args:
        name: Nombre del logger a obtener
        
    Returns:
        Logger configurado
    """
    if name == "datamaq" or name == "default":
        return LoggerFactory.get_default_logger()
    return LoggerFactory.get_logger(name)

def log_debug(message: str, *args, **kwargs) -> None:
    """
    Función centralizada para registrar mensajes de debug.
    Utiliza la funcionalidad de log_debug con información adicional
    cuando el modo verbose está activado.
    
    Args:
        message: Mensaje a registrar
        *args: Argumentos posicionales para el mensaje
        **kwargs: Argumentos con nombre para la llamada al logger
    """
    log_debug_base(message, *args, **kwargs)

def enable_verbose_debug(enabled: bool = True) -> None:
    """
    Activa o desactiva el modo verbose para mensajes de debug.
    Función de conveniencia para set_debug_verbose.
    
    Args:
        enabled: True para activar, False para desactivar
    """
    set_debug_verbose(enabled)
    logger = get_logger("dependency_injection")
    mode = "activado" if enabled else "desactivado"
    logger.info(f"Modo debug verbose {mode} desde dependency_injection")

def is_verbose_debug_enabled() -> bool:
    """
    Verifica si el modo verbose de debug está activado.
    Función de conveniencia para get_debug_verbose.
    
    Returns:
        True si está activado, False si no
    """
    return get_debug_verbose()
