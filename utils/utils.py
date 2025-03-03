# utils.py
import functools
import pymysql
from src.db_operations import get_db_config  



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
    Establece una conexión a la base de datos utilizando la configuración definida.

    Esta función intenta conectarse a la base de datos utilizando los parámetros especificados
    en la configuración de la base de datos. Está decorada con 'reconnect_on_failure', lo que
    asegura que intentará reconectar automáticamente en caso de fallar la conexión inicial.

    Returns:
        pymysql.connections.Connection: Un objeto de conexión a la base de datos.
    """
    db_config = get_db_config()  # Obtener la configuración de la base de datos
    connection = pymysql.connect(**db_config)
    return connection

