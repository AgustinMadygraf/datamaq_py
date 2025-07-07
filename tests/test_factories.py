"""
Test de fábricas: Verifica que las fábricas crean objetos correctamente configurados.
"""
import pytest  # pylint: disable=import-error
from src.factories import create_repository, create_modbus_device, create_data_transfer_controller


def test_create_repository():
    repo = create_repository()
    # Debe tener los métodos de la interfaz
    assert hasattr(repo, 'ejecutar_consulta')
    assert hasattr(repo, 'actualizar_registro')
    assert hasattr(repo, 'commit')
    assert hasattr(repo, 'rollback')
    assert hasattr(repo, 'cerrar_conexion')


def test_create_modbus_device(monkeypatch):
    # Mock ModbusConnectionManager y ModbusDevice para evitar hardware real
    from src import factories
    monkeypatch.setattr(factories, 'ModbusConnectionManager', lambda logger: type('FakeMgr', (), {'establish_connection': lambda self: 'fake_instrument', 'device_address': 1})())
    monkeypatch.setattr(factories, 'ModbusDevice', lambda instrument, logger: type('FakeDevice', (), {'instrument': instrument, 'logger': logger})())
    device = create_modbus_device()
    assert hasattr(device, 'instrument')
    assert hasattr(device, 'logger')


def test_create_data_transfer_controller(monkeypatch):
    # Mock DataTransferController para evitar dependencias reales
    from src import factories
    monkeypatch.setattr(factories, 'DataTransferController', lambda logger, repo: type('FakeController', (), {'logger': logger, 'repo': repo})())
    controller = create_data_transfer_controller()
    assert hasattr(controller, 'logger')
    assert hasattr(controller, 'repo')
