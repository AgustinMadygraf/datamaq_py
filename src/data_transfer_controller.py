"""
Path: src/controllers/data_transfer_controller.py
Este módulo se encarga de controlar la transferencia de datos 
entre la base de datos y el servidor PHP, utilizando una arquitectura
basada en clases que facilita la extensión y el mantenimiento.
"""

import time
from datetime import datetime
import subprocess
import pymysql
from utils.logging.dependency_injection import get_logger
from src.db_operations import SQLAlchemyDatabaseRepository

logger = get_logger()


class BaseDataTransferService:
    """
    Servicio base que contiene métodos comunes para obtener el tiempo UNIX, leer e insertar datos
    en la base de datos.
    """
    def __init__(self, log):
        self.logger = log

    def _get_unix_time(self):
        """
        Calcula el tiempo UNIX redondeado al múltiplo de 300 segundos.
        """
        unixtime = int(time.time())
        return round(unixtime / 300) * 300

    def obtener_datos(self, cursor, consulta):
        """
        Ejecuta la consulta SELECT y retorna los resultados.
        """
        try:
            cursor.execute(consulta)
            return cursor.fetchall()
        except pymysql.MySQLError as e:
            self.logger.error("Error de MySQL al ejecutar consulta: %s", e)
        except (TypeError, ValueError) as e:
            self.logger.error("Error al ejecutar consulta: %s", e)
        return None

    def insertar_datos(self, conn, datos, consulta_insercion, num_filas):
        """
        Inserta los datos en la base de datos usando la consulta de inserción proporcionada.
        """
        try:
            with conn.cursor() as cursor:
                for fila in datos:
                    if len(fila) == num_filas:
                        cursor.execute(consulta_insercion, fila)
                    else:
                        self.logger.warning("Fila con número incorrecto de elementos: %s", fila)
                conn.commit()
                self.logger.info("%s registros insertados con éxito.", len(datos))
        except pymysql.MySQLError as e:
            self.logger.error("Error de MySQL al insertar datos: %s", e)
            conn.rollback()
        except (TypeError, ValueError) as e:
            self.logger.error("Error al insertar datos: %s", e)
            conn.rollback()

class ProductionLogTransferService(BaseDataTransferService):
    """
    Servicio encargado de transferir los datos de ProductionLog.
    """
    def get_queries(self):
        " Establece las consultas SELECT e INSERT para ProductionLog. "
        consulta_select = """
            SELECT
                (SELECT valor FROM registros_modbus WHERE registro = 'HR_COUNTER1_LO') AS HR_COUNTER1_LO, 
                (SELECT valor FROM registros_modbus WHERE registro = 'HR_COUNTER1_HI') AS HR_COUNTER1_HI, 
                (SELECT valor FROM registros_modbus WHERE registro = 'HR_COUNTER2_LO') AS HR_COUNTER2_LO, 
                (SELECT valor FROM registros_modbus WHERE registro = 'HR_COUNTER2_HI') AS HR_COUNTER2_HI;
        """
        consulta_insert = """
            INSERT INTO ProductionLog (unixtime, HR_COUNTER1_LO, HR_COUNTER1_HI, HR_COUNTER2_LO, HR_COUNTER2_HI)
            VALUES (%s, %s, %s, %s, %s)
        """
        num_filas = 5
        return consulta_select, consulta_insert, num_filas

    def transfer(self):
        """
        Ejecuta la transferencia de datos para ProductionLog.
        """
        conn = SQLAlchemyDatabaseRepository()
        # Se obtiene la conexión en bruto si es necesario.
        if not hasattr(conn, "cursor"):
            conn = conn.raw_connection()
        if not conn:
            self.logger.error("No se pudo establecer conexión con la base de datos.")
            return

        with conn.cursor() as cursor:
            self.logger.info("Iniciando transferencia de ProductionLog.")
            unixtime = self._get_unix_time()
            consulta_select, consulta_insert, num_filas = self.get_queries()
            datos_originales = self.obtener_datos(cursor, consulta_select)
            datos = []
            if datos_originales:
                datos = [(unixtime,) + tuple(int(x) for x in fila) for fila in datos_originales]

            if datos:
                # Se verifica que no exista ya un registro para el mismo unixtime.
                cursor.execute(
                    "SELECT COUNT(*) FROM ProductionLog WHERE unixtime = %s", (unixtime,)
                )
                result = cursor.fetchone()
                if result and result[0] == 0:
                    self.insertar_datos(conn, datos, consulta_insert, num_filas)
                    conn.commit()
                    self.logger.info("Transferencia de ProductionLog completada exitosamente.")
                else:
                    self.logger.warning("Registro duplicado para unixtime %s.", unixtime)
            else:
                self.logger.warning("No se obtuvieron datos para ProductionLog.")
        conn.close()

class IntervalProductionTransferService(BaseDataTransferService):
    """
    Servicio encargado de transferir los datos de intervalproduction.
    """
    def get_queries(self):
        " Establece las consultas SELECT e INSERT para intervalproduction. "
        consulta_select = """
            SELECT 
                ((SELECT HR_COUNTER1_LO FROM ProductionLog ORDER BY ID DESC LIMIT 1) - 
                 (SELECT HR_COUNTER1_LO FROM ProductionLog WHERE ID = (SELECT MAX(ID) - 1 FROM ProductionLog))) AS HR_COUNTER1,
                ((SELECT HR_COUNTER2_LO FROM ProductionLog ORDER BY ID DESC LIMIT 1) - 
                 (SELECT HR_COUNTER2_LO FROM ProductionLog WHERE ID = (SELECT MAX(ID) - 1 FROM ProductionLog))) AS HR_COUNTER2
            FROM ProductionLog
            LIMIT 1;
        """
        consulta_insert = """
            INSERT INTO intervalproduction (unixtime, HR_COUNTER1, HR_COUNTER2)
            VALUES (%s, %s, %s)
        """
        num_filas = 3
        return consulta_select, consulta_insert, num_filas

    def transfer(self):
        """
        Ejecuta la transferencia de datos para intervalproduction.
        """
        conn = SQLAlchemyDatabaseRepository()
        if not hasattr(conn, "cursor"):
            conn = conn.raw_connection()
        if not conn:
            self.logger.error("No se pudo establecer conexión para intervalproduction.")
            return

        with conn.cursor() as cursor:
            self.logger.info("Iniciando transferencia de intervalproduction.")
            unixtime = self._get_unix_time()
            consulta_select, consulta_insert, num_filas = self.get_queries()
            datos_originales = self.obtener_datos(cursor, consulta_select)
            datos = []
            if datos_originales:
                datos = [(unixtime,) + tuple(int(x) for x in fila) for fila in datos_originales]

            if datos:
                cursor.execute(
                    "SELECT COUNT(*) FROM intervalproduction WHERE unixtime = %s", 
                    (unixtime,)
                )
                result = cursor.fetchone()
                if result and result[0] == 0:
                    self.insertar_datos(conn, datos, consulta_insert, num_filas)
                    conn.commit()
                    self.logger.info("Transferencia de intervalproduction completada exitosamente.")
                else:
                    self.logger.warning("Registro duplicado para unixtime %s.", unixtime)
            else:
                self.logger.warning("No se obtuvieron datos para intervalproduction.")
        conn.close()

class PHPDataTransferService:
    """
    Servicio encargado de enviar los datos a través de un script PHP.
    """
    def __init__(self, log, php_interpreter=None, php_script=None):
        self.logger = log
        self.php_interpreter = php_interpreter or "C://AppServ//php7//php.exe"
        self.php_script = php_script or "C://AppServ//www//DataMaq//includes//SendData_python.php"

    def send(self):
        """
        Ejecuta el script PHP y retorna True si fue exitoso.
        """
        try:
            result = subprocess.run(
                [self.php_interpreter, self.php_script],
                capture_output=True,
                text=True,
                shell=True,
                check=True
            )
            if result.returncode == 0:
                self.logger.info("Script PHP ejecutado exitosamente. Salida:")
                self.logger.info(result.stdout)
                return True
            else:
                self.logger.error(
                    "Error al ejecutar el script PHP. Código de salida: %s",
                    result.returncode
                )
                self.logger.error("Mensaje de error: %s", result.stderr)
                self.logger.error("Comando ejecutado: %s %s", self.php_interpreter, self.php_script)
                return False
        except subprocess.CalledProcessError as e:
            self.logger.error("Excepción al ejecutar el script PHP: %s", str(e))
            return False

class DataTransferController:
    """
    Controlador que orquesta la transferencia de datos:
      - Verifica si es el momento de transferir (según la hora actual).
      - Ejecuta la transferencia de ProductionLog e intervalproduction.
      - Ejecuta el servicio PHP para enviar los datos.
    """
    def __init__(self, log):
        self.logger = log
        self.production_service = ProductionLogTransferService(log)
        self.interval_service = IntervalProductionTransferService(log)
        self.php_service = PHPDataTransferService(log=log)

    def es_tiempo_cercano_multiplo_cinco(self, tolerancia=5):
        """
        Verifica si el tiempo actual está cercano (dentro de la tolerancia)
        a un múltiplo de 5 minutos.
        """
        ahora = datetime.now()
        minuto_actual = ahora.minute
        segundo_actual = ahora.second
        cercano_a_multiplo = (
            (minuto_actual % 5) <= (tolerancia / 60) and segundo_actual <= tolerancia
        )
        self.logger.info(
            "Chequeando tiempo: %s, cercano a múltiplo de 5: %s",
            ahora, 'sí' if cercano_a_multiplo else 'no'
        )
        return cercano_a_multiplo

    def run_transfer(self):
        """
        Orquesta la transferencia de datos:
          - Si es tiempo de transferencia, ejecuta los tres servicios.
          - De lo contrario, informa que no es el momento.
        """
        if self.es_tiempo_cercano_multiplo_cinco():
            self.logger.info("Iniciando transferencia de datos.")
            self.production_service.transfer()
            self.interval_service.transfer()
            php_success = self.php_service.send()
            if not php_success:
                self.logger.warning(
                    "La transferencia de datos PHP falló, pero el programa continuará ejecutándose."
                )
        else:
            self.logger.info(
                "No es momento de transferir datos. Esperando la próxima verificación."
            )

def main_transfer_controller():
    """
    Función principal que instancia el controlador de transferencia y ejecuta la operación.
    """
    controller = DataTransferController(logger)
    controller.run_transfer()
