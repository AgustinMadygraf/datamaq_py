"""
Path: src/controllers/data_transfer_controller.py
Este script se encarga de controlar la transferencia de datos entre la base de datos y el servidor PHP.
"""

from src.services.data_transfer_service import (
    transfer_production_log_service,
    transfer_interval_production_service,
    send_data_php_service,
    es_tiempo_cercano_multiplo_cinco_service
)
from src.logs.config_logger import configurar_logging

logger = configurar_logging()

def main_transfer_controller():
    if es_tiempo_cercano_multiplo_cinco_service():
        logger.info("Iniciando transferencia de datos.")
        transfer_production_log_service()
        transfer_interval_production_service()
        send_data_php_service()
    else:
        logger.info("No es momento de transferir datos. Esperando la próxima verificación.")
