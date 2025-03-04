"""
Path: src/utils/modbus_connection.py
Este módulo centraliza la lógica de conexión Modbus,
incluyendo la detección de puertos serie y la inicialización de conexiones.
"""

import serial.tools.list_ports
import minimalmodbus
from utils.logging.dependency_injection import get_logger

logger = get_logger()


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
