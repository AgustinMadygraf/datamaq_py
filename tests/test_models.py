"""
Test de entidades de dominio: Verifica que las entidades no dependen de infraestructura y pueden instanciarse.
"""
from src.domain.modbus_register import ModbusRegister
from src.domain.production_counter import ProductionCounter
from src.domain.interval_production import IntervalProduction

def test_modbus_register():
    reg = ModbusRegister(address=1, value=123, description="Test", unit="V")
    assert reg.address == 1
    assert reg.value == 123
    assert reg.description == "Test"
    assert reg.unit == "V"

def test_production_counter():
    pc = ProductionCounter(id=1, count=100, timestamp="2025-07-07T10:00:00", description="Turno mañana")
    assert pc.id == 1
    assert pc.count == 100
    assert pc.timestamp == "2025-07-07T10:00:00"
    assert pc.description == "Turno mañana"

def test_interval_production():
    ip = IntervalProduction(start_time="2025-07-07T08:00:00", end_time="2025-07-07T09:00:00", produced_units=50, defective_units=2, notes="OK")
    assert ip.start_time == "2025-07-07T08:00:00"
    assert ip.end_time == "2025-07-07T09:00:00"
    assert ip.produced_units == 50
    assert ip.defective_units == 2
    assert ip.notes == "OK"
