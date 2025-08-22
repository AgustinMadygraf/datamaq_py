"""
Path: use_cases/process_modbus_operations.py
"""

from abc import ABC, abstractmethod

class IModbusGateway(ABC):
    @abstractmethod
    def read_digital_input(self, address: int):
        pass

    @abstractmethod
    def read_register(self, register: int, functioncode: int = 3):
        pass

class IDatabaseGateway(ABC):
    @abstractmethod
    def actualizar_registro(self, query, params):
        pass

class ProcessModbusOperationsUseCase:
    D1 = 70
    D2 = 71
    HR_COUNTER1_LO = 22
    HR_COUNTER1_HI = 23
    HR_COUNTER2_LO = 24
    HR_COUNTER2_HI = 25

    def __init__(self, modbus_gateway: IModbusGateway, db_gateway: IDatabaseGateway, logger):
        self.modbus_gateway = modbus_gateway
        self.db_gateway = db_gateway
        self.logger = logger

    def execute(self):
        # Procesar entradas digitales
        for address, description in [
            (self.D1, "HR_INPUT1_STATE"),
            (self.D2, "HR_INPUT2_STATE")
        ]:
            value = self.modbus_gateway.read_digital_input(address)
            query, params = self._build_update_query(address, value)
            self.db_gateway.actualizar_registro(query, params)
            self.logger.info(f"Registro actualizado: dirección {address}, descripción: {description}, valor {value}")

        # Procesar registros de alta resolución
        for register, description in [
            (self.HR_COUNTER1_LO, "HR_COUNTER1_LO"),
            (self.HR_COUNTER1_HI, "HR_COUNTER1_HI"),
            (self.HR_COUNTER2_LO, "HR_COUNTER2_LO"),
            (self.HR_COUNTER2_HI, "HR_COUNTER2_HI")
        ]:
            value = self.modbus_gateway.read_register(register)
            query, params = self._build_update_query(register, value)
            self.db_gateway.actualizar_registro(query, params)
            self.logger.info(f"Registro actualizado: dirección {register}, descripción: {description}, valor {value}")

    def _build_update_query(self, address: int, value):
        query = "UPDATE registros_modbus SET valor = :valor WHERE direccion_modbus = :direccion"
        params = {'valor': value, 'direccion': address}
        return query, params
