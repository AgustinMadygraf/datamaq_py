"""
Procesador de operaciones Modbus siguiendo principios SOLID y POO.
"""

import minimalmodbus  # type: ignore
import serial.tools.list_ports  # type: ignore

from src.domain.ports.database_repository import IDatabaseRepository
from src.infrastructure.db.sqlalchemy_repository import SQLAlchemyDatabaseRepository, DatabaseUpdateError
from src.crosscutting.logging.dependency_injection import get_logger

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
            instrument = minimalmodbus.Instrument(com_port, self.device_address)
            # Configuración adicional si es necesario
            # instrument.serial.baudrate = 9600
            # instrument.serial.timeout = 1
            return instrument
        else:
            device_description = "USB-SERIAL CH340"
            com_port = self.detect_com_port(device_description)
            if com_port:
                self.logger.info(f"Puerto detectado: {com_port}")
                instrument = minimalmodbus.Instrument(com_port, self.device_address)
                return instrument
            else:
                error_msg = "No se detectaron puertos COM para el dispositivo."
                self.logger.error(error_msg)
                raise ModbusConnectionError(error_msg)


def process_modbus_operations(repository: IDatabaseRepository):
    """
    Lee registros Modbus y almacena los valores en la base de datos a través del repositorio.
    """
    if repository is None:
        logger.error("Repositorio no proporcionado a process_modbus_operations. Abortando operación.")
        return
    try:
        connection_manager = ModbusConnectionManager(logger)
        instrument = connection_manager.establish_connection()
        registros = [1, 2, 3, 4]  # IDs de registros a leer
        for reg in registros:
            try:
                valor = instrument.read_register(reg, 0)
                repository.actualizar_registro(
                    "INSERT INTO registros_modbus (registro, valor) VALUES (:registro, :valor) ON DUPLICATE KEY UPDATE valor = VALUES(valor)",
                    {"registro": f"HR_{reg}", "valor": valor}
                )
                logger.info(f"Registro HR_{reg} leído y almacenado: {valor}")
            except Exception as e:
                logger.error(f"Error leyendo registro {reg}: {e}")
        repository.commit()
    except Exception as e:
        logger.error(f"Error en process_modbus_operations: {e}")
        if repository is not None:
            repository.rollback()


def run_modbus_processing(repository: IDatabaseRepository = None):
    """
    Función de orquestación que inicializa la conexión y procesa las operaciones
    """
    connection_manager = ModbusConnectionManager(logger)
    try:
        instrument = connection_manager.establish_connection()
    except ModbusConnectionError as e:
        logger.error(f"Error de conexión Modbus: {e}")
        return

    # Aquí solo se debe llamar a la función interna, sin pasar instrument ni logger
    process_modbus_operations(repository)  # Si es necesario, pero no pasar más argumentos