"""
Path: src/modbus_processor.py
"""

import minimalmodbus
import serial.tools.list_ports
from src.db_operations import DatabaseUpdateError
from utils.logging.simple_logger import LoggerService

logger = LoggerService()

class ModbusReadError(Exception):
    """Excepción para errores de lectura del dispositivo Modbus."""
    pass

class ModbusConfig:
    """
    Clase de configuración que contiene constantes relacionadas con las direcciones Modbus.
    Separa la configuración del comportamiento según el principio de separación de responsabilidades.
    """
    # Constantes para entradas digitales
    D1 = 70
    D2 = 71
    
    # Constantes para registros de alta resolución
    HR_COUNTER1_LO = 22
    HR_COUNTER1_HI = 23
    HR_COUNTER2_LO = 24
    HR_COUNTER2_HI = 25

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
            result = method(*args, **kwargs)
            # Usar ModbusDebug para registrar la lectura exitosa
            register_address = args[0] if args else kwargs.get('address', 'unknown')
            return result
        except (serial.SerialException, IOError, ValueError, minimalmodbus.ModbusException) as e:
            self.logger.error(f"Error al leer del dispositivo Modbus: {e}")
            # Usar ModbusDebug para registrar el error de lectura
            register_address = args[0] if args else kwargs.get('address', 'unknown')
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

class ModbusDatabaseUpdater:
    """
    Responsable de actualizar la base de datos con los valores leídos.
    Sigue el principio de responsabilidad única (SRP).
    """
    def __init__(self, repository, db_logger):
        self.repository = repository
        self.logger = db_logger
    
    def update_database(self, address: int, value, description: str):
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

class ModbusProcessor:
    """
    Orquesta las operaciones Modbus, coordinando la lectura de dispositivos y la actualización de la base de datos.
    Ahora se enfoca en la coordinación en lugar de realizar ambas operaciones.
    """
    def __init__(self, modbus_device: ModbusDevice, db_updater: ModbusDatabaseUpdater, modbus_logger):
        self.device = modbus_device
        self.db_updater = db_updater
        self.logger = modbus_logger
        self.config = ModbusConfig()
        # Iniciar contador para estadísticas
        self.successful_reads = 0
        self.failed_reads = 0

    def process(self):
        """
        Procesa todas las operaciones Modbus.
        """
        # Usar DebugTimer para medir el tiempo de procesamiento
        self.logger.debug("Iniciando procesamiento de entradas digitales...")
        self.process_digital_inputs()
        
        self.logger.debug("Iniciando procesamiento de registros de alta resolución...")
        self.process_high_resolution_registers()
        
        # Registrar estadísticas
        self.logger.debug(f"Procesamiento completado: {self.successful_reads} lecturas exitosas, {self.failed_reads} fallidas")

    def process_digital_inputs(self):
        """
        Procesa las entradas digitales y actualiza la base de datos.
        """
        self._process_input(self.config.D1, "HR_INPUT1_STATE", self.device.read_digital_input)
        self._process_input(self.config.D2, "HR_INPUT2_STATE", self.device.read_digital_input)

    def process_high_resolution_registers(self):
        """
        Procesa los registros de alta resolución y actualiza la base de datos.
        """
        self._process_register(self.config.HR_COUNTER1_LO, "HR_COUNTER1_LO")
        self._process_register(self.config.HR_COUNTER1_HI, "HR_COUNTER1_HI")
        self._process_register(self.config.HR_COUNTER2_LO, "HR_COUNTER2_LO")
        self._process_register(self.config.HR_COUNTER2_HI, "HR_COUNTER2_HI")

    def _process_input(self, address: int, description: str, read_function):
        """
        Procesa una entrada digital específica y actualiza la base de datos.
        """
        try:
            value = read_function(address)            
            if value is not None:
                self.db_updater.update_database(address, value, description)
                self.successful_reads += 1
            else:
                error_msg = f"Error al leer la entrada en la dirección {address}"
                self.logger.error(error_msg)
                self.failed_reads += 1
                raise ModbusReadError(error_msg)
        except Exception as e:
            self.failed_reads += 1
            self.logger.error(f"Error procesando entrada {description} (dir: {address}): {e}")
            raise

    def _process_register(self, register: int, description: str):
        """
        Procesa un registro de alta resolución y actualiza la base de datos.
        """
        try:
            value = self.device.read_register(register, functioncode=3)
            
            if value is not None:
                self.db_updater.update_database(register, value, description)
                self.successful_reads += 1
            else:
                error_msg = f"Error al leer el registro en la dirección {register}"
                self.logger.error(error_msg)
                self.failed_reads += 1
                raise ModbusReadError(error_msg)
        except Exception as e:
            self.failed_reads += 1
            self.logger.error(f"Error procesando registro {description} (dir: {register}): {e}")
            raise
