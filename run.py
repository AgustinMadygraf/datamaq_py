"""
Path: run.py
Este script se ocupa de ejecutar el bucle principal del programa,
procesando operaciones Modbus continuamente.
"""

import sys
import platform
from utils.logging.dependency_injection import get_logger, log_debug, enable_verbose_debug
from utils.logging.error_manager import init_error_manager, critical_error
from src.controllers.system import main_loop


if __name__ == "__main__":
    try:
        # Configurar logging
        logger = get_logger()
        logger.info('Iniciando aplicación "DataMaq" ')
        
        # Activar modo debug verbose en entorno de desarrollo
        if "--verbose" in sys.argv:
            enable_verbose_debug(True)
            log_debug("Modo debug verbose activado por argumento de línea de comandos")
        
        # Registrar información del sistema
        log_debug(f"Sistema operativo: {platform.system()} {platform.release()}")
        log_debug(f"Versión Python: {platform.python_version()}")

        # Inicializar el gestor de errores con el logger
        init_error_manager(logger)
        logger.info("Gestor de errores inicializado")
        main_loop()
        logger.info("Aplicación finalizada correctamente")
        sys.exit(0)

    except (OSError, RuntimeError) as e:
        # Usar el gestor de errores para manejar la excepción
        critical_error(e, {"context": "main", "fase": "inicialización"})
        sys.exit(1)
    except (ValueError, TypeError) as e:  # Capturar excepciones específicas
        # Usar el gestor de errores para manejar excepciones desconocidas
        critical_error(e, {"context": "main", "tipo": "excepción específica", "detalle": str(e)})
        sys.exit(1)
