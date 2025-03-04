"""
Path: src/core/modbus_processor.py
Este módulo se encarga de procesar las operaciones Modbus,
"""

import minimalmodbus
import serial.tools.list_ports
from src.db_operations import SQLAlchemyDatabaseRepository, DatabaseUpdateError
from utils.logging.dependency_injection import get_logger

logger = get_logger()

# Constantes (se reutilizan las mismas definiciones)
D1 = 70
D2 = 71
HR_COUNTER1_LO = 22
HR_COUNTER1_HI = 23
HR_COUNTER2_LO = 24
HR_COUNTER2_HI = 25

repository_instance = SQLAlchemyDatabaseRepository()

def process_modbus_operations():
    "Procesa las operaciones Modbus."
    try:
        com_port, device_address = inicializar_conexion_modbus()
    except ModbusConnectionError as e:
        logger.error(f"Error de conexión Modbus: {e}")
        return

    establish_db_connection()
    instrument = establish_modbus_connection(com_port, device_address)

    process_digital_input(instrument)
    process_high_resolution_register(instrument)


def build_update_query(address, value):
    """
    Construye una consulta SQL de actualización para la tabla 'registros_modbus'.
    """
    consulta = "UPDATE registros_modbus SET valor = :valor WHERE direccion_modbus = :direccion"
    parametros = {'valor': value, 'direccion': address}
    return consulta, parametros

def update_database(address, value, descripcion):
    """
    Función de compatibilidad que utiliza el repositorio para actualizar un registro.
    """
    consulta, parametros = build_update_query(address, value)
    try:
        repository_instance.actualizar_registro(consulta, parametros)
        logger.info(
            f"Registro actualizado: dirección {address}, descripción: {descripcion}, valor {value}"
        )
    except Exception as e:
        logger.error(f"Error al actualizar el registro: dirección {address}, {descripcion}: {e}")
        raise DatabaseUpdateError(f"Error al actualizar la base de datos: {e}") from e

def establish_db_connection():
    " Establece la conexión con la base de datos."
    engine = SQLAlchemyDatabaseRepository()
    if engine is None:
        raise DatabaseConnectionError("Error de conexión a la base de datos")
    return engine

def process_digital_input(instrument):
    " Procesa las entradas digitales y actualiza la base de datos."
    process_input_and_update(instrument, read_digital_input, D1, "HR_INPUT1_STATE")
    process_input_and_update(instrument, read_digital_input, D2, "HR_INPUT2_STATE")

def process_input_and_update(instrument, read_function, address, description):
    "Procesa una entrada digital y actualiza la base de datos."
    try:
        state = read_function(instrument, address)
        if state is not None:
            update_database(address, state, descripcion=description)
    except minimalmodbus.ModbusException as e:
        raise ModbusReadError(
            f"Error al leer la dirección {address} del dispositivo Modbus: {e}"
        ) from e

def process_high_resolution_register(instrument):
    "Procesa los registros de alta resolución y actualiza la base de datos."
    update_register_value(instrument, HR_COUNTER1_LO, "HR_COUNTER1_LO")
    update_register_value(instrument, HR_COUNTER1_HI, "HR_COUNTER1_HI")
    update_register_value(instrument, HR_COUNTER2_LO, "HR_COUNTER2_LO")
    update_register_value(instrument, HR_COUNTER2_HI, "HR_COUNTER2_HI")

def update_register_value(instrument, register, description):
    "Actualiza el valor de un registro en la base de datos."
    value = safe_modbus_read(instrument.read_register, register, functioncode=3)
    if value is not None:
        update_database(register, value, descripcion=description)

class DatabaseConnectionError(Exception):
    """Excepción para errores de conexión con la base de datos."""
    pass

class ModbusReadError(Exception):
    """Excepción para errores de lectura del dispositivo Modbus."""
    pass

def read_digital_input(instrument, address):
    """
    Lee el estado de una entrada digital de un dispositivo Modbus.

    Utiliza la función 'safe_modbus_read' para realizar una lectura segura de un bit del dispositivo
    Modbus especificado. Esta función se enfoca en leer estados de entradas digitales, 
    como sensores on/off.

    Args:
        instrument (minimalmodbus.Instrument): El instrumento Modbus utilizado para la lectura.
        address (int): La dirección de la entrada digital a leer en el dispositivo Modbus.

    Returns:
        int/None: El estado de la entrada digital (1 o 0) si la lectura es exitosa, 
        o None si ocurre un error.
    """
    return safe_modbus_read(instrument.read_bit, address, functioncode=2)

class ModbusConnectionError(Exception):
    """Excepción para errores de conexión con el dispositivo Modbus."""
    pass


def detect_serial_ports(device_description):
    """
    Busca y retorna el nombre del puerto serie que coincide con la descripción del dispositivo dada.

    Args:
        device_description (str): La descripción del dispositivo Modbus a buscar entre los puertos serie.

    Returns:
        str/None: El nombre del puerto serie que coincide con la descripción del dispositivo, 
        o None si no se encuentra.
    """
    available_ports = list(serial.tools.list_ports.comports())
    for port, desc, _ in available_ports:
        if device_description in desc:
            return port
    return None


def inicializar_conexion_modbus():
    """
    Inicializa la conexión con el dispositivo Modbus, detectando el puerto serie adecuado.

    Returns:
        tuple: Una tupla que contiene el nombre del puerto serie encontrado 
        y la dirección del dispositivo Modbus.

    Raises:
        ModbusConnectionError: Si no se detecta ningún puerto COM para el dispositivo.
    """
    device_address = 1
    device_description = "DigiRail Connect"
    com_port = detect_serial_ports(device_description)
    if (com_port):
        logger.info(f"Puerto {device_description} detectado: {com_port}")
    else:
        device_description = "USB-SERIAL CH340"
        com_port = detect_serial_ports(device_description)
        if (com_port):
            logger.info(f"Puerto detectado: {com_port}")
        else:
            logger.error("No se detectaron puertos COM para el dispositivo.")
            raise ModbusConnectionError("No se detectaron puertos COM para el dispositivo")
    return com_port, device_address


def establish_modbus_connection(com_port, device_address):
    """
    Establece la conexión con el dispositivo Modbus.

    Args:
        com_port (str): Puerto serie a utilizar para la conexión.
        device_address (int): Dirección del dispositivo Modbus.

    Returns:
        minimalmodbus.Instrument: Objeto de conexión al instrumento Modbus.

    Raises:
        ModbusConnectionError: Si hay un error al establecer la conexión.
    """
    try:
        instrument = minimalmodbus.Instrument(com_port, device_address)
        logger.info(f"Conexión Modbus establecida en puerto {com_port}, dirección {device_address}")
        return instrument
    except minimalmodbus.ModbusException as e:
        error_msg = f"Error al configurar el puerto serie: {e}"
        logger.error(error_msg)
        raise ModbusConnectionError(error_msg) from e


def safe_modbus_read(method, *args, **kwargs):
    """
    Realiza una lectura segura de un dispositivo Modbus.

    Args:
        method (callable): Método de lectura Modbus a ser invocado.
        *args: Argumentos posicionales para el método de lectura.
        **kwargs: Argumentos de palabra clave para el método de lectura.

    Returns:
        El resultado del método de lectura si es exitoso, o None si ocurre una excepción.
    """
    try:
        return method(*args, **kwargs)
    except (serial.SerialException, IOError, ValueError, minimalmodbus.ModbusException) as e:
        logger.error(f"Error al leer del dispositivo Modbus: {e}")
        return None
