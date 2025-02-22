"""
Path: src/models/data_model.py
Este módulo se encarga de manejar los datos de la base de datos.
"""

import pymysql
from src.logs.config_logger import configurar_logging

logger = configurar_logging()

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
