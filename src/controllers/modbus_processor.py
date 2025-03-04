"""
Path: src/core/modbus_processor.py
Este módulo se encarga de procesar las operaciones Modbus siguiendo principios SOLID y POO.
"""

import minimalmodbus
import serial.tools.list_ports
from src.db_operations import SQLAlchemyDatabaseRepository, DatabaseUpdateError
from utils.logging.dependency_injection import get_logger

logger = get_logger()

# Excepciones específicas
class ModbusConnectionError(Exception):
    """Excepción para errores de conexión con el dispositivo Modbus."""
    pass

class ModbusReadError(Exception):
    """Excepción para errores de lectura del dispositivo Modbus."""
    pass

class ModbusConnectionManager:
    """
    Encapsula la lógica para detectar y establecer una conexión Modbus.
    """
    def __init__(self, log, device_address=1):
        self.logger = log
        self.device_address = device_address

    def detect_com_port(self, device_description: str):
        """
        Busca y retorna el puerto serie que coincide con la descripción del dispositivo.
        """
        available_ports = list(serial.tools.list_ports.comports())
        for port, desc, _ in available_ports:
            if device_description in desc:
                return port
        return None

    def establish_connection(self):
        """
        Inicializa y establece la conexión Modbus.
        Retorna un objeto minimalmodbus.Instrument.
        """
        # Intentar detectar el dispositivo "DigiRail Connect"
        device_description = "DigiRail Connect"
        com_port = self.detect_com_port(device_description)
        if com_port:
            self.logger.info(f"Puerto {device_description} detectado: {com_port}")
        else:
            # Intentar con "USB-SERIAL CH340"
            device_description = "USB-SERIAL CH340"
            com_port = self.detect_com_port(device_description)
            if com_port:
                self.logger.info(f"Puerto detectado: {com_port}")
            else:
                error_msg = "No se detectaron puertos COM para el dispositivo."
                self.logger.error(error_msg)
                raise ModbusConnectionError(error_msg)

        try:
            instrument = minimalmodbus.Instrument(com_port, self.device_address)
            self.logger.info(
                f"Conexión Modbus establecida en puerto {com_port}, dirección {self.device_address}"
            )
            return instrument
        except minimalmodbus.ModbusException as e:
            error_msg = f"Error al configurar el puerto serie: {e}"
            self.logger.error(error_msg)
            raise ModbusConnectionError(error_msg) from e

class ModbusDevice:
    """
    Envuelve el objeto minimalmodbus.Instrument y provee métodos seguros para leer datos.
    """
    def __init__(self, instrument, device_logger):
        self.instrument = instrument
        self.logger = device_logger

    def safe_read(self, method, *args, **kwargs):
        """
        Realiza una lectura segura usando el método proporcionado.
        """
        try:
            return method(*args, **kwargs)
        except (serial.SerialException, IOError, ValueError, minimalmodbus.ModbusException) as e:
            self.logger.error(f"Error al leer del dispositivo Modbus: {e}")
            return None

    def read_digital_input(self, address: int):
        """
        Lee el estado de una entrada digital.
        """
        return self.safe_read(self.instrument.read_bit, address, functioncode=2)

    def read_register(self, register: int, functioncode: int = 3):
        """
        Lee el valor de un registro de alta resolución.
        """
        return self.safe_read(self.instrument.read_register, register, functioncode=functioncode)

class ModbusProcessor:
    """
    Procesa las operaciones Modbus, actualizando la base de datos.
    """
    # Constantes definidas para las direcciones y registros
    D1 = 70
    D2 = 71
    HR_COUNTER1_LO = 22
    HR_COUNTER1_HI = 23
    HR_COUNTER2_LO = 24
    HR_COUNTER2_HI = 25

    def __init__(self, modbus_device: ModbusDevice, repository, modbus_logger):
        self.device = modbus_device
        self.repository = repository
        self.logger = modbus_logger

    def process(self):
        """
        Procesa todas las operaciones Modbus.
        """
        self.process_digital_inputs()
        self.process_high_resolution_registers()

    def process_digital_inputs(self):
        """
        Procesa las entradas digitales y actualiza la base de datos.
        """
        self._process_input(self.D1, "HR_INPUT1_STATE", self.device.read_digital_input)
        self._process_input(self.D2, "HR_INPUT2_STATE", self.device.read_digital_input)

    def process_high_resolution_registers(self):
        """
        Procesa los registros de alta resolución y actualiza la base de datos.
        """
        self._process_register(self.HR_COUNTER1_LO, "HR_COUNTER1_LO")
        self._process_register(self.HR_COUNTER1_HI, "HR_COUNTER1_HI")
        self._process_register(self.HR_COUNTER2_LO, "HR_COUNTER2_LO")
        self._process_register(self.HR_COUNTER2_HI, "HR_COUNTER2_HI")

    def _process_input(self, address: int, description: str, read_function):
        """
        Procesa una entrada digital específica y actualiza la base de datos.
        """
        value = read_function(address)
        if value is not None:
            self._update_database(address, value, description)
        else:
            error_msg = f"Error al leer la entrada en la dirección {address}"
            self.logger.error(error_msg)
            raise ModbusReadError(error_msg)

    def _process_register(self, register: int, description: str):
        """
        Procesa un registro de alta resolución y actualiza la base de datos.
        """
        value = self.device.read_register(register, functioncode=3)
        if value is not None:
            self._update_database(register, value, description)
        else:
            error_msg = f"Error al leer el registro en la dirección {register}"
            self.logger.error(error_msg)
            raise ModbusReadError(error_msg)

    def _update_database(self, address: int, value, description: str):
        """
        Actualiza el registro correspondiente en la base de datos.
        """
        query, params = self._build_update_query(address, value)
        try:
            self.repository.actualizar_registro(query, params)
            self.logger.info(
                f"Registro actualizado: dirección {address}, "
                f"descripción: {description}, valor {value}"
            )
        except Exception as e:
            self.logger.error(
                f"Error al actualizar el registro: dirección {address}, {description}: {e}"
            )
            raise DatabaseUpdateError(f"Error al actualizar la base de datos: {e}") from e

    def _build_update_query(self, address: int, value):
        """
        Construye la consulta SQL para actualizar el registro.
        """
        query = "UPDATE registros_modbus SET valor = :valor WHERE direccion_modbus = :direccion"
        params = {'valor': value, 'direccion': address}
        return query, params

def process_modbus_operations():
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

    modbus_device = ModbusDevice(instrument, logger)
    repository = SQLAlchemyDatabaseRepository()
    processor = ModbusProcessor(modbus_device, repository, logger)
    try:
        processor.process()
    except (ModbusReadError, DatabaseUpdateError) as e:
        logger.error(f"Error durante el procesamiento de operaciones Modbus: {e}")
