"""
Controlador de transferencia de datos entre la base de datos y el servidor.
"""
import time
from datetime import datetime
from utils.logging.dependency_injection import get_logger
from src.domain.entities import IDatabaseRepository
from src.infrastructure.db.sqlalchemy_repository import SQLAlchemyDatabaseRepository
from src.application.use_cases import main_transfer_controller

logger = get_logger()

class BaseDataTransferService:
    def __init__(self, log, repository: IDatabaseRepository, intervalo_segundos=300):
        self.logger = log
        self.repository = repository
        self.intervalo_segundos = intervalo_segundos

    def _get_unix_time(self):
        unixtime = int(time.time())
        return round(unixtime / self.intervalo_segundos) * self.intervalo_segundos

    def obtener_datos(self, consulta):
        try:
            return self.repository.ejecutar_consulta(consulta, {})
        except Exception as e:
            self.logger.error("Error al ejecutar consulta: %s", e)
        return None

    def insertar_datos(self, datos, consulta_insercion, campos):
        try:
            for fila in datos:
                if len(fila) == len(campos):
                    parametros = dict(zip(campos, fila))
                    self.repository.actualizar_registro(consulta_insercion, parametros)
                else:
                    self.logger.warning("Fila con número incorrecto de elementos: %s", fila)
            self.repository.commit()
            self.logger.info("%s registros insertados con éxito.", len(datos))
        except Exception as e:
            self.logger.error("Error al insertar datos: %s", e)
            self.repository.rollback()
