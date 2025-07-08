"""
Adaptador para IModbusProcessor que utiliza ModbusProcessor.
"""
from src.application.interfaces import IModbusProcessor
from src.modbus_processor import ModbusProcessor, ModbusConnectionManager, ModbusConnectionError, ModbusDevice
from src.utils.logging.dependency_injection import get_logger

class ModbusProcessorAdapter(IModbusProcessor):
    def __init__(self, repository, logger=None):
        self.repository = repository
        self.logger = logger or get_logger()

    def procesar_datos(self, datos: dict = None) -> dict:
        """
        Orquesta el procesamiento de operaciones Modbus usando ModbusProcessor.
        El parámetro 'datos' se ignora para compatibilidad con la interfaz.
        """
        connection_manager = ModbusConnectionManager(self.logger)
        try:
            instrument = connection_manager.establish_connection()
        except ModbusConnectionError as e:
            self.logger.error(f"Error de conexión Modbus: {e}")
            return {"error": str(e)}
        modbus_device = ModbusDevice(instrument, self.logger)
        processor = ModbusProcessor(modbus_device, self.repository, self.logger)
        try:
            processor.process()
            return {"status": "ok"}
        except Exception as e:
            self.logger.error(f"Error durante el procesamiento de operaciones Modbus: {e}")
            return {"error": str(e)}
