from src.utils.logging.decorators import handle_errors, log_execution
"""
Path: src/app_controller.py
Este módulo se encarga de controlar el ciclo principal de la aplicación,
procesando operaciones Modbus y transferencias de datos.
"""

import time
import signal
import platform
from src.utils.logging.dependency_injection import get_logger
from src.modbus_processor import process_modbus_operations
from src.data_transfer_controller import main_transfer_controller
from src.infrastructure.CLI.app_view import clear_screen

class AppController:
    """Controlador principal que gestiona el ciclo de la aplicación."""
    def __init__(self, logger=None, repository=None):
        self.logger = logger or get_logger()
        self.repository = repository
        self.running = True

    def setup_signal_handlers(self):
        "Configura los manejadores de señales para el sistema operativo actual."
        current_os = platform.system()
        self.logger.info(f"Sistema operativo detectado: {current_os}")
        self.logger.debug(f"Sistema operativo detectado: {current_os}") # para testerar el nivel de debug
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

    @handle_errors()
    @log_execution()
    def execute_main_operations(self):
        "Se encarga de ejecutar las operaciones principales del programa."
        self.logger.debug(
            "Ejecutando iteración del bucle principal.",
            extra={"event": "main_loop_iteration", "controller": "AppController"}
        )
        repo = self.repository
        if repo is None:
            from src.infrastructure.factories import create_repository
            repo = create_repository()
        self.logger.info(
            "Procesando operaciones Modbus.",
            extra={"event": "process_modbus", "repository": type(repo).__name__}
        )
        process_modbus_operations(repository=repo)
        print("")  # Se puede remover o delegar a la vista según convenga
        self.logger.info(
            "Ejecutando transferencia de datos.",
            extra={"event": "data_transfer", "controller": "AppController"}
        )
        main_transfer_controller()
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
