#src/logs/config_logger.py
import logging
from logging.handlers import RotatingFileHandler


class DebugAndAboveFilter(logging.Filter):
    """
    Filtro de registro personalizado para excluir mensajes de nivel INFO.

    Este filtro se puede aplicar a un manejador de registros (handler) para excluir
    los registros de nivel INFO. Es útil cuando se desea registrar mensajes de nivel
    DEBUG y superiores, pero omitir los de nivel INFO.

    Métodos:
        filter(record): Determina si el registro dado debe ser registrado o no.
    """
    def filter(self, record):
        # Excluir los registros de nivel INFO del archivo de log
        return record.levelno != logging.INFO

def create_handler(handler_class, level, format, **kwargs):
    """
    Crea y configura un manejador de registros (handler) para el sistema de logging.

    Esta función es una fábrica que crea y configura un manejador de registros.
    Configura el nivel de registro, el formato y cualquier otro parámetro relevante
    para el manejador.

    Args:
        handler_class (logging.Handler): La clase del manejador de registros a crear.
        level (int): El nivel de registro para el manejador.
        format (str): El formato de los mensajes de registro.
        **kwargs: Argumentos adicionales específicos del manejador.

    Returns:
        logging.Handler: Un manejador de registros configurado.
    """
    handler = handler_class(**kwargs)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(format))
    return handler

def configurar_logging():
    """
    Configura el sistema de logging global de la aplicación.

    Esta función configura el sistema de logging con dos manejadores: uno para
    escribir en un archivo con rotación y otro para la salida de consola.
    Se establece un formato específico para los mensajes y se filtran los mensajes
    de nivel INFO del archivo de registro.

    Returns:
        logging.Logger: El objeto logger configurado para la aplicación.
    """
    logger = logging.getLogger()
    if logger.hasHandlers():
        return logger

    log_format = '%(asctime)s - %(levelname)s - %(module)s - %(filename)s:%(lineno)d: %(message)s'
    log_file = 'src/logs/sistema.log'
    max_bytes = 10485760  # 10MB
    backup_count = 5

    file_handler = create_handler(
        RotatingFileHandler, 
        logging.DEBUG, 
        log_format, 
        filename=log_file, 
        maxBytes=max_bytes, 
        backupCount=backup_count
    )
    file_handler.addFilter(DebugAndAboveFilter())  # Aplicar el filtro

    console_handler = create_handler(
        logging.StreamHandler, 
        logging.INFO, 
        log_format
    )

    logger.setLevel(logging.DEBUG)  # Nivel más bajo para capturar todos los mensajes
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Configurar el logger con un nivel específico
configurar_logging()
