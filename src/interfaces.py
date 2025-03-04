"""
Path: src/interfaces.py
Este script define la interfaz de la clase DatabaseRepository.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Dict

class IDatabaseRepository(ABC):
    " Interfaz para la clase DatabaseRepository."
    @abstractmethod
    def obtener_engine(self) -> Any:
        """
        Retorna el objeto engine de SQLAlchemy configurado para la conexión a la base de datos.
        """
        pass

    @abstractmethod
    def ejecutar_consulta(self, consulta: str, parametros: Dict) -> Any:
        """
        Ejecuta una consulta de lectura (SELECT) y retorna los resultados.
        
        Args:
            consulta (str): La consulta SQL a ejecutar.
            parametros (Dict): Diccionario de parámetros para la consulta.
            
        Returns:
            Any: Los resultados de la consulta.
        """
        pass

    @abstractmethod
    def actualizar_registro(self, consulta: str, parametros: Dict) -> None:
        """
        Ejecuta una consulta de actualización (UPDATE) de manera transaccional.
        
        Args:
            consulta (str): La consulta SQL de actualización.
            parametros (Dict): Diccionario de parámetros para la consulta.
        """
        pass

    @abstractmethod
    def insertar_lote(self, consulta: str, lista_parametros: List[Dict]) -> None:
        """
        Realiza inserciones en lote (batch insert) de manera transaccional.
        
        Args:
            consulta (str): La consulta SQL para la inserción.
            lista_parametros (List[Dict]): Una lista de diccionarios
            con los parámetros para cada inserción.
        """
        pass

    @abstractmethod
    def commit(self) -> None:
        """
        Confirma la transacción actual.
        """
        pass

    @abstractmethod
    def rollback(self) -> None:
        """
        Revierte la transacción actual.
        """
        pass

    @abstractmethod
    def cerrar_conexion(self) -> None:
        """
        Cierra la conexión o finaliza la sesión de la base de datos, liberando los recursos.
        """
        pass
