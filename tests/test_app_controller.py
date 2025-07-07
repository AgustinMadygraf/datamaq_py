"""
Test de AppController: Verifica la inyección de repositorio y el fallback a la fábrica.
"""
import pytest  # pylint: disable=import-error
from src.app_controller import AppController

class DummyRepo:
    def __init__(self):
        self.called = False
    def ejecutar_consulta(self, *a, **k): pass
    def actualizar_registro(self, *a, **k): pass
    def insertar_lote(self, *a, **k): pass
    def commit(self): pass
    def rollback(self): pass
    def cerrar_conexion(self): pass

class DummyLogger:
    def debug(self, msg, **kwargs): pass
    def info(self, msg, **kwargs): pass
    def error(self, msg, **kwargs): pass


def test_appcontroller_with_injected_repo(monkeypatch):
    repo = DummyRepo()
    logger = DummyLogger()
    # Mock process_modbus_operations y main_transfer_controller para no ejecutar lógica real
    monkeypatch.setattr('src.app_controller.process_modbus_operations', lambda repository: repo.__setattr__('called', True))
    monkeypatch.setattr('src.app_controller.main_transfer_controller', lambda: None)
    app = AppController(logger=logger, repository=repo)
    app.execute_main_operations()
    assert repo.called

def test_appcontroller_without_repo(monkeypatch):
    logger = DummyLogger()
    # Mock process_modbus_operations y main_transfer_controller para no ejecutar lógica real
    monkeypatch.setattr('src.app_controller.process_modbus_operations', lambda repository: None)
    monkeypatch.setattr('src.app_controller.main_transfer_controller', lambda: None)
    app = AppController(logger=logger)
    # No debe lanzar excepción aunque no se pase repo
    app.execute_main_operations()
