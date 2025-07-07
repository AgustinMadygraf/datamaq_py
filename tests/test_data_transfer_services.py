"""
Test de integración: Verifica que los servicios de transferencia funcionan con mocks de repositorio.
"""
import pytest  # pylint: disable=import-error
from src.data_transfer_controller import ProductionLogTransferService, IntervalProductionTransferService

class DummyRepo:
    def __init__(self):
        self.actualizar_registro_called = False
        self.commit_called = False
        self.ejecutar_consulta_called = False
    def actualizar_registro(self, consulta, parametros):
        self.actualizar_registro_called = True
    def obtener_engine(self): pass
    def ejecutar_consulta(self, consulta, parametros):
        self.ejecutar_consulta_called = True
        return [(1, 2, 3, 4)]
    def insertar_lote(self, consulta, lista_parametros): pass
    def commit(self):
        self.commit_called = True
    def rollback(self): pass
    def cerrar_conexion(self): pass

class DummyLogger:
    def info(self, msg, *args): pass
    def error(self, msg, *args): pass
    def warning(self, msg, *args): pass
    def debug(self, msg, *args): pass


def test_production_log_transfer_service_with_mock():
    repo = DummyRepo()
    logger = DummyLogger()
    service = ProductionLogTransferService(logger, repo)
    service.insertar_datos([(1,2,3,4)], "INSERT ...", ["a","b","c","d"])
    assert repo.actualizar_registro_called
    assert repo.commit_called

def test_interval_production_transfer_service_with_mock():
    repo = DummyRepo()
    logger = DummyLogger()
    service = IntervalProductionTransferService(logger, repo)
    service.insertar_datos([(1,2)], "INSERT ...", ["a","b"])
    assert repo.actualizar_registro_called
    assert repo.commit_called
