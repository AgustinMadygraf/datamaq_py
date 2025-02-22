"""
Path: src/db_operations.py
Este script se ocupa de realizar operaciones de base de datos, como actualizaciones y consultas.
"""

import pymysql
from src.logs.config_logger import configurar_logging
import functools
import os
from sqlalchemy import create_engine, text

logger = configurar_logging()

def get_db_engine():
    " Obtiene un objeto de engine de SQLAlchemy para la base de datos."
    config = get_db_config()
    conn_str = f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['db']}"
    engine = create_engine(conn_str, pool_pre_ping=True)
    return engine

def perform_update(connection, address, value):
    " Realiza una actualización en la base de datos."
    query, params = build_update_query(address, value)
    return execute_query(connection, query, params)

def update_database(address, value, descripcion):
    """
    Actualiza un registro en la base de datos con un valor específico.

    Esta función construye y ejecuta una consulta SQL para actualizar un registro en la base de datos.
    Imprime un mensaje indicando si la actualización fue exitosa o no. En caso de errores en la ejecución
    de la consulta, lanza una excepción personalizada `DatabaseUpdateError`.

    Args:
        address (int): La dirección del registro en la base de datos a actualizar.
        value: El valor a asignar en el registro especificado.
        descripcion (str): Descripción del registro para mostrar en mensajes de log.

    Raises:
        DatabaseUpdateError: Si ocurre un error al actualizar la base de datos.

    Returns:
        None
    """
    engine = get_db_engine()
    query, params = build_update_query(address, value)
    try:
        with engine.begin() as conn:
            conn.execute(text(query), params)
        logger.info(f"Registro actualizado: dirección {address}, descripción: {descripcion} valor {value}")
    except Exception as e:
        logger.error(f"Error al actualizar el registro: dirección {address}, {descripcion}: {e}")
        raise DatabaseUpdateError(f"Error al actualizar la base de datos: {e}") from e

def build_update_query(address, value):
    """
    Construye una consulta SQL de actualización y sus parámetros.

    Esta función genera una consulta SQL para actualizar un registro en la tabla 'registros_modbus',
    utilizando la dirección del registro y el nuevo valor a asignar. La consulta se construye de
    manera parametrizada para prevenir inyecciones SQL.

    Args:
        address (int): La dirección del registro en la base de datos a actualizar.
        value: El nuevo valor a asignar en el registro especificado.

    Returns:
        tuple: Una tupla conteniendo la consulta SQL como string y los parámetros como un diccionario.
    """
    query = "UPDATE registros_modbus SET valor = :valor WHERE direccion_modbus = :direccion"
    params = {'valor': value, 'direccion': address}
    return query, params

def execute_query(connection, query, params):
    """
    Ejecuta una consulta SQL en la base de datos especificada.

    Esta función intenta ejecutar una consulta SQL utilizando la conexión y los parámetros proporcionados.
    En caso de éxito, confirma (commit) la transacción. Si ocurre un error durante la ejecución de la consulta,
    imprime un mensaje de error y retorna False.

    Args:
        connection (pymysql.connections.Connection): La conexión activa a la base de datos.
        query (str): La consulta SQL a ejecutar.
        params (tuple): Parámetros para la consulta SQL.

    Returns:
        bool: True si la consulta se ejecuta con éxito, False en caso de error.
    """
    if not connection:
        logger.error("No hay una conexión activa a la base de datos.")
        return False

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()
        return True
    except Exception as e:
        logger.error(f"Error al ejecutar la consulta en la base de datos: {e}")
        return False

def reconnect_on_failure(func):
    """
    Decorador que intenta reconectar a la base de datos en caso de un fallo en la conexión.

    Este decorador envuelve una función que realiza operaciones de base de datos. Si se detecta
    un error de conexión operacional o de MySQL durante la ejecución de la función, intenta
    establecer una nueva conexión y reintentar la operación.

    Args:
        func (function): La función que se va a decorar.

    Returns:
        function: La función envuelta con lógica de manejo de errores y reconexión.
    """
    @functools.wraps(func)
    def wrapper_reconnect(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (pymysql.OperationalError, pymysql.MySQLError) as e:
            print(f"Se detectó un error en la conexión a la base de datos: {e}. Intentando reconectar...")
            try:
                db_config = get_db_config()  # Obtener la configuración actualizada de la base de datos
                connection = pymysql.connect(**db_config)
                args = (connection,) + args[1:]
                return func(*args, **kwargs)
            except Exception as e:
                print(f"No se pudo reconectar a la base de datos: {e}")
                return None
    return wrapper_reconnect


@reconnect_on_failure
def check_db_connection():
    """
    Establece una conexión a la base de datos local o remota.

    Returns:
        sqlalchemy.engine.Engine: Un objeto de engine de SQLAlchemy.
    """
    return get_db_engine()

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
        'db': 'novus',
        'port': 3306  
    }

