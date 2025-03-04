# src/db_operations.py
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

    def ejecutar_consulta(self, consulta: str, parametros: dict) -> any:
        """
        Ejecuta una consulta de lectura (SELECT) y retorna los resultados.
        """
        try:
            result = self.session.execute(text(consulta), parametros)
            rows = result.fetchall()
            return rows
        except Exception as e:
            logger.error(f"Error ejecutando consulta: {consulta} con parámetros {parametros}. Error: {e}")
            self.session.rollback()
            raise e

    def actualizar_registro(self, consulta: str, parametros: dict) -> None:
        """
        Ejecuta una consulta de actualización (UPDATE) de manera transaccional.
        """
        try:
            self.session.execute(text(consulta), parametros)
            self.session.commit()
            logger.info(f"Actualización exitosa con consulta: {consulta} y parámetros: {parametros}")
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error actualizando registro con consulta: {consulta} y parámetros: {parametros}. Error: {e}")
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

# Funciones auxiliares para construir consultas específicas

def build_update_query(address, value):
    """
    Construye una consulta SQL de actualización para la tabla 'registros_modbus'.
    """
    consulta = "UPDATE registros_modbus SET valor = :valor WHERE direccion_modbus = :direccion"
    parametros = {'valor': value, 'direccion': address}
    return consulta, parametros

# Capa de compatibilidad para mantener la API antigua

# Se crea una instancia global del repositorio para utilizarla en las funciones legacy
repository_instance = SQLAlchemyDatabaseRepository()

def check_db_connection():
    """
    Función de compatibilidad que retorna la instancia del repositorio.
    """
    return repository_instance

def update_database(address, value, descripcion):
    """
    Función de compatibilidad que utiliza el repositorio para actualizar un registro.
    """
    consulta, parametros = build_update_query(address, value)
    try:
        repository_instance.actualizar_registro(consulta, parametros)
        logger.info(
            f"Registro actualizado: dirección {address}, descripción: {descripcion}, valor {value}"
        )
    except Exception as e:
        logger.error(f"Error al actualizar el registro: dirección {address}, {descripcion}: {e}")
        raise DatabaseUpdateError(f"Error al actualizar la base de datos: {e}") from e
