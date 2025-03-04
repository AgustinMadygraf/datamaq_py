"""
Path: src/core/system.py
Este módulo se encarga de ejecutar el bucle principal del programa.
"""

import os
import time
import signal
import platform
from utils.logging.dependency_injection import get_logger
from src.controllers.modbus_processor import process_modbus_operations
from src.controllers.data_transfer_controller import main_transfer_controller

# Inicializar el logger a nivel de módulo
logger = get_logger()


def setup_signal_handlers(running):
    """
    Configura los manejadores de señales de forma compatible con el sistema operativo.
    En sistemas Unix, configura SIGINT y SIGTERM.
    En Windows, no se configuran señales (se maneja con excepciones).
    """
    current_os = platform.system()
    logger.info(f"Sistema operativo detectado: {current_os}")

    if current_os != "Windows":
        # En sistemas Unix/Linux/MacOS
        logger.info("Configurando manejadores de señales para sistema Unix")
        signal.signal(signal.SIGINT, lambda signum, frame: handle_signal(signum, frame, running))
        signal.signal(signal.SIGTERM, lambda signum, frame: handle_signal(signum, frame, running))
        logger.debug("Manejadores de señal SIGINT y SIGTERM configurados")
        return True
    else:
        # En Windows, las señales funcionan de manera diferente
        logger.info("Sistema Windows detectado, no se configuran señales POSIX")
        logger.debug("En Windows, las señales POSIX no están disponibles, usando KeyboardInterrupt")
        return False

def handle_signal(signum, _, running):
    """Maneja las señales de terminación del programa."""
    running[0] = False
    logger.info(f"Señal {signum} recibida. Terminando el bucle principal...")
    logger.debug(f"Manejador de señal invocado: signum={signum}")

def main_loop():
    """Ejecuta el bucle principal del programa."""
    running = [True]

    # Configurar manejadores de señales según el sistema operativo
    setup_signal_handlers(running)

    try:
        logger.debug("Iniciando bucle principal")
        time.sleep(4)
        while running[0]:
            execute_main_operations()
    except KeyboardInterrupt:
        handle_keyboard_interrupt()
def execute_main_operations():
    """Ejecuta las operaciones principales del bucle."""
    logger.info("Ejecutando iteración del bucle principal.")
    process_modbus_operations()
    print("")
    main_transfer_controller()
    time.sleep(1)
    limpiar_pantalla()


def handle_keyboard_interrupt():
    "Maneja la interrupción de teclado (Ctrl+C) y finaliza el bucle principal."
    logger.info("Interrupción de teclado (Ctrl+C) recibida. Terminando el bucle principal...")
    logger.debug("Excepción KeyboardInterrupt capturada en main_loop")

def limpiar_pantalla():
    """
    Limpia la consola de comandos según el sistema operativo.
    """
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
