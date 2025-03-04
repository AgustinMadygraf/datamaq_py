"""
Path: src/controllers/data_transfer_controller.py
Este script se encarga de controlar la transferencia de datos 
entre la base de datos y el servidor PHP.
"""
from datetime import datetime
import time
import subprocess
import pymysql
from utils.logging.dependency_injection import get_logger
from src.db_operations import SQLAlchemyDatabaseRepository

logger = get_logger()

def main_transfer_controller():
    """Función principal que controla la transferencia de datos entre 
    la base de datos y el servidor PHP."""
    if es_tiempo_cercano_multiplo_cinco_service():
        logger.info("Iniciando transferencia de datos.")
        transfer_production_log_service()
        transfer_interval_production_service()

        # Try to execute PHP script, but continue if it fails
        php_success = send_data_php_service()
        if not php_success:
            logger.warning(
                "La transferencia de datos PHP falló, pero el programa continuará ejecutándose."
            )
    else:
        logger.info("No es momento de transferir datos. Esperando la próxima verificación.")

def transfer_production_log_service():
    " Transfiere los datos de ProductionLog a la base de datos."
    conn = SQLAlchemyDatabaseRepository()
    if not hasattr(conn, "cursor"):
        conn = conn.raw_connection()
    if not conn:
        logger.error("No se pudo establecer conexión con la base de datos.")
        return
    with conn.cursor() as cursor:
        logger.info("Iniciando transferencia de ProductionLog.")
        unixtime = int(time.time())
        unixtime = (round(unixtime / 300)) * 300
        consulta1, consulta2, num_filas = get_production_log_data()
        datos_originales = obtener_datos(cursor, consulta1)
        datos = []
        if datos_originales:
            datos = [(unixtime,) + tuple(int(x) for x in fila) for fila in datos_originales]
        if datos:
            cursor.execute(
                "SELECT COUNT(*) FROM intervalproduction WHERE unixtime = %s", 
                (unixtime,)
            )
            if cursor.fetchone()[0] == 0:
                insertar_datos(conn, datos, consulta2, num_filas)
                conn.commit()
                logger.info("Transferencia de ProductionLog completada exitosamente.")
            else:
                logger.warning("Registro duplicado para unixtime %s.", unixtime)
        else:
            logger.warning("No se obtuvieron datos para ProductionLog.")
    conn.close()

def transfer_interval_production_service():
    "Transfiere los datos de intervalproduction a la base de datos."
    conn = SQLAlchemyDatabaseRepository()
    if not hasattr(conn, "cursor"):
        conn = conn.raw_connection()
    if not conn:
        logger.error("No se pudo establecer conexión para intervalproduction.")
        return
    with conn.cursor() as cursor:
        logger.info("Iniciando transferencia de intervalproduction.")
        unixtime = int(time.time())
        unixtime = (round(unixtime / 300)) * 300
        consulta1, consulta2, num_filas = get_interval_production_data()
        datos_originales = obtener_datos(cursor, consulta1)
        datos = []
        if datos_originales:
            datos = [(unixtime,) + tuple(int(x) for x in fila) for fila in datos_originales]
        if datos:
            cursor.execute(
                "SELECT COUNT(*) FROM intervalproduction WHERE unixtime = %s", 
                (unixtime,)
            )
            if cursor.fetchone()[0] == 0:
                insertar_datos(conn, datos, consulta2, num_filas)
                conn.commit()
                logger.info("Transferencia de intervalproduction completada exitosamente.")
            else:
                logger.warning("Registro duplicado para unixtime %s.", unixtime)
        else:
            logger.warning("No se obtuvieron datos para intervalproduction.")
    conn.close()

def send_data_php_service():
    "Envía los datos a través de un script PHP."
    php_interpreter = "C://AppServ//php7//php.exe"
    php_script = "C://AppServ//www//DataMaq//includes//SendData_python.php"
    try:
        # Removed check=True to prevent exceptions
        result = subprocess.run(
            [php_interpreter, php_script],
            capture_output=True,
            text=True,
            shell=True,
            check=True
        )
        if result.returncode == 0:
            logger.info("Script PHP ejecutado exitosamente. Salida:")
            logger.info(result.stdout)
            return True
        else:
            logger.error("Error al ejecutar el script PHP. Código de salida: %s", result.returncode)
            logger.error("Mensaje de error: %s", result.stderr)
            # Log the command that was run for debugging purposes
            logger.error("Comando ejecutado: %s %s", php_interpreter, php_script)
            return False
    except subprocess.CalledProcessError as e:
        logger.error("Excepción al ejecutar el script PHP: %s", str(e))
        return False

def transferir_datos_service(consulta1, consulta2, num_filas):
    "Transfiere los datos de una consulta a la base de datos."
    try:
        conn = SQLAlchemyDatabaseRepository()
        if not hasattr(conn, "cursor"):
            conn = conn.raw_connection()
        if not conn:
            logger.error("No se pudo establecer conexión con la base de datos.")
            return
        with conn.cursor() as cursor:
            logger.info("Iniciando la transferencia de datos.")
            unixtime = int(time.time())
            unixtime = (round(unixtime / 300)) * 300
            datos_originales = obtener_datos(cursor, consulta1)
            datos = [(unixtime,) + tuple(int(x) for x in fila) for fila in datos_originales]
            if datos:
                cursor.execute(
                    "SELECT COUNT(*) FROM intervalproduction WHERE unixtime = %s", 
                    (unixtime,)
                )
                if cursor.fetchone()[0] == 0:
                    insertar_datos(conn, datos, consulta2, num_filas)
                    conn.commit()
                    logger.info("Transferencia de datos completada exitosamente.")
                else:
                    logger.warning(
                        "Se evitó la inserción de un registro duplicado para el unixtime %s.", 
                        unixtime
                    )
            else:
                logger.warning("No se obtuvieron datos para transferir.")
    except pymysql.MySQLError as e:
        logger.error("Error de MySQL durante la transferencia de datos: %s", e)
        conn.rollback()
    except (TypeError, ValueError) as e:
        logger.error("Error durante la transferencia de datos: %s", e)
        conn.rollback()
    finally:
        if conn:
            conn.close()
            logger.info("Conexión a la base de datos cerrada.")

def es_tiempo_cercano_multiplo_cinco_service(tolerancia=5):
    "Verifica si el tiempo actual está cerca de un múltiplo de cinco minutos."
    ahora = datetime.now()
    minuto_actual = ahora.minute
    segundo_actual = ahora.second
    cercano_a_multiplo = minuto_actual % 5 <= tolerancia / 60 and segundo_actual <= tolerancia
    logger.info(
        "Chequeando tiempo: %s, cercano a múltiplo de 5: %s", 
        ahora,
        'sí' if cercano_a_multiplo else 'no'
    )
    return cercano_a_multiplo

def obtener_datos(cursor, consulta):
    "Obtiene los datos de una consulta."
    try:
        cursor.execute(consulta)
        return cursor.fetchall()
    except pymysql.MySQLError as e:
        logger.error("Error de MySQL al ejecutar consulta: %s", e)
    except (TypeError, ValueError) as e:
        logger.error("Error al ejecutar consulta: %s", e)
    return None

def insertar_datos(conn, datos, consulta2, num_filas):
    "Inserta los datos en la base de datos."
    try:
        with conn.cursor() as cursor:
            for fila in datos:
                if len(fila) == num_filas:
                    cursor.execute(consulta2, fila)
                else:
                    logger.warning("Fila con número incorrecto de elementos: %s", fila)
            conn.commit()
            logger.info("%s registros insertados con éxito.", len(datos))
    except pymysql.MySQLError as e:
        logger.error("Error de MySQL al insertar datos: %s", e)
        conn.rollback()
    except (TypeError, ValueError) as e:
        logger.error("Error al insertar datos: %s", e)
        conn.rollback()

def get_production_log_data():
    """
    Retorna la consulta SELECT, INSERT y el número esperado de elementos para ProductionLog.
    """
    consulta1 = """
            SELECT
                (SELECT valor FROM registros_modbus WHERE registro = 'HR_COUNTER1_LO') AS HR_COUNTER1_LO, 
                (SELECT valor FROM registros_modbus WHERE registro = 'HR_COUNTER1_HI') AS HR_COUNTER1_HI, 
                (SELECT valor FROM registros_modbus WHERE registro = 'HR_COUNTER2_LO') AS HR_COUNTER2_LO, 
                (SELECT valor FROM registros_modbus WHERE registro = 'HR_COUNTER2_HI') AS HR_COUNTER2_HI;
    """
    consulta2 = """
            INSERT INTO ProductionLog (unixtime, HR_COUNTER1_LO, HR_COUNTER1_HI, HR_COUNTER2_LO, HR_COUNTER2_HI)
            VALUES (%s, %s, %s, %s, %s)
    """
    num_filas = 5
    return consulta1, consulta2, num_filas

def get_interval_production_data():
    """
    Retorna la consulta SELECT, INSERT y el número esperado de elementos para intervalproduction.
    """
    consulta1 = """
            SELECT 
                ((SELECT HR_COUNTER1_LO FROM ProductionLog ORDER BY ID DESC LIMIT 1) - 
                (SELECT HR_COUNTER1_LO FROM ProductionLog WHERE ID = (SELECT MAX(ID) - 1 FROM ProductionLog))) AS HR_COUNTER1,
                ((SELECT HR_COUNTER2_LO FROM ProductionLog ORDER BY ID DESC LIMIT 1) - 
                (SELECT HR_COUNTER2_LO FROM ProductionLog WHERE ID = (SELECT MAX(ID) - 1 FROM ProductionLog))) AS HR_COUNTER2
            FROM ProductionLog
            LIMIT 1;
    """
    consulta2 = """
            INSERT INTO intervalproduction (unixtime, HR_COUNTER1, HR_COUNTER2)
            VALUES (%s, %s, %s)
    """
    num_filas = 3
    return consulta1, consulta2, num_filas
