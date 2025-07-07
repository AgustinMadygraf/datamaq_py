"""
Test de interfaces: Verifica que las interfaces de puertos Modbus y DB se pueden importar y heredar correctamente.
"""

from src.interfaces import IDatabaseRepository, IModbusConnectionManager, IModbusDevice, IModbusProcessor

# Clases dummy para verificar herencia y métodos abstractos
class DummyDB(IDatabaseRepository):
    def obtener_engine(self): pass
    def ejecutar_consulta(self, consulta, parametros): pass
    def actualizar_registro(self, consulta, parametros): pass
    def insertar_lote(self, consulta, lista_parametros): pass
    def commit(self): pass
    def rollback(self): pass
    def cerrar_conexion(self): pass

class DummyConnMgr(IModbusConnectionManager):
    def detectar_dispositivos(self): return []
    def abrir_conexion(self, direccion): pass
    def cerrar_conexion(self, conexion): pass

class DummyDevice(IModbusDevice):
    def leer_registro(self, direccion): return 0
    def escribir_registro(self, direccion, valor): pass


# DummyModbusProcessor implementa solo IModbusProcessor
class DummyModbusProcessor(IModbusProcessor):
    def procesar_datos(self, datos):
        return datos

def test_interfaces_instanciables():
    DummyDB()
    DummyConnMgr()
    DummyDevice()
    DummyModbusProcessor()
