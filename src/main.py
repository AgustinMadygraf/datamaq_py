"""
Path: src/main.py
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
            # Importar interfaces y caso de uso
            from use_cases.process_modbus_operations import ProcessModbusOperationsUseCase, IModbusGateway, IDatabaseGateway
            from src.modbus_processor import ModbusConnectionManager, ModbusDevice, ModbusConnectionError

            # Adaptador concreto para ModbusGateway
            class ModbusGateway(IModbusGateway):
                def __init__(self, logger):
                    self.connection_manager = ModbusConnectionManager(logger)
                    try:
                        self.instrument = self.connection_manager.establish_connection()
                    except ModbusConnectionError as e:
                        logger.error(f"Error de conexión Modbus: {e}")
                        self.instrument = None
                    self.logger = logger
                def read_digital_input(self, address: int):
                    if self.instrument:
                        device = ModbusDevice(self.instrument, self.logger)
                        return device.read_digital_input(address)
                    return None
                def read_register(self, register: int, functioncode: int = 3):
                    if self.instrument:
                        device = ModbusDevice(self.instrument, self.logger)
                        return device.read_register(register, functioncode=functioncode)
                    return None

            class DatabaseGateway(IDatabaseGateway):
                def __init__(self, repository):
                    self.repository = repository
                def actualizar_registro(self, query, params):
                    self.repository.actualizar_registro(query, params)

            modbus_gateway = ModbusGateway(self.logger)
            db_gateway = DatabaseGateway(repo)
            modbus_use_case = ProcessModbusOperationsUseCase(modbus_gateway, db_gateway, self.logger)
            self.controller = AppController(logger=self.logger, repository=repo, modbus_use_case=modbus_use_case)

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
