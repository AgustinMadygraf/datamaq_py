"""
Path: src/main.py
Encapsula la lógica de inicialización y ejecución de la aplicación,
procesando operaciones Modbus continuamente.
"""

import sys
import platform
from src.utils.logging.logger_configurator import set_debug_verbose
from src.utils.logging.dependency_injection import get_logger
from src.utils.logging.error_manager import init_error_manager, critical_error
from src.infrastructure.factories import create_repository
from src.app_controller import AppController

class MainApplication:
    " Clase principal de la aplicación. "
    def __init__(self, controller=None):
        # Activar modo debug verbose si se pasa el argumento en la línea de comandos
        # NOTA: Esto debe hacerse ANTES de obtener el logger
        if "--verbose" in sys.argv:
            set_debug_verbose(True)
            print("Modo debug verbose activado por argumento de línea de comandos")

        self.logger = get_logger()
        if controller:
            self.controller = controller
        else:
            repo = create_repository()
            self.controller = AppController(repository=repo)

    def initialize(self):
        """Realiza la configuración inicial de la aplicación."""
        self.logger.info('Iniciando aplicación "DataMaq"')

        # Registrar información del sistema.
        self.logger.info(f"Sistema operativo: {platform.system()} {platform.release()}")
        self.logger.info(f"Versión Python: {platform.python_version()}")
        self.logger.debug("Este mensaje DEBUG solo debería verse en modo verbose")

        # Inicializar el gestor de errores.
        init_error_manager(self.logger)
        self.logger.info("Gestor de errores inicializado")

    def run(self):
        """Ejecuta el ciclo principal de la aplicación y gestiona el flujo de ejecución."""
        try:
            self.initialize()
            self.controller.run()
            self.logger.info("Aplicación finalizada correctamente")
            sys.exit(0)
        except (OSError, RuntimeError) as e:
            critical_error(e, {"context": "main", "fase": "inicialización"})
            sys.exit(1)
        except (ValueError, TypeError) as e:
            critical_error(
                e,
                {
                    "context": "main", 
                    "tipo": "excepción específica", 
                    "detalle": str(e)
                }
            )
            sys.exit(1)
