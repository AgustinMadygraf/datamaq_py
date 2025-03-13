"""
Path: src/main.py
Encapsula la lógica de inicialización y ejecución de la aplicación,
procesando operaciones Modbus continuamente.
"""

import sys
import platform
from utils.logging.simple_logger import get_logger
from src.controllers.app_controller import AppController

class MainApplication:
    " Clase principal de la aplicación. "
    def __init__(self, controller=None):
        self.logger = get_logger()
        self.controller = controller if controller else AppController()

    def initialize(self):
        """Realiza la configuración inicial de la aplicación."""
        self.logger.info('Iniciando aplicación "DataMaq"')

        # Registrar información del sistema.
        self.logger.info(f"Sistema operativo: {platform.system()} {platform.release()}")
        self.logger.info(f"Versión Python: {platform.python_version()}")
        self.logger.debug("Este mensaje DEBUG solo debería verse en modo verbose")

    def run(self):
        """Ejecuta el ciclo principal de la aplicación y gestiona el flujo de ejecución."""
        try:
            self.initialize()
            self.controller.run()
            self.logger.info("Aplicación finalizada correctamente")
            sys.exit(0)
        except (OSError, RuntimeError) as e:
            self.logger.error(f"Error de sistema: {e}")
            sys.exit(1)
        except (ValueError, TypeError) as e:
            self.logger.error(f"Error de programación: {e}")
            sys.exit(1)
