"""
Test de integración: Verifica que process_modbus_operations requiere un repositorio y funciona con un mock.
"""
import pytest  # pylint: disable=import-error
from src.modbus_processor import process_modbus_operations

class DummyRepo:
    def actualizar_registro(self, *args, **kwargs):
        self.called = True
    def obtener_engine(self): pass
    def ejecutar_consulta(self, consulta, parametros): pass
    def insertar_lote(self, consulta, lista_parametros): pass
    def commit(self): pass
    def rollback(self): pass
    def cerrar_conexion(self): pass

class DummyDevice:
    def read_digital_input(self, address): return 1
    def read_register(self, register, functioncode=3): return 42

class DummyLogger:
    def info(self, msg): pass
    def error(self, msg): pass
    def debug(self, msg): pass

class DummyModbusProcessor:
    def __init__(self, device, repo, logger):
        self.device = device
        self.repository = repo
        self.logger = logger
    def process(self):
        self.repository.actualizar_registro('query', {'valor': 1, 'direccion': 1})


def test_process_modbus_operations_requires_repo():
    with pytest.raises(ValueError):
        process_modbus_operations(repository=None)


def test_process_modbus_operations_with_mock(monkeypatch):
    repo = DummyRepo()
    # Monkeypatch ModbusConnectionManager y ModbusDevice para evitar hardware real
    from src import modbus_processor
    monkeypatch.setattr(modbus_processor, 'ModbusConnectionManager', lambda logger: type('FakeMgr', (), {'establish_connection': lambda self: 'fake_instrument', 'device_address': 1})())
    monkeypatch.setattr(modbus_processor, 'ModbusDevice', lambda instrument, logger: DummyDevice())
    monkeypatch.setattr(modbus_processor, 'ModbusProcessor', lambda device, repo, logger: DummyModbusProcessor(device, repo, logger))
    process_modbus_operations(repository=repo)
    assert hasattr(repo, 'called')
