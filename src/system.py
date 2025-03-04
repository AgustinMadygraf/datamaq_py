"""
Path: src/controllers/system.py
Este módulo se encarga de ejecutar el bucle principal del programa.
"""

import os
import time
import signal
import platform
from utils.logging.dependency_injection import get_logger
from src.modbus_processor import process_modbus_operations
from src.data_transfer_controller import main_transfer_controller

class SystemController:
    " Controlador del sistema que ejecuta el bucle principal del programa. "
    def __init__(self, logger=None):
        """
        Inicializa el controlador del sistema.
        Args:
            logger: Objeto logger (se inyecta para facilitar pruebas 
            y separación de responsabilidades).
        """
        self.logger = logger or get_logger()
        self.running = True

    def setup_signal_handlers(self):
        """
        Configura los manejadores de señales de forma compatible con el sistema operativo.
        En sistemas Unix, configura SIGINT y SIGTERM.
        En Windows, se asume que se manejará mediante KeyboardInterrupt.
        """
        current_os = platform.system()
        self.logger.info(f"Sistema operativo detectado: {current_os}")

        if current_os != "Windows":
            self.logger.info("Configurando manejadores de señales para sistema Unix")
            signal.signal(signal.SIGINT, self.handle_signal)
            signal.signal(signal.SIGTERM, self.handle_signal)
            self.logger.debug("Manejadores de señal SIGINT y SIGTERM configurados")
        else:
            self.logger.info("Sistema Windows detectado, no se configuran señales POSIX")
            self.logger.debug("En Windows, se manejará la interrupción mediante KeyboardInterrupt")

    def handle_signal(self, signum, _frame):
        """Maneja las señales de terminación del programa."""
        self.logger.info(f"Señal {signum} recibida. Terminando el bucle principal...")
        self.logger.debug(f"Manejador de señal invocado: signum={signum}")
        self.running = False

    def execute_main_operations(self):
        """
        Ejecuta las operaciones principales del bucle:
        - Procesa operaciones Modbus.
        - Ejecuta la transferencia de datos.
        - Realiza una pausa breve y limpia la pantalla.
        """
        self.logger.info("Ejecutando iteración del bucle principal.")
        process_modbus_operations()
        print("")
        main_transfer_controller()
        time.sleep(1)
        self.clear_screen()

    def clear_screen(self):
        """Limpia la consola de comandos según el sistema operativo."""
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')

    def run(self):
        """
        Ejecuta el bucle principal del programa,
        configurando previamente los manejadores de señales.
        """
        self.setup_signal_handlers()
        try:
            self.logger.debug("Iniciando bucle principal")
            time.sleep(4)  # Pausa inicial si se requiere
            while self.running:
                self.execute_main_operations()
        except KeyboardInterrupt:
            self.logger.info(
                "Interrupción de teclado (Ctrl+C) recibida. Terminando el bucle principal..."
            )
            self.logger.debug("Excepción KeyboardInterrupt capturada en main_loop")
