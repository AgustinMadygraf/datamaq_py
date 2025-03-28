"""
Path: src/data_transfer_controller.py
"""

import subprocess
import pymysql
import time
from utils.logging.simple_logger import LoggerService
from src.db_operations import SQLAlchemyDatabaseRepository
from src.time_utility import TimeUtility

logger = LoggerService()

class DatabaseConnector:
    "Clase encargada de gestionar la conexión a la base de datos."
    def __init__(self, logger, repository):
        self.logger = logger
        self.repository = repository
    
    def get_connection(self):
        " Obtiene una conexión a la base de datos. "
        conn = self.repository.raw_connection()
        if not conn:
            self.logger.error("No se pudo establecer conexión con la base de datos.")
            return None
        return conn

class BaseDataTransferService:
    "Clase base para los servicios de transferencia de datos."
    def __init__(self, log, repository=None):
        self.logger = log
        self.time_utility = TimeUtility()
        self.db_connector = DatabaseConnector(log, repository)

    def obtener_datos(self, cursor, consulta):
        " Obtiene los datos de la base de datos. "
        try:
            cursor.execute(consulta)
            return cursor.fetchall()
        except pymysql.MySQLError as e:
            self.logger.error("Error de MySQL al ejecutar consulta: %s", e)
        except (TypeError, ValueError) as e:
            self.logger.error("Error al ejecutar consulta: %s", e)
        return None

    def insertar_datos(self, conn, datos, consulta_insercion, num_filas):
        " Inserta los datos en la base de datos. "
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
            
    def check_record_exists(self, conn, table, unixtime):
        " Verifica si ya existe un registro con el mismo unixtime. "
        with conn.cursor() as cursor:
            cursor.execute(
                f"SELECT COUNT(*) FROM {table} WHERE unixtime = %s", 
                (unixtime,)
            )
            result = cursor.fetchone()
            return result and result[0] > 0

class ProductionLogTransferService(BaseDataTransferService):
    "Servicio encargado de transferir los datos de ProductionLog."
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
        "Ejecuta la transferencia de datos para ProductionLog."
        conn = self.db_connector.get_connection()
        if not conn:
            return

        with conn.cursor() as cursor:
            self.logger.info("Iniciando transferencia de ProductionLog.")
            unixtime = TimeUtility.get_unix_time()
            consulta_select, consulta_insert, num_filas = self.get_queries()
            datos_originales = self.obtener_datos(cursor, consulta_select)
            datos = []
            if datos_originales:
                datos = [(unixtime,) + tuple(int(x) for x in fila) for fila in datos_originales]

            if datos:
                # Se verifica que no exista ya un registro para el mismo unixtime.
                if not self.check_record_exists(conn, "ProductionLog", unixtime):
                    self.insertar_datos(conn, datos, consulta_insert, num_filas)
                    conn.commit()
                    self.logger.info("Transferencia de ProductionLog completada exitosamente.")
                else:
                    self.logger.warning("Registro duplicado para unixtime %s.", unixtime)
            else:
                self.logger.warning("No se obtuvieron datos para ProductionLog.")
        conn.close()

class IntervalProductionTransferService(BaseDataTransferService):
    "Servicio encargado de transferir los datos de intervalproduction."
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
        "Ejecuta la transferencia de datos para intervalproduction."
        conn = self.db_connector.get_connection()
        if not conn:
            return

        with conn.cursor() as cursor:
            self.logger.info("Iniciando transferencia de intervalproduction.")
            unixtime = TimeUtility.get_unix_time()
            consulta_select, consulta_insert, num_filas = self.get_queries()
            datos_originales = self.obtener_datos(cursor, consulta_select)
            datos = []
            if datos_originales:
                datos = [(unixtime,) + tuple(int(x) for x in fila) for fila in datos_originales]

            if datos:
                if not self.check_record_exists(conn, "intervalproduction", unixtime):
                    self.insertar_datos(conn, datos, consulta_insert, num_filas)
                    conn.commit()
                    self.logger.info("Transferencia de intervalproduction completada exitosamente.")
                else:
                    self.logger.warning("Registro duplicado para unixtime %s.", unixtime)
            else:
                self.logger.warning("No se obtuvieron datos para intervalproduction.")
        conn.close()

class PHPDataTransferService:
    "Servicio encargado de enviar los datos a través de un script PHP."
    def __init__(self, log, php_interpreter=None, php_script=None):
        self.logger = log
        self.php_interpreter = php_interpreter or "C://AppServ//php7//php.exe"
        self.php_script = php_script or "C://AppServ//www//DataMaq//includes//SendData_python.php"

    def send(self):
        "Ejecuta el script PHP y retorna True si fue exitoso."
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

class TransferScheduler:
    "Responsable de determinar cuándo se debe realizar la transferencia."
    def __init__(self, logger):
        self.logger = logger
        self.time_utility = TimeUtility()
        self.last_transfer_time = 0
        self.transfer_interval = 300
    
    def _is_transfer_time(self) -> bool:
        " Determina si es momento de realizar la transferencia. "
        current_time = int(time.time())
        if self.last_transfer_time == 0 or (current_time - self.last_transfer_time) >= self.transfer_interval:
            self.last_transfer_time = current_time
            return True
        return False
    
    def should_transfer(self) -> bool:
        " Verifica si es momento de transferir los datos."
        self.logger.info(
            "Verificando si es momento de transferir datos: %s",
            "momento adecuado" if self._is_transfer_time() else "aún no es el momento"
        )
        return self._is_transfer_time()
