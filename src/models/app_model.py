from src.infrastructure.db.sqlalchemy_repository import SQLAlchemyDatabaseRepository

class ModelBase:
    """Clase base para manejar la conexión y operaciones de datos."""
    def __init__(self, repository=None):
        # Permite inyectar cualquier implementación de IDatabaseRepository
        self.repository = repository or SQLAlchemyDatabaseRepository()

    def get_repository(self):
        """Retorna el repositorio para operar con la base de datos."""
        return self.repository

# ...Posibles entidades o métodos adicionales para el modelo...