"""
Path: src/modbus_connection_manager.py
"""

import minimalmodbus
import serial.tools.list_ports

class ModbusConnectionError(Exception):
    """Excepción para errores de conexión con el dispositivo Modbus."""
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
