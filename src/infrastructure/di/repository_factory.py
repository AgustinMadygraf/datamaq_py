"""
Factoría para obtener instancias de IDatabaseRepository.
Permite desacoplar la infraestructura de la lógica de aplicación.
"""

from src.domain.ports.database_repository import IDatabaseRepository
from src.infrastructure.db.sqlalchemy_repository import SQLAlchemyDatabaseRepository

def get_database_repository() -> IDatabaseRepository:
    """
    Devuelve una instancia de IDatabaseRepository.
    Por defecto, retorna SQLAlchemyDatabaseRepository.
    """
    return SQLAlchemyDatabaseRepository()
