"""
Test de decoradores: Verifica que los errores se capturan y registran adecuadamente.
"""
import pytest  # pylint: disable=import-error
from src.utils.logging.decorators import handle_errors

class DummyLogger:
    def __init__(self):
        self.last_error = None
    def error(self, msg):
        self.last_error = msg

class DummyClass:
    def __init__(self, logger):
        self.logger = logger
    @handle_errors()
    def metodo_con_error(self):
        raise ValueError("fallo de prueba")

def test_handle_errors_captura_y_loguea():
    logger = DummyLogger()
    obj = DummyClass(logger)
    with pytest.raises(ValueError):
        obj.metodo_con_error()
    assert logger.last_error is not None
    assert "fallo de prueba" in logger.last_error
