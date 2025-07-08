"""
Servicio de dominio: Procesamiento de entradas y registros Modbus.
Extrae la lógica de negocio de ModbusProcessor.
"""
from src.domain.modbus_register import ModbusRegister
from src.domain.production_counter import ProductionCounter
from src.domain.interval_production import IntervalProduction
from typing import Callable

def procesar_entrada_digital(address: int, description: str, read_function: Callable[[int], int]) -> ModbusRegister:
    value = read_function(address)
    if value is None:
        raise ValueError(f"Error al leer la entrada en la dirección {address}")
    return ModbusRegister(address=address, value=value, description=description)

def procesar_registro_alta_resolucion(register: int, description: str, read_function: Callable[[int, int], int]) -> ModbusRegister:
    value = read_function(register, 3)
    if value is None:
        raise ValueError(f"Error al leer el registro en la dirección {register}")
    return ModbusRegister(address=register, value=value, description=description)
