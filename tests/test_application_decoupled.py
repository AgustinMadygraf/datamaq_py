"""
Test de integración desacoplada: uso de un mock de IDatabaseRepository en un caso de uso.
"""
import unittest
from unittest.mock import MagicMock
from src.application.use_cases import DataTransferController
from src.domain.ports.database_repository import IDatabaseRepository

class FakeDatabaseRepository(IDatabaseRepository):
    def obtener_engine(self):
        return None
    def ejecutar_consulta(self, consulta, parametros):
        return [ (1, 'dato') ]
    def actualizar_registro(self, consulta, parametros):
        self.last_update = (consulta, parametros)

class TestDataTransferController(unittest.TestCase):
    def setUp(self):
        self.logger = MagicMock()
        self.repository = FakeDatabaseRepository()
        self.controller = DataTransferController(self.logger, self.repository)

    def test_run_transfer_calls_services(self):
        # Simular funciones de obtención/inserción
        obtener_datos = MagicMock(return_value=[(1, 'dato')])
        insertar_datos = MagicMock()
        self.controller._ultimo_guardado = None
        self.controller.es_tiempo_cercano_multiplo_cinco = MagicMock(return_value=True)
        self.controller.production_service.transfer = MagicMock()
        self.controller.interval_service.transfer = MagicMock()
        self.controller.run_transfer(obtener_datos, insertar_datos)
        self.controller.production_service.transfer.assert_called()
        self.controller.interval_service.transfer.assert_called()

if __name__ == "__main__":
    unittest.main()
