"""
Path: src/controllers/data_transfer_controller.py
"""

from src.data_transfer_services import (
    ProductionLogTransferService,
    IntervalProductionTransferService,
    PHPDataTransferService,
    TransferScheduler
)


class DataTransferController:
    """
    Controlador que orquesta la transferencia de datos:
      - Verifica si es el momento de transferir (según la hora actual).
      - Ejecuta la transferencia de ProductionLog e intervalproduction.
      - Ejecuta el servicio PHP para enviar los datos.
    """
    def __init__(self, log, production_service=None, interval_service=None, php_service=None, scheduler=None):
        self.logger = log
        # Inyectar o crear las dependencias necesarias
        self.production_service = production_service or ProductionLogTransferService(log)
        self.interval_service = interval_service or IntervalProductionTransferService(log)
        self.php_service = php_service or PHPDataTransferService(log=log)
        self.scheduler = scheduler or TransferScheduler(log)

    def run_transfer(self):
        """
        Orquesta la transferencia de datos:
          - Si es tiempo de transferencia, ejecuta los tres servicios.
          - De lo contrario, informa que no es el momento.
        """
        if self.scheduler.should_transfer():
            self.logger.info("Iniciando transferencia de datos.")
            self.production_service.transfer()
            self.interval_service.transfer()
            php_success = self.php_service.send()
            if not php_success:
                self.logger.warning(
                    "La transferencia de datos PHP falló, pero el programa continuará ejecutándose."
                )
        else:
            self.logger.info(
                "No es momento de transferir datos. Esperando la próxima verificación."
            )

