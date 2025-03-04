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
from src.data_transfer import main_transfer

# Inicializar el logger a nivel de módulo
logger = get_logger()

# Variable global para control de ejecución
running = True

def setup_signal_handlers():
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
        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)
        logger.debug("Manejadores de señal SIGINT y SIGTERM configurados")
        return True
    else:
        # En Windows, las señales funcionan de manera diferente
        logger.info("Sistema Windows detectado, no se configuran señales POSIX")
        logger.debug("En Windows, las señales POSIX no están disponibles, usando KeyboardInterrupt")
        return False

def handle_signal(signum, frame):
    """Maneja las señales de terminación del programa."""
    global running
    running = False
    logger.info(f"Señal {signum} recibida. Terminando el bucle principal...")
    logger.debug(f"Manejador de señal invocado: signum={signum}")

def main_loop():
    """Ejecuta el bucle principal del programa."""
    global running
    running = True
    
    # Configurar manejadores de señales según el sistema operativo
    setup_signal_handlers()
    

    try:
        logger.debug("Iniciando bucle principal")
        while running:
            execute_main_operations()
    except KeyboardInterrupt:
        handle_keyboard_interrupt()

def execute_main_operations():
    """Ejecuta las operaciones principales del bucle."""
    logger.info("Ejecutando iteración del bucle principal.")
    main_transfer()
    process_modbus_operations()
    time.sleep(1)
    limpiar_pantalla()

def handle_keyboard_interrupt():
    """Maneja la interrupción de teclado (Ctrl+C)."""
    global running
    logger.info("Interrupción de teclado (Ctrl+C) recibida. Terminando el bucle principal...")
    logger.debug("Excepción KeyboardInterrupt capturada en main_loop")
    running = False

def limpiar_pantalla():
    """
    Limpia la consola de comandos según el sistema operativo.
    """
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
