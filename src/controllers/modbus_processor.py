"""
Path: src/core/modbus_processor.py
Este módulo se encarga de procesar las operaciones Modbus,
"""

import minimalmodbus
from src.logs.config_logger import configurar_logging
from src.db_operations import check_db_connection, update_database
from src.controller import read_digital_input, ModbusConnectionError, detect_serial_ports

logger = configurar_logging()

# Constantes (se reutilizan las mismas definiciones)
D1 = 70
D2 = 71
HR_COUNTER1_LO = 22
HR_COUNTER1_HI = 23
HR_COUNTER2_LO = 24
HR_COUNTER2_HI = 25

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

def establish_db_connection():
    " Establece la conexión con la base de datos."
    engine = check_db_connection()
    if engine is None:
        raise DatabaseConnectionError("Error de conexión a la base de datos")
    return engine

def establish_modbus_connection(com_port, device_address):
    "Establece la conexión con el dispositivo Modbus."
    return establish_connection(
        lambda: minimalmodbus.Instrument(com_port, device_address), 
        "Error al configurar el puerto serie", 
        ModbusConnectionError
    )

def establish_connection(connect_func, error_message, error_exception):
    " Establece una conexión segura y maneja errores."
    try:
        return connect_func()
    except Exception as e:
        logger.error(f"{error_message}: {e}")
        raise error_exception(f"{error_message}. Detalles: {e}") from e

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
        raise ModbusReadError(f"Error al leer la dirección {address} del dispositivo Modbus: {e}") from e

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

def safe_modbus_read(method, *args, **kwargs):
    "Realiza una lectura segura de un dispositivo Modbus."
    try:
        return method(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error al leer del dispositivo Modbus: {e}")
        return None

class DatabaseConnectionError(Exception):
    """Excepción para errores de conexión con la base de datos."""
    pass

class ModbusReadError(Exception):
    """Excepción para errores de lectura del dispositivo Modbus."""
    pass

def inicializar_conexion_modbus():
    "Inicializa la conexión Modbus."

    device_address = 1
    device_description = "DigiRail Connect"  
    com_port = detect_serial_ports(device_description)
    if com_port:
        logger.info(f"Puerto {device_description} detectado: {com_port}")
    else:
        device_description = "USB-SERIAL CH340"  
        com_port = detect_serial_ports(device_description)
        if com_port:
            logger.info(f"Puerto detectado: {com_port}")
        else:
            logger.error("No se detectaron puertos COM para el dispositivo.")
            exit()
    return com_port, device_address
