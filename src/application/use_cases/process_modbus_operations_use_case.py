"""
Caso de uso: Procesar operaciones Modbus
"""

from src.application.interfaces import IModbusProcessor

class ProcessModbusOperationsUseCase:
    def __init__(self, modbus_processor: IModbusProcessor):
        self.modbus_processor = modbus_processor

    def execute(self, *args, **kwargs):
        """
        Orquesta el procesamiento de operaciones Modbus.
        Args y kwargs se delegan al procesador concreto.
        """
        return self.modbus_processor.procesar_datos(*args, **kwargs)
