"""
UnitOfWork: Context manager para transacciones atómicas sobre un repositorio.
"""
from src.interfaces import IDatabaseRepository

class UnitOfWork:
    def __init__(self, repository: IDatabaseRepository):
        self.repository = repository
        self._committed = False

    def __enter__(self):
        return self

    def commit(self):
        self.repository.commit()
        self._committed = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and not self._committed:
            self.commit()
        elif exc_type is not None:
            self.repository.rollback()
        # No suprime excepciones
        return False
