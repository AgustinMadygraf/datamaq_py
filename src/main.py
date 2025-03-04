"""
Path: src/main.py
Encapsula la lógica de inicialización y ejecución de la aplicación,
procesando operaciones Modbus continuamente.
"""

import sys
import platform
from utils.logging.dependency_injection import get_logger, enable_verbose_debug
from utils.logging.error_manager import init_error_manager, critical_error
from src.system import SystemController

class MainApplication:
    " Clase principal de la aplicación. "
    def __init__(self, controller=None):
        """
        Inicializa la aplicación.
        Args:
            controller: Instancia de SystemController o similar. 
            Si no se proporciona, se crea uno por defecto.
        """
        self.logger = get_logger()
        self.controller = controller if controller else SystemController()

    def initialize(self):
        """Realiza la configuración inicial de la aplicación."""
        self.logger.info('Iniciando aplicación "DataMaq"')

        # Activar modo debug verbose si se pasa el argumento en la línea de comandos.
        if "--verbose" in sys.argv:
            enable_verbose_debug(True)
            self.logger.debug("Modo debug verbose activado por argumento de línea de comandos")

        # Registrar información del sistema.
        self.logger.debug(f"Sistema operativo: {platform.system()} {platform.release()}")
        self.logger.debug(f"Versión Python: {platform.python_version()}")

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
