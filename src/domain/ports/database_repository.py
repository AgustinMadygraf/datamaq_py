# src/domain/ports/database_repository.py
"""
Puerto de dominio para acceso a base de datos.
Define la interfaz que debe implementar cualquier repositorio de base de datos.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

class IDatabaseRepository(ABC):
    """Interfaz para la clase DatabaseRepository."""
    @abstractmethod
    def obtener_engine(self) -> Any:
        pass

    @abstractmethod
    def ejecutar_consulta(self, consulta: str, parametros: Dict) -> Any:
        pass

    @abstractmethod
    def actualizar_registro(self, consulta: str, parametros: Dict) -> None:
        pass
