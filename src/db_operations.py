"""
Path: src/db_operations.py
Implementa la interfaz IDatabaseRepository utilizando SQLAlchemy para operaciones de base de datos.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.interfaces import IDatabaseRepository
from utils.logging.simple_logger import  get_logger

logger = get_logger()

# Verificar si el archivo .env existe
if not os.path.exists('.env'):
    logger.error("El archivo .env no existe. Por favor, cree el archivo .env con la configuración necesaria.")
    while True:
        user_input = input("Escriba 'acepto' para continuar, deberá crear '.env' con las credenciales ")
        if user_input == "acepto":
            break
        else:
            print("Debe aceptar para continuar.")

# Cargamos las variables de entorno desde el archivo .env
load_dotenv()

class SQLAlchemyDatabaseRepository(IDatabaseRepository):
    "Implementación de la interfaz IDatabaseRepository utilizando SQLAlchemy."

    def __init__(self, logger=None):
        self.logger = logger or get_logger()
        self.engine = self.obtener_engine()
        self.session_local = sessionmaker(bind=self.engine)
        self.session = self.session_local()

    def get_db_config(self):
        """
        Obtiene la configuración de la base de datos desde variables de entorno o parámetros.
        
        Returns:
            dict: Un diccionario con la configuración de la base de datos.
        
        Raises:
            ValueError: Si alguno de los valores de configuración esenciales no está definido.
        """
        try:
            # Obtener variables de entorno con validación usando los nombres correctos de .env
            host = os.getenv('DB_SERVER')
            user = os.getenv('DB_USERNAME')
            password = os.getenv('DB_PASSWORD')
            db = os.getenv('DB_NAME')
            port = os.getenv('DB_PORT', '3306')
            
            # Validar que las variables esenciales no son None o vacías
            missing_vars = []
            if not host:
                missing_vars.append('DB_SERVER')
            if not user:
                missing_vars.append('DB_USERNAME')
            if not password:
                missing_vars.append('DB_PASSWORD')
            if not db:
                missing_vars.append('DB_NAME')
            
            if missing_vars:
                error_msg = f"Variables de entorno requeridas no definidas: {', '.join(missing_vars)}"
                self.logger.error(error_msg)
                raise ValueError(error_msg)
            
            return {
                'host': host,
                'user': user,
                'password': password,
                'db': db,
                'port': port
            }
        except Exception as e:
            self.logger.error(f"Error al obtener la configuración de la base de datos: {e}")
            raise e

    def obtener_engine(self) -> any:
        """
        Retorna el objeto engine de SQLAlchemy configurado para la conexión a la base de datos.
        """
        try:
            config = self.get_db_config()
            conn_str = (
                f"mysql+pymysql://{config['user']}:{config['password']}@"
                f"{config['host']}:{config['port']}/{config['db']}"
            )
            engine = create_engine(conn_str, pool_pre_ping=True)
            return engine
        except Exception as e:
            self.logger.error(f"Error al obtener el engine de SQLAlchemy: {e}")
            raise e

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
            self.logger.error(
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
            self.logger.info(
                f"Actualización exitosa con consulta: {consulta} y parámetros: {parametros}"
            )
        except Exception as e:
            self.session.rollback()
            self.logger.error(
                f"Error actualizando registro con consulta: {consulta} y "
                f"parámetros: {parametros}. Error: {e}"
            )
            raise DatabaseUpdateError(f"Error al actualizar la base de datos: {e}") from e

    def insertar_lote(self, consulta: str, lista_parametros: list) -> None:
        """
        Realiza inserciones en lote (batch insert) de manera transaccional.
        """
        try:
            self.session.execute(text(consulta), lista_parametros)
            self.session.commit()
            self.logger.info(f"Inserción en lote exitosa con consulta: {consulta}")
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error insertando lote con consulta: {consulta}. Error: {e}")
            raise e

    def commit(self) -> None:
        """
        Confirma la transacción actual.
        """
        try:
            self.session.commit()
        except Exception as e:
            self.logger.error(f"Error al hacer commit: {e}")
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
        self.logger.info("Conexión cerrada exitosamente")

class DatabaseUpdateError(Exception):
    """Excepción para errores en la actualización de la base de datos."""
    pass
