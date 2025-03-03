import csv
import pymysql
import datetime
from db_operations import check_db_connection, execute_query

# Ruta al archivo CSV
csv_file_path = r'C:\AppServ\www\DataMaq\database\intervalproduction_d.csv'

def excel_date_to_unix(date_serial, excel_epoch=datetime.datetime(1899, 12, 30)):
    """
    Convierte una fecha serial de Excel a Unix time.

    Args:
        date_serial (int): La fecha serial de Excel.
        excel_epoch (datetime.datetime): La época desde la que Excel cuenta los días.

    Returns:
        int: La fecha en formato Unix time.
    """
    date = excel_epoch + datetime.timedelta(days=date_serial)
    unixtime = int(date.timestamp())
    return unixtime

def load_csv_to_mysql(csv_path):
    # Establecer conexión a la base de datos
    connection = check_db_connection()
    if connection is None:
        print("Error al conectar con la base de datos.")
        return
    
    # Abrir el archivo CSV
    with open(csv_path, mode='r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            # Convertir de fecha de Excel a Unix time
            fecha = int(row['Fecha'])  # Asegúrate de que 'Fecha' es un entero
            unixtime = excel_date_to_unix(fecha)  # Conversión aquí
            hr_counter1 = row['HR_COUNTER1']
            hr_counter2 = row['HR_COUNTER2']
            
            # Preparar la sentencia SQL
            query = "INSERT INTO intervalproduction_d (unixtime, HR_COUNTER1, HR_COUNTER2) VALUES (%s, %s, %s)"
            params = (unixtime, hr_counter1, hr_counter2)
            
            # Ejecutar la consulta
            if not execute_query(connection, query, params):
                print(f"Error al insertar el registro {unixtime, hr_counter1, hr_counter2}")
    
    # Cerrar la conexión
    connection.close()

# Llamada a la función
load_csv_to_mysql(csv_file_path)
