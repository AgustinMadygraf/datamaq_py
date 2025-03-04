"""
Path: src/controller.py
Este script se ocupa de manejar la conexión con el dispositivo Modbus
y procesar las operaciones Modbus.
"""

import os
import platform
from utils.logging.dependency_injection import get_logger
from src.db_operations import update_database
from src.utils.modbus_connection import safe_modbus_read

D1 = 70
D2 = 71
HR_COUNTER1_LO = 22
HR_COUNTER1_HI = 23
HR_COUNTER2_LO = 24
HR_COUNTER2_HI = 25

logger = get_logger()

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

def update_register_value(instrument, register, description):
    " Actualiza el valor de un registro en la base de datos "
    value = safe_modbus_read(instrument.read_register, register, functioncode=3)
    if value is not None:
        update_database(register, value, descripcion=description)

def process_high_resolution_register(instrument):
    " Procesa los registros de alta resolución del dispositivo Modbus "
    update_register_value(instrument, HR_COUNTER1_LO, "HR_COUNTER1_LO")
    update_register_value(instrument, HR_COUNTER1_HI, "HR_COUNTER1_HI")
    update_register_value(instrument, HR_COUNTER2_LO, "HR_COUNTER2_LO")
    update_register_value(instrument, HR_COUNTER2_HI, "HR_COUNTER2_HI")

def limpiar_pantalla():
    """
    Limpia la consola de comandos según el sistema operativo.
    """
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
