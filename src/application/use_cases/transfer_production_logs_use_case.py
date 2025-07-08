"""
Caso de uso: Transferir logs de producción
"""

from src.application.interfaces import IDataTransferService

class TransferProductionLogsUseCase:
    def __init__(self, data_transfer_service: IDataTransferService):
        self.data_transfer_service = data_transfer_service

    def execute(self, *args, **kwargs):
        """
        Orquesta la transferencia de logs de producción.
        Args y kwargs se delegan al servicio concreto.
        """
        return self.data_transfer_service.transfer_logs(*args, **kwargs)
