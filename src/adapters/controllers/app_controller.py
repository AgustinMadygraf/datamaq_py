"""
Controlador principal que gestiona el ciclo de la aplicación.
"""
import time
import signal
import platform
from utils.logging.dependency_injection import get_logger
from src.adapters.controllers.modbus_processor import process_modbus_operations
from src.application.use_cases import main_transfer_controller
from src.adapters.controllers.app_view import clear_screen

class AppController:
    def __init__(self, logger=None):
        self.logger = logger or get_logger()
        self.running = True

    def setup_signal_handlers(self):
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
        self.logger.info(f"Señal {signum} recibida. Terminando el bucle principal...")
        self.running = False

    def execute_main_operations(self):
        self.logger.debug("Ejecutando iteración del bucle principal.")
        def obtener_datos(consulta):
            # Implementar o delegar a la infraestructura real
            return []
        def insertar_datos(datos, consulta_insercion, campos):
            # Implementar o delegar a la infraestructura real
            pass
        try:
            process_modbus_operations()
            print("")
            main_transfer_controller(self.logger, obtener_datos, insertar_datos)
        except Exception as e:
            self.logger.error(f"Error en operaciones principales: {e}")
        time.sleep(1)
        clear_screen()

    def run(self):
        self.setup_signal_handlers()
        try:
            self.logger.info("Iniciando bucle principal")
            input("Presione Enter para comenzar el bucle principal...")
            while self.running:
                self.execute_main_operations()
        except KeyboardInterrupt:
            self.logger.info("Interrupción (Ctrl+C) recibida. Terminando el bucle principal...")