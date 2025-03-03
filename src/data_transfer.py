"""
Path: src/data_transfer.py
Este módulo actúa como la capa de vista y delega la transferencia de datos al controlador.
"""

import subprocess
from utils.logging.dependency_injection import get_logger
from src.controllers.data_transfer_controller import main_transfer_controller

logger = get_logger()

def main_transfer():
    "Función principal que inicia el proceso de transferencia de datos."
    main_transfer_controller()

def send_data_php(): # ver s ino es codigo muerto
    "Envía los datos a través de un script PHP."
    php_interpreter = "C://AppServ//php7//php.exe"
    php_script = "C://AppServ//www//DataMaq//includes//SendData_python.php"
    result = subprocess.run([php_interpreter, php_script], capture_output=True, text=True, shell=True, check=True)
    if result.returncode == 0:
        logger.info("Script PHP ejecutado exitosamente. Salida:")
        logger.info(result.stdout)
    else:
        logger.error("Error al ejecutar el script PHP. Código de salida: %s", result.returncode)
        logger.error(result.stderr)
