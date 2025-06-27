from src.db_operations import SQLAlchemyDatabaseRepository

class ModelBase:
    """Clase base para manejar la conexión y operaciones de datos."""
    def __init__(self, repository=None):
        # Permite inyectar cualquier implementación de IDatabaseRepository
        self.repository = repository or SQLAlchemyDatabaseRepository()

    def get_repository(self):
        """Retorna el repositorio para operar con la base de datos."""
        return self.repository

# Mover este archivo a /models en la siguiente validación para consolidar el modelo.
# ...Posibles entidades o métodos adicionales para el modelo...
