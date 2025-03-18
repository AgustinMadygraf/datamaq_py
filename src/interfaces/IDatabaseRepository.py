from abc import ABC, abstractmethod

class IDatabaseRepository(ABC):
    # Define abstract methods as needed by implementations
    @abstractmethod
    def get_db_config(self):
        pass

    @abstractmethod
    def obtener_engine(self) -> any:
        pass

    @abstractmethod
    def raw_connection(self):
        """Retorna una conexión en bruto (DBAPI connection) desde el engine."""
        pass

    @abstractmethod
    def ejecutar_consulta(self, consulta: str, parametros: dict) -> any:
        """Ejecuta una consulta de lectura y retorna sus resultados."""
        pass

    @abstractmethod
    def actualizar_registro(self, consulta: str, parametros: dict) -> None:
        """Ejecuta una consulta de actualización de manera transaccional."""
        pass

    @abstractmethod
    def insertar_lote(self, consulta: str, lista_parametros: list) -> None:
        """Realiza inserciones en lote (batch insert) de manera transaccional."""
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass

    @abstractmethod
    def cerrar_conexion(self) -> None:
        pass
