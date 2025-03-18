"""
Path: src/main.py
"""

from utils.logging.simple_logger import LoggerService
from src.db_operations import SQLAlchemyDatabaseRepository
from src.modbus_connection_manager import ModbusConnectionManager
from src.controllers.data_transfer_controller import DataTransferController
from src.controllers.app_controller import AppController

# Inicialización de dependencias
logger = LoggerService()
connection_manager = ModbusConnectionManager(logger)
repository = SQLAlchemyDatabaseRepository(logger)
data_transfer_controller = DataTransferController(logger, repository)
app_controller = AppController(logger, connection_manager, repository, data_transfer_controller)

def run():
    app_controller.run()
