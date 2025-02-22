"""
Path: run.py
Este script se ocupa de ejecutar el bucle principal del programa,
procesando operaciones Modbus continuamente.
"""

from src.logs.config_logger import configurar_logging
from src.controllers.system import main_loop

# Configurar logging
logger = configurar_logging()

if __name__ == "__main__":
    main_loop()
