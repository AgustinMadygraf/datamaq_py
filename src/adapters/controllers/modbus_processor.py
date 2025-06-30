"""
Procesador de operaciones Modbus siguiendo principios SOLID y POO.
"""

import minimalmodbus
import serial.tools.list_ports

from src.domain.entities import IDatabaseRepository
from src.infrastructure.db.sqlalchemy_repository import SQLAlchemyDatabaseRepository, DatabaseUpdateError
from utils.logging.dependency_injection import get_logger

logger = get_logger()


class ModbusConnectionError(Exception):
    pass


class ModbusReadError(Exception):
    pass


class ModbusConnectionManager:
    def __init__(self, log, device_address=1):
        self.logger = log
        self.device_address = device_address

    def detect_com_port(self, device_description: str):
        available_ports = list(serial.tools.list_ports.comports())
        for port, desc, _ in available_ports:
            if device_description in desc:
                return port
        return None

    def establish_connection(self):
        device_description = "DigiRail Connect"
        com_port = self.detect_com_port(device_description)
        if com_port:
            self.logger.info(f"Puerto {device_description} detectado: {com_port}")
        else:
            device_description = "USB-SERIAL CH340"
            com_port = self.detect_com_port(device_description)
            if com_port:
                self.logger.info(f"Puerto detectado: {com_port}")
            else:
                error_msg = "No se detectaron puertos COM para el dispositivo."
                self.logger.error(error_msg)
                raise ModbusConnectionError(error_msg)


def process_modbus_operations(repository: IDatabaseRepository = None):
    """
    Función de orquestación que inicializa la conexión, procesa las operaciones
    y actualiza la base de datos.
    """
    connection_manager = ModbusConnectionManager(logger)
    try:
        instrument = connection_manager.establish_connection()
    except ModbusConnectionError as e:
        logger.error(f"Error de conexión Modbus: {e}")
        return

    # Aquí deberías definir ModbusDevice y ModbusProcessor o importarlos si ya existen
    # modbus_device = ModbusDevice(instrument, logger)
    # if repository is None:
    #     repository = SQLAlchemyDatabaseRepository()
    # processor = ModbusProcessor(modbus_device, repository, logger)
    # try:
    #     processor.process()
    # except (ModbusReadError, DatabaseUpdateError) as e:
    #     logger.error(f"Error durante el procesamiento de operaciones Modbus: {e}")
    pass