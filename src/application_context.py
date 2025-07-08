"""
ApplicationContext: Gestión centralizada del ciclo de vida de recursos (DB, Modbus, logger).
"""
from src.db_operations import SQLAlchemyDatabaseRepository
from src.modbus_processor import ModbusDevice, ModbusConnectionManager
from src.utils.logging.dependency_injection import get_logger

class ApplicationContext:
    def __init__(self):
        self.logger = get_logger()
        self.repository = None
        self.modbus_device = None
        self._resources = []

    def __enter__(self):
        self.repository = SQLAlchemyDatabaseRepository()
        self._resources.append(self.repository)
        connection_manager = ModbusConnectionManager(self.logger)
        instrument = connection_manager.establish_connection()
        self.modbus_device = ModbusDevice(instrument, self.logger)
        self._resources.append(self.modbus_device)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cerrar recursos en orden inverso
        for res in reversed(self._resources):
            if hasattr(res, 'cerrar_conexion'):
                try:
                    res.cerrar_conexion()
                except Exception:
                    pass
        self._resources.clear()
