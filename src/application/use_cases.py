from datetime import datetime
from src.domain.services import ProductionLogTransferService, IntervalProductionTransferService
from src.infrastructure.db.sqlalchemy_repository import SQLAlchemyDatabaseRepository

# Casos de uso de la aplicación
# Definición de casos de uso:
# - Orquestan la interacción entre entidades, servicios de dominio y adaptadores.
# - No contienen lógica de infraestructura.
# - Representan acciones o procesos clave del sistema.

class TransferirDatosCasoUso:
    """Caso de uso para transferir datos entre sistemas."""
    def __init__(self, servicio_transferencia):
        self.servicio_transferencia = servicio_transferencia

    def ejecutar(self, datos):
        # Orquestar la transferencia usando el servicio de dominio
        self.servicio_transferencia.transferir(datos)

# Agregar aquí otros casos de uso según los procesos del sistema.

class DataTransferController:
    """
    Controlador que orquesta la transferencia de datos:
      - Verifica si es el momento de transferir (según la hora actual).
      - Ejecuta la transferencia de ProductionLog e intervalproduction.
    """
    def __init__(self, log):
        self.logger = log
        repository = SQLAlchemyDatabaseRepository()
        self.production_service = ProductionLogTransferService(log, repository)
        self.interval_service = IntervalProductionTransferService(log, repository)

    def es_tiempo_cercano_multiplo_cinco(self, tolerancia=5):
        ahora = datetime.now()
        minuto_actual = ahora.minute
        segundo_actual = ahora.second
        cercano_a_multiplo = (
            (minuto_actual % 5) <= (tolerancia / 60) and segundo_actual <= tolerancia
        )
        self.logger.info(
            "Chequeando tiempo: %s, cercano a múltiplo de 5: %s",
            ahora, 'sí' if cercano_a_multiplo else 'no'
        )
        return cercano_a_multiplo

    def run_transfer(self, obtener_datos, insertar_datos):
        if self.es_tiempo_cercano_multiplo_cinco():
            self.logger.info("Iniciando transferencia de datos.")
            unixtime = int(datetime.now().timestamp())
            self.production_service.transfer(unixtime, obtener_datos, insertar_datos)
            self.interval_service.transfer(unixtime, obtener_datos, insertar_datos)
        else:
            self.logger.info(
                "No es momento de transferir datos. Esperando la próxima verificación."
            )

def main_transfer_controller(logger, obtener_datos, insertar_datos):
    controller = DataTransferController(logger)
    controller.run_transfer(obtener_datos, insertar_datos)
