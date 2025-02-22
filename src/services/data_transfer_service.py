"""
Path: src/services/data_transfer_service.py
Este módulo se encarga de realizar la transferencia de datos entre la base de datos y el servidor PHP.
"""

from datetime import datetime
import time
import subprocess
import pymysql
from src.logs.config_logger import configurar_logging
from src.db_operations import check_db_connection
from src.models.data_model import obtener_datos, insertar_datos
from src.models.data_transfer_model import get_production_log_data, get_interval_production_data

logger = configurar_logging()

def transfer_production_log_service():
    conn = check_db_connection()
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
        datos = [(unixtime,) + tuple(int(x) for x in fila) for fila in datos_originales] if datos_originales else []
        if datos:
            cursor.execute("SELECT COUNT(*) FROM intervalproduction WHERE unixtime = %s", (unixtime,))
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
    conn = check_db_connection()
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
        datos = [(unixtime,) + tuple(int(x) for x in fila) for fila in datos_originales] if datos_originales else []
        if datos:
            cursor.execute("SELECT COUNT(*) FROM intervalproduction WHERE unixtime = %s", (unixtime,))
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
    php_interpreter = "C://AppServ//php7//php.exe"
    php_script = "C://AppServ//www//DataMaq//includes//SendData_python.php"
    result = subprocess.run([php_interpreter, php_script], capture_output=True, text=True, shell=True, check=True)
    if result.returncode == 0:
        logger.info("Script PHP ejecutado exitosamente. Salida:")
        logger.info(result.stdout)
    else:
        logger.error("Error al ejecutar el script PHP. Código de salida: %s", result.returncode)
        logger.error(result.stderr)

def transferir_datos_service(consulta1, consulta2, num_filas):
    try:
        conn = check_db_connection()
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
                cursor.execute("SELECT COUNT(*) FROM intervalproduction WHERE unixtime = %s", (unixtime,))
                if cursor.fetchone()[0] == 0:
                    insertar_datos(conn, datos, consulta2, num_filas)
                    conn.commit()
                    logger.info("Transferencia de datos completada exitosamente.")
                else:
                    logger.warning("Se evitó la inserción de un registro duplicado para el unixtime %s.", unixtime)
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
    ahora = datetime.now()
    minuto_actual = ahora.minute
    segundo_actual = ahora.second
    cercano_a_multiplo = minuto_actual % 5 <= tolerancia / 60 and segundo_actual <= tolerancia
    logger.info("Chequeando tiempo: %s, cercano a múltiplo de 5: %s", ahora, 'sí' if cercano_a_multiplo else 'no')
    return cercano_a_multiplo
