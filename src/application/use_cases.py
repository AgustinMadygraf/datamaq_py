from datetime import datetime
from src.domain.services import ProductionLogTransferService, IntervalProductionTransferService
from src.domain.ports.database_repository import IDatabaseRepository

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
      - Controla que solo se grabe una vez cada 5 minutos.
    """
    def __init__(self, log, repository: IDatabaseRepository):
        self.logger = log
        self.repository = repository  # Debe ser IDatabaseRepository
        self.production_service = ProductionLogTransferService(log, repository)
        self.interval_service = IntervalProductionTransferService(log, repository)
        self._ultimo_guardado = None  # Timestamp del último guardado exitoso

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
        from datetime import timedelta
        ahora = datetime.now()
        if self.es_tiempo_cercano_multiplo_cinco():
            if self._ultimo_guardado is None or (ahora - self._ultimo_guardado) >= timedelta(minutes=5):
                self.logger.info(f"Iniciando transferencia de datos | unixtime: {int(ahora.timestamp())}")
                unixtime = int(ahora.timestamp())
                self.production_service.transfer(unixtime, obtener_datos, insertar_datos)
                self.logger.info(f"Transferencia ProductionLog completada | unixtime: {unixtime}")
                self.interval_service.transfer(unixtime, obtener_datos, insertar_datos)
                self.logger.info(f"Transferencia IntervalProduction completada | unixtime: {unixtime}")
                self._ultimo_guardado = ahora
            else:
                self.logger.info(
                    f"Ya se grabó en esta ventana de 5 minutos. Último guardado: {self._ultimo_guardado}"
                )
        else:
            self.logger.info(
                f"No es momento de transferir datos. Esperando la próxima verificación. | ahora: {ahora}"
            )

def main_transfer_controller(logger, obtener_datos, insertar_datos, repository):
    controller = DataTransferController(logger, repository)
    controller.run_transfer(obtener_datos, insertar_datos)
