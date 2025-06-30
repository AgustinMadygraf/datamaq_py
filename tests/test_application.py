import unittest
from unittest.mock import MagicMock
from src.application.use_cases import DataTransferController
from src.domain.entities import IDatabaseRepository

class DummyRepository(IDatabaseRepository):
    def obtener_engine(self):
        return None
    def ejecutar_consulta(self, consulta, parametros):
        return [(1, 2, 3)]
    def actualizar_registro(self, consulta, parametros):
        pass
    def insertar_lote(self, consulta, lista_parametros):
        pass
    def commit(self):
        pass

class TestDataTransferController(unittest.TestCase):
    def setUp(self):
        self.logger = MagicMock()
        self.repository = DummyRepository()
        self.controller = DataTransferController(self.logger, self.repository)

    def test_no_transfer_if_not_time(self):
        self.controller._ultimo_guardado = None
        self.controller.es_tiempo_cercano_multiplo_cinco = MagicMock(return_value=False)
        obtener_datos = MagicMock()
        insertar_datos = MagicMock()
        self.controller.run_transfer(obtener_datos, insertar_datos)
        self.logger.info.assert_any_call('No es momento de transferir datos. Esperando la próxima verificación.')

    def test_transfer_if_time_and_not_saved(self):
        self.controller._ultimo_guardado = None
        self.controller.es_tiempo_cercano_multiplo_cinco = MagicMock(return_value=True)
        obtener_datos = MagicMock()
        insertar_datos = MagicMock()
        self.controller.production_service.transfer = MagicMock()
        self.controller.interval_service.transfer = MagicMock()
        self.controller.run_transfer(obtener_datos, insertar_datos)
        self.controller.production_service.transfer.assert_called()
        self.controller.interval_service.transfer.assert_called()

if __name__ == '__main__':
    unittest.main()
