"""
Path: src/core/system.py
Este módulo se encarga de ejecutar el bucle principal del programa.
"""

import time
import signal
from utils.logging.dependency_injection import get_logger
from src.controllers.modbus_processor import process_modbus_operations
from src.data_transfer import main_transfer
from src.controller import limpiar_pantalla

# Inicializar el logger a nivel de módulo
logger = get_logger()


def main_loop():
    "Ejecuta el bucle principal del programa."
    global running
    running = True
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    time.sleep(5)

    while running:
        logger.info("Ejecutando iteración del bucle principal.")
        main_transfer()
        process_modbus_operations()
        time.sleep(1)
        limpiar_pantalla()

def handle_signal(signum, frame):
    "Maneja las señales de terminación del programa."
    global running
    running = False
    logger.info("Señal de terminación recibida. Terminando el bucle principal...")
