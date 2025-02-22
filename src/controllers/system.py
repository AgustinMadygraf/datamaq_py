"""
Path: src/core/system.py
Este módulo se encarga de ejecutar el bucle principal del programa.
"""

import time
import signal
from src.logs.config_logger import configurar_logging
from src.controllers.modbus_processor import process_modbus_operations
from src.data_transfer import MainTransfer
from src.controller import limpiar_pantalla

logger = configurar_logging()

def main_loop():
    "Ejecuta el bucle principal del programa."
    global running
    running = True
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    time.sleep(5)

    while running:
        logger.info("Ejecutando iteración del bucle principal.")
        MainTransfer()
        process_modbus_operations()
        time.sleep(1)
        limpiar_pantalla()

def handle_signal(signum, frame):
    "Maneja las señales de terminación del programa."
    global running
    running = False
    logger.info("Señal de terminación recibida. Terminando el bucle principal...")
