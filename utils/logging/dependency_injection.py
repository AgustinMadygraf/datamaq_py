"""
Path: utils/logging/dependency_injection.py
Contenedor de dependencias para inyección de dependencias.
Facilita el acceso a servicios centralizados como el logger.
"""

import os
import logging
from utils.logging.logger_configurator import LoggerConfigurator
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
