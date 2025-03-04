"""
Path: src/db_operations.py
Este módulo se encarga de realizar operaciones de lectura y escritura en la base de datos.
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.interfaces import IDatabaseRepository
from utils.logging.dependency_injection import get_logger

logger = get_logger()

class DatabaseUpdateError(Exception):
    """Excepción para errores en la actualización de la base de datos."""
    pass

def get_db_config():
    """
    Obtiene la configuración de la base de datos desde variables de entorno o parámetros.
    Returns:
        dict: Un diccionario con la configuración de la base de datos.
    """
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', '12345678'),
        'db': os.getenv('DB_NAME', 'novus'),
        'port': os.getenv('DB_PORT', '3306')
    }

class SQLAlchemyDatabaseRepository(IDatabaseRepository):
    " Implementación de la interfaz IDatabaseRepository utilizando SQLAlchemy."
    def __init__(self):
        # Inicializa el engine y la sesión utilizando la configuración definida
        self.engine = self.obtener_engine()
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.session = self.SessionLocal()

    def obtener_engine(self) -> any:
        """
        Retorna el objeto engine de SQLAlchemy configurado para la conexión a la base de datos.
        """
        config = get_db_config()
        conn_str = (
            f"mysql+pymysql://{config['user']}:{config['password']}@"
            f"{config['host']}:{config['port']}/{config['db']}"
        )
        engine = create_engine(conn_str, pool_pre_ping=True)
        return engine

    def raw_connection(self):
        """
        Retorna una conexión en bruto (DBAPI connection) desde el engine.
        Esto permite compatibilidad con código legado que utiliza métodos de cursor.
        """
        return self.engine.raw_connection()

    def ejecutar_consulta(self, consulta: str, parametros: dict) -> any:
        """
        Ejecuta una consulta de lectura (SELECT) y retorna los resultados.
        """
        try:
            result = self.session.execute(text(consulta), parametros)
            rows = result.fetchall()
            return rows
        except Exception as e:
            logger.error(
                f"Error ejecutando consulta: {consulta} con parámetros {parametros}. Error: {e}"
            )
            self.session.rollback()
            raise e

    def actualizar_registro(self, consulta: str, parametros: dict) -> None:
        """
        Ejecuta una consulta de actualización (UPDATE) de manera transaccional.
        """
        try:
            self.session.execute(text(consulta), parametros)
            self.session.commit()
            logger.info(
                f"Actualización exitosa con consulta: {consulta} y parámetros: {parametros}"
            )
        except Exception as e:
            self.session.rollback()
            logger.error(
                f"Error actualizando registro con consulta: {consulta} y parámetros: {parametros}. Error: {e}"
            )
            raise DatabaseUpdateError(f"Error al actualizar la base de datos: {e}") from e

    def insertar_lote(self, consulta: str, lista_parametros: list) -> None:
        """
        Realiza inserciones en lote (batch insert) de manera transaccional.
        """
        try:
            self.session.execute(text(consulta), lista_parametros)
            self.session.commit()
            logger.info(f"Inserción en lote exitosa con consulta: {consulta}")
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error insertando lote con consulta: {consulta}. Error: {e}")
            raise e

    def commit(self) -> None:
        """
        Confirma la transacción actual.
        """
        try:
            self.session.commit()
        except Exception as e:
            logger.error(f"Error al hacer commit: {e}")
            self.session.rollback()
            raise e

    def rollback(self) -> None:
        """
        Revierte la transacción actual.
        """
        self.session.rollback()

    def cerrar_conexion(self) -> None:
        """
        Cierra la sesión y la conexión de la base de datos.
        """
        self.session.close()
        self.engine.dispose()
