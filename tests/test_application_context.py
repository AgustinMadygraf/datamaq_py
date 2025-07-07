"""
Test de ApplicationContext: Verifica que se cierran correctamente las conexiones DB y Modbus.
"""
from src.application_context import ApplicationContext

class DummyResource:
    def __init__(self):
        self.closed = False
    def cerrar_conexion(self):
        self.closed = True

class DummyLogger:
    def info(self, msg): pass
    def error(self, msg): pass


def test_application_context_closes_resources(monkeypatch):
    dummy_db = DummyResource()
    dummy_modbus = DummyResource()
    # Monkeypatch para que ApplicationContext use los dummies
    from src import application_context
    monkeypatch.setattr(application_context, 'SQLAlchemyDatabaseRepository', lambda: dummy_db)
    monkeypatch.setattr(application_context, 'ModbusConnectionManager', lambda logger: type('FakeMgr', (), {'establish_connection': lambda self: 'fake_instrument', 'device_address': 1})())
    monkeypatch.setattr(application_context, 'ModbusDevice', lambda instrument, logger: dummy_modbus)
    ctx = ApplicationContext()
    with ctx:
        pass
    assert dummy_db.closed
    assert dummy_modbus.closed
