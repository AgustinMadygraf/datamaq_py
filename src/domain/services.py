# Servicios de dominio
# Definición de servicios de dominio:
# - Encapsulan reglas de negocio puras.
# - No dependen de infraestructura ni frameworks externos.
# - Operan sobre entidades y objetos de valor del dominio.

# Eliminar clase ProduccionService y su método calcular_eficiencia (no referenciados)

class ProductionLogTransferService:
    """
    Servicio encargado de transferir los datos de ProductionLog.
    """
    def __init__(self, log, repository):
        self.logger = log
        self.repository = repository

    def get_queries(self):
        consulta_select = """
            SELECT
                (SELECT valor FROM registros_modbus WHERE registro = 'HR_COUNTER1_LO') AS HR_COUNTER1_LO, 
                (SELECT valor FROM registros_modbus WHERE registro = 'HR_COUNTER1_HI') AS HR_COUNTER1_HI, 
                (SELECT valor FROM registros_modbus WHERE registro = 'HR_COUNTER2_LO') AS HR_COUNTER2_LO, 
                (SELECT valor FROM registros_modbus WHERE registro = 'HR_COUNTER2_HI') AS HR_COUNTER2_HI;
        """
        consulta_insert = """
            INSERT INTO ProductionLog (unixtime, HR_COUNTER1_LO, HR_COUNTER1_HI, HR_COUNTER2_LO, HR_COUNTER2_HI)
            VALUES (:unixtime, :HR_COUNTER1_LO, :HR_COUNTER1_HI, :HR_COUNTER2_LO, :HR_COUNTER2_HI)
        """
        campos = ["unixtime", "HR_COUNTER1_LO", "HR_COUNTER1_HI", "HR_COUNTER2_LO", "HR_COUNTER2_HI"]
        return consulta_select, consulta_insert, campos

    def transfer(self, unixtime, obtener_datos, insertar_datos):
        try:
            if not self.repository:
                self.logger.error("No se pudo establecer conexión con la base de datos.")
                return
            consulta_select, consulta_insert, campos = self.get_queries()
            datos_originales = obtener_datos(consulta_select)
            datos = []
            if datos_originales:
                datos = [(unixtime,) + tuple(int(x) for x in fila) for fila in datos_originales]
            if datos:
                result = self.repository.ejecutar_consulta(
                    "SELECT COUNT(*) FROM ProductionLog WHERE unixtime = :unixtime", {"unixtime": unixtime}
                )
                if result and result[0][0] == 0:
                    insertar_datos(datos, consulta_insert, campos)
                else:
                    self.logger.warning("Registro duplicado para unixtime %s.", unixtime)
            else:
                self.logger.warning("No se obtuvieron datos para ProductionLog.")
        except Exception as e:
            self.logger.error(f"Error inesperado en la transferencia de ProductionLog: {e}")

class IntervalProductionTransferService:
    """
    Servicio encargado de transferir los datos de intervalproduction.
    """
    def __init__(self, log, repository):
        self.logger = log
        self.repository = repository

    def get_queries(self):
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
            VALUES (:unixtime, :HR_COUNTER1, :HR_COUNTER2)
        """
        campos = ["unixtime", "HR_COUNTER1", "HR_COUNTER2"]
        return consulta_select, consulta_insert, campos

    def transfer(self, unixtime, obtener_datos, insertar_datos):
        try:
            if not self.repository:
                self.logger.error("No se pudo establecer conexión con la base de datos.")
                return
            consulta_select, consulta_insert, campos = self.get_queries()
            datos_originales = obtener_datos(consulta_select)
            datos = []
            if datos_originales:
                datos = [(unixtime,) + tuple(int(x) for x in fila) for fila in datos_originales]
            if datos:
                insertar_datos(datos, consulta_insert, campos)
            else:
                self.logger.warning("No se obtuvieron datos para intervalproduction.")
        except Exception as e:
            self.logger.error(f"Error inesperado en la transferencia de intervalproduction: {e}")
