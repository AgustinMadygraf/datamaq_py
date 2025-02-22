"""
Path: src/controller.py
Este script se ocupa de manejar la conexión con el dispositivo Modbus
y procesar las operaciones Modbus.
"""

from src.logs.config_logger import configurar_logging
from src.db_operations import update_database
import serial.tools.list_ports
import os
import platform

D1 = 70
D2 = 71
HR_COUNTER1_LO = 22
HR_COUNTER1_HI = 23
HR_COUNTER2_LO = 24
HR_COUNTER2_HI = 25

logger = configurar_logging()

def read_digital_input(instrument, address):
    """
    Lee el estado de una entrada digital de un dispositivo Modbus.

    Utiliza la función 'safe_modbus_read' para realizar una lectura segura de un bit del dispositivo
    Modbus especificado. Esta función se enfoca en leer estados de entradas digitales, como sensores on/off.

    Args:
        instrument (minimalmodbus.Instrument): El instrumento Modbus utilizado para la lectura.
        address (int): La dirección de la entrada digital a leer en el dispositivo Modbus.

    Returns:
        int/None: El estado de la entrada digital (1 o 0) si la lectura es exitosa, o None si ocurre un error.
    """
    return safe_modbus_read(instrument.read_bit, address, functioncode=2)

def inicializar_conexion_modbus():
    """
    Inicializa la conexión con el dispositivo Modbus, detectando el puerto serie adecuado.

    Esta función busca un puerto serie disponible que coincida con las descripciones de los dispositivos
    'DigiRail Connect' o 'USB-SERIAL CH340'. Si se encuentra un puerto correspondiente, se retorna su nombre
    junto con la dirección predefinida del dispositivo Modbus.

    Returns:
        tuple: Una tupla que contiene el nombre del puerto serie encontrado y la dirección del dispositivo Modbus.

    Raises:
        SystemExit: Si no se detecta ningún puerto COM para el dispositivo.

    Proceso:
        - Intenta detectar un puerto serie para 'DigiRail Connect'.
        - Si no se encuentra, intenta detectar 'USB-SERIAL CH340'.
        - Si se encuentra un puerto, retorna su nombre y la dirección del dispositivo Modbus.
        - Si no se detecta ningún puerto, muestra un mensaje de error y sale del programa.
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
            logger.info(f"Puerto detectado: {com_port}\n")
        else:
            logger.error("No se detectaron puertos COM para tudispositivo.")
            input("Presiona una tecla para salir")
            exit()
    return com_port, device_address

def update_register_value(instrument, register, description):
    # Se elimina "connection" y se utiliza update_database directamente
    value = safe_modbus_read(instrument.read_register, register, functioncode=3)
    if value is not None:
        update_database(register, value, descripcion=description)

def process_high_resolution_register(instrument):
    # Se elimina el parámetro "connection"
    update_register_value(instrument, HR_COUNTER1_LO, "HR_COUNTER1_LO")
    update_register_value(instrument, HR_COUNTER1_HI, "HR_COUNTER1_HI")
    update_register_value(instrument, HR_COUNTER2_LO, "HR_COUNTER2_LO")
    update_register_value(instrument, HR_COUNTER2_HI, "HR_COUNTER2_HI")

def detect_serial_ports(device_description):
    """
    Busca y retorna el nombre del puerto serie que coincide con la descripción del dispositivo dada.

    Esta función recorre todos los puertos serie disponibles en el sistema y compara la descripción
    de cada uno con la descripción del dispositivo proporcionada. Si encuentra una coincidencia,
    retorna el nombre del puerto serie correspondiente.

    Args:
        device_description (str): La descripción del dispositivo Modbus a buscar entre los puertos serie.

    Returns:
        str/None: El nombre del puerto serie que coincide con la descripción del dispositivo, o None si no se encuentra.
    """
    available_ports = list(serial.tools.list_ports.comports())
    for port, desc, hwid in available_ports:
        if device_description in desc:
            return port
    return None

def safe_modbus_read(method, *args, **kwargs):
    """
    Realiza una lectura segura de un dispositivo Modbus.

    Envuelve la llamada a un método de lectura Modbus en un bloque try-except para manejar excepciones.
    Proporciona un mecanismo de recuperación y registro de errores en caso de fallas en la lectura.

    Args:
        method (callable): Método de lectura Modbus a ser invocado.
        *args: Argumentos posicionales para el método de lectura.
        **kwargs: Argumentos de palabra clave para el método de lectura.

    Returns:
        El resultado del método de lectura si es exitoso, o None si ocurre una excepción.
    """
    try:
        return method(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error al leer del dispositivo Modbus: {e}")
        return None

def limpiar_pantalla():
    """
    Limpia la consola de comandos según el sistema operativo.
    """
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

class ModbusConnectionError(Exception):
    """Excepción para errores de conexión con el dispositivo Modbus."""
    pass
