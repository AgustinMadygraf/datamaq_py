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
        pass

    @abstractmethod
    def ejecutar_consulta(self, consulta: str, parametros: dict) -> any:
        pass

    @abstractmethod
    def actualizar_registro(self, consulta: str, parametros: dict) -> None:
        pass

    @abstractmethod
    def insertar_lote(self, consulta: str, lista_parametros: list) -> None:
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
