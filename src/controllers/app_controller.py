"""
Path: src/controllers/app_controller.py
Este módulo se encarga de controlar el ciclo principal de la aplicación,
procesando operaciones Modbus y transferencias de datos.
"""

import time
import signal
import platform
from utils.logging.dependency_injection import get_logger
from src.modbus_connection_manager import ModbusConnectionManager, ModbusConnectionError
from src.views.app_view import clear_screen
from src.controllers.data_transfer_controller import DataTransferController

from src.db_operations import SQLAlchemyDatabaseRepository, DatabaseUpdateError
from src.modbus_processor import ModbusDevice, ModbusProcessor, ModbusReadError, ModbusDatabaseUpdater

logger = get_logger()

class AppController:
    """Controlador principal que gestiona el ciclo de la aplicación."""
    def __init__(self, logger=None):
        self.logger = logger or get_logger()
        self.running = True

    def setup_signal_handlers(self):
        "Configura los manejadores de señales para el sistema operativo actual."
        current_os = platform.system()
        self.logger.info(f"Sistema operativo detectado: {current_os}")
        self.logger.debug(f"Sistema operativo detectado: {current_os}")
        if current_os != "Windows":
            self.logger.info("Configurando manejadores de señales para sistema Unix")
            signal.signal(signal.SIGINT, self.handle_signal)
            signal.signal(signal.SIGTERM, self.handle_signal)
        else:
            self.logger.info("Sistema Windows detectado, se manejará mediante KeyboardInterrupt")

    def handle_signal(self, signum, _frame):
        " Manejador de señales para SIGINT y SIG"
        self.logger.info(f"Señal {signum} recibida. Terminando el bucle principal...")
        self.running = False

    def execute_main_operations(self):
        "Se encarga de ejecutar las operaciones principales del programa."
        self.logger.debug("Ejecutando iteración del bucle principal.")
        connection_manager = ModbusConnectionManager(logger)
        try:
            instrument = connection_manager.establish_connection()
        except ModbusConnectionError as e:
            logger.error(f"Error de conexión Modbus: {e}")
            return

        modbus_device = ModbusDevice(instrument, logger)
        repository = SQLAlchemyDatabaseRepository()
        db_updater = ModbusDatabaseUpdater(repository, logger)
        processor = ModbusProcessor(modbus_device, db_updater, logger)
        try:
            processor.process()
        except (ModbusReadError, DatabaseUpdateError) as e:
            logger.error(f"Error durante el procesamiento de operaciones Modbus: {e}")

        print("")  # Se puede remover o delegar a la vista según convenga
        controller = DataTransferController(logger)
        controller.run_transfer()
        time.sleep(1)
        clear_screen()  # se utiliza la función de la vista

    def run(self):
        "Ejecuta el ciclo principal de la aplicación."
        self.setup_signal_handlers()
        try:
            self.logger.info("Iniciando bucle principal")
            input("Presione Enter para comenzar el bucle principal...")
            while self.running:
                self.execute_main_operations()
        except KeyboardInterrupt:
            self.logger.info("Interrupción (Ctrl+C) recibida. Terminando el bucle principal...")
