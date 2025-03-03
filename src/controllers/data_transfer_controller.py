"""
Path: src/controllers/data_transfer_controller.py
Este script se encarga de controlar la transferencia de datos 
entre la base de datos y el servidor PHP.
"""

from src.services.data_transfer_service import (
    transfer_production_log_service,
    transfer_interval_production_service,
    send_data_php_service,
    es_tiempo_cercano_multiplo_cinco_service
)
from utils.logging.dependency_injection import get_logger

logger = get_logger()

def main_transfer_controller():
    """Función principal que controla la transferencia de datos entre 
    la base de datos y el servidor PHP."""
    if es_tiempo_cercano_multiplo_cinco_service():
        logger.info("Iniciando transferencia de datos.")
        transfer_production_log_service()
        transfer_interval_production_service()
        send_data_php_service()
    else:
        logger.info("No es momento de transferir datos. Esperando la próxima verificación.")
