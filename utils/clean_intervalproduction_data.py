import pymysql
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuración de la conexión a la base de datos
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345678',
    'db': 'novus',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}



def calcular_diferenciales(registro_actual, registro_anterior):
    """
    Calcula los diferenciales de `HR_COUNTER1` y `HR_COUNTER2`.
    Muestra cómo se obtuvieron los valores calculados, utilizando las marcas de tiempo
    'datetime' para una mejor claridad.
    """
    diff_hr_counter1 = registro_actual['HR_COUNTER1_LO'] - registro_anterior['HR_COUNTER1_LO']
    diff_hr_counter2 = registro_actual['HR_COUNTER2_LO'] - registro_anterior['HR_COUNTER2_LO']

    # Convertir unixtime a datetime para visualización
    datetime_actual = registro_actual['datetime'].strftime('%Y-%m-%d %H:%M:%S')
    datetime_anterior = registro_anterior['datetime'].strftime('%Y-%m-%d %H:%M:%S')

    # Mostrar cómo se calculó el valor
    print(f"\n\nPara datetime {datetime_actual} (unixtime {registro_actual['unixtime']}):")
    print(f"  - HR_COUNTER1 calculado como diferencia de {registro_actual['HR_COUNTER1_LO']} ({datetime_actual}) - {registro_anterior['HR_COUNTER1_LO']} ({datetime_anterior}) = {diff_hr_counter1}")
    print(f"  - HR_COUNTER2 calculado como diferencia de {registro_actual['HR_COUNTER2_LO']} ({datetime_actual}) - {registro_anterior['HR_COUNTER2_LO']} ({datetime_anterior}) = {diff_hr_counter2}")

    return diff_hr_counter1, diff_hr_counter2


def insertar_registro_intervalproduction(cursor, unixtime, diff_hr_counter1, diff_hr_counter2, guardar_ceros=False):
    """
    Inserta un registro en `intervalproduction` con los diferenciales calculados o con valores cero,
    dependiendo de la elección del usuario.
    """
    # Decidir qué valores insertar basado en la elección del usuario
    valores_a_insertar = (unixtime, 0, 0) if guardar_ceros else (unixtime, diff_hr_counter1, diff_hr_counter2)
    
    sql_insert = """
        INSERT INTO intervalproduction (unixtime, HR_COUNTER1, HR_COUNTER2)
        VALUES (%s, %s, %s)
    """
    cursor.execute(sql_insert, valores_a_insertar)
    if guardar_ceros:
        logging.info(f"Registro con valores cero insertado con éxito para unixtime {unixtime}.")
    else:
        logging.info(f"Registro restituido con éxito para unixtime {unixtime} con diferenciales HR_COUNTER1 = {diff_hr_counter1} y HR_COUNTER2 = {diff_hr_counter2}.")

def obtener_registros_productionlog(cursor):
    """
    Obtiene todos los registros de `productionlog` ordenados por `unixtime` de mayor a menor.
    """
    logging.info("Obteniendo registros de `productionlog` en orden descendente.")
    cursor.execute("SELECT * FROM productionlog ORDER BY unixtime DESC")  # Orden descendente
    return cursor.fetchall()

def restituir_registros():
    try:
        connection = pymysql.connect(**config)
        with connection.cursor() as cursor:
            registros = obtener_registros_productionlog(cursor)

            # Ajuste: invertir el orden de comparación debido al orden descendente de los registros
            for i in range(len(registros) - 1, 0, -1):
                registro_actual = registros[i]
                registro_siguiente = registros[i - 1]  # Ahora 'siguiente' es el registro anterior en tiempo
                diff_hr_counter1, diff_hr_counter2 = calcular_diferenciales(registro_actual, registro_siguiente)
                
                cursor.execute("SELECT COUNT(*) AS count FROM intervalproduction WHERE unixtime = %s", (registro_actual['unixtime'],))
                if cursor.fetchone()['count'] == 0:
                    print(f"Diferenciales calculados: HR_COUNTER1 = {diff_hr_counter1}, HR_COUNTER2 = {diff_hr_counter2}")
                    #respuesta = input("¿Desea insertar este registro en la base de datos con los diferenciales calculados (s) o con valores cero (0)?: ")
                    respuesta = '0'
                    if respuesta.lower() == 's':
                        insertar_registro_intervalproduction(cursor, registro_actual['unixtime'], diff_hr_counter1, diff_hr_counter2)
                    elif respuesta == '0':
                        insertar_registro_intervalproduction(cursor, registro_actual['unixtime'], diff_hr_counter1, diff_hr_counter2, guardar_ceros=True)
            
            connection.commit()
            logging.info("Proceso completado.")
    except pymysql.MySQLError as e:
        logging.error(f"Error de conexión a la base de datos: {e}")
    finally:
        if connection:
            connection.close()
            logging.info("Conexión a la base de datos cerrada.")


restituir_registros()
input("presione enter para salir")