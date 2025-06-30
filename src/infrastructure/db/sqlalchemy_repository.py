from src.domain.entities import IDatabaseRepository
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from utils.logging.dependency_injection import get_logger

# Cargamos las variables de entorno desde el archivo .env
load_dotenv()
logger = get_logger()

class DatabaseUpdateError(Exception):
    """Excepción para errores en la actualización de la base de datos."""
    pass

class SQLAlchemyDatabaseRepository(IDatabaseRepository):
    """Implementación de la interfaz IDatabaseRepository utilizando SQLAlchemy."""
    def __init__(self):
        self.engine = self.obtener_engine()
        self.session_local = sessionmaker(bind=self.engine)
        self.session = self.session_local()

    def get_db_config(self):
        try:
            return {
                'host': os.getenv('DB_HOST'),
                'user': os.getenv('DB_USER'),
                'password': os.getenv('DB_PASSWORD'),
                'db': os.getenv('DB_NAME'),
                'port': os.getenv('DB_PORT', '3306')
            }
        except Exception as e:
            logger.error(f"Error al obtener la configuración de la base de datos: {e}")
            raise e

    def obtener_engine(self) -> any:
        try:
            config = self.get_db_config()
            conn_str = (
                f"mysql+pymysql://{config['user']}:{config['password']}@"
                f"{config['host']}:{config['port']}/{config['db']}"
            )
            engine = create_engine(conn_str, pool_pre_ping=True)
            return engine
        except Exception as e:
            logger.error(f"Error al obtener el engine de SQLAlchemy: {e}")
            raise e

    def ejecutar_consulta(self, consulta: str, parametros: dict) -> any:
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
        try:
            self.session.execute(text(consulta), parametros)
            self.session.commit()
            logger.info(
                f"Actualización exitosa con consulta: {consulta} y parámetros: {parametros}"
            )
        except Exception as e:
            self.session.rollback()
            logger.error(
                f"Error actualizando registro con consulta: {consulta} y "
                f"parámetros: {parametros}. Error: {e}"
            )
            raise DatabaseUpdateError(f"Error al actualizar la base de datos: {e}") from e

    def insertar_lote(self, consulta: str, lista_parametros: list) -> None:
        try:
            self.session.execute(text(consulta), lista_parametros)
            self.session.commit()
            logger.info(f"Inserción en lote exitosa con consulta: {consulta}")
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error insertando lote con consulta: {consulta}. Error: {e}")
            raise e

    def commit(self) -> None:
        try:
            self.session.commit()
        except Exception as e:
            logger.error(f"Error al hacer commit: {e}")
            self.session.rollback()
            raise e
