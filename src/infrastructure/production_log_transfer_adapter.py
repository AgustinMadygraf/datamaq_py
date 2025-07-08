"""
Adaptador para IDataTransferService que utiliza ProductionLogTransferService.
"""
from src.application.interfaces import IDataTransferService
from src.data_transfer_controller import ProductionLogTransferService
from src.utils.logging.dependency_injection import get_logger

class ProductionLogTransferAdapter(IDataTransferService):
    def __init__(self, repository, logger=None):
        self.repository = repository
        self.logger = logger or get_logger()
        self.service = ProductionLogTransferService(self.logger, self.repository)

    def transfer_logs(self, *args, **kwargs):
        """
        Orquesta la transferencia de logs de producción.
        """
        self.service.transfer()
        return {"status": "ok"}
