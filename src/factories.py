"""
Fábricas centralizadas para la creación de dependencias principales.
"""
from src.db_operations import SQLAlchemyDatabaseRepository
from src.modbus_processor import ModbusDevice, ModbusConnectionManager
from src.utils.logging.dependency_injection import get_logger
from src.data_transfer_controller import DataTransferController


def create_repository():
    """Crea una instancia del repositorio de base de datos."""
    return SQLAlchemyDatabaseRepository()


def create_modbus_device():
    """Crea una instancia de ModbusDevice con conexión detectada automáticamente."""
    logger = get_logger()
    connection_manager = ModbusConnectionManager(logger)
    instrument = connection_manager.establish_connection()
    return ModbusDevice(instrument, logger)


def create_data_transfer_controller():
    """Crea una instancia de DataTransferController con sus dependencias inyectadas."""
    logger = get_logger()
    repo = create_repository()
    return DataTransferController(logger, repo)
