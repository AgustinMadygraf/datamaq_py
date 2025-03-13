"""
Path: src/container.py
"""

from utils.logging.simple_logger import get_logger
from src.db_operations import SQLAlchemyDatabaseRepository
from src.modbus_connection_manager import ModbusConnectionManager
from src.controllers.data_transfer_controller import DataTransferController
from src.controllers.app_controller import AppController

# Inicialización de dependencias
logger = get_logger()
connection_manager = ModbusConnectionManager(logger)
repository = SQLAlchemyDatabaseRepository(logger)
data_transfer_controller = DataTransferController(logger)

# Creación del controlador principal con dependencias inyectadas
app_controller = AppController(logger, connection_manager, repository, data_transfer_controller)

def run():
    app_controller.run()
