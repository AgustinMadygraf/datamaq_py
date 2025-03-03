"""
Path: src/data_transfer.py
Este módulo actúa como la capa de vista y delega la transferencia de datos al controlador.
"""

from utils.logging.dependency_injection import get_logger
from src.controllers.data_transfer_controller import main_transfer_controller

logger = get_logger()

def main_transfer():
    "Función principal que inicia el proceso de transferencia de datos."
    main_transfer_controller()
