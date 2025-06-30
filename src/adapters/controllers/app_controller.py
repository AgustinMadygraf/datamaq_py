import time
from src.adapters.controllers.modbus_processor import run_modbus_processing
from src.application.use_cases import main_transfer_controller
from src.adapters.controllers.app_view import clear_screen
from src.infrastructure.db.sqlalchemy_repository import SQLAlchemyDatabaseRepository
from src.adapters.controllers.decorators import log_and_handle_errors

class AppController:
    def __init__(self, logger=None):
        from utils.logging.dependency_injection import get_logger
        self.logger = logger or get_logger()
        self.running = True

    def setup_signal_handlers(self):
        import signal
        import platform
        current_os = platform.system()
        self.logger.info(f"Sistema operativo detectado: {current_os}")
        self.logger.debug(f"Sistema operativo detectado: {current_os}")
        if current_os != "Windows":
            self.logger.info("Configurando manejadores de señales para sistema Unix")
            signal.signal(signal.SIGINT, self.handle_signal)
            signal.signal(signal.SIGTERM, self.handle_signal)
        else:
            self.logger.info("Sistema Windows detectado, se manejará mediante KeyboardInterrupt")

    def handle_signal(self, signum, _frame):
        self.logger.info(f"Señal {signum} recibida. Terminando el bucle principal...")
        self.running = False

    @log_and_handle_errors
    def execute_main_operations(self):
        self.logger.debug("Ejecutando iteración del bucle principal.")
        repository = SQLAlchemyDatabaseRepository()

        def obtener_datos(consulta):
            return repository.ejecutar_consulta(consulta, {})

        def insertar_datos(datos, consulta_insercion, campos):
            for fila in datos:
                parametros = dict(zip(campos, fila))
                repository.actualizar_registro(consulta_insercion, parametros)

        try:
            run_modbus_processing()
            print("")
            main_transfer_controller(self.logger, obtener_datos, insertar_datos, repository)
        except Exception as e:
            self.logger.error(f"Error en operaciones principales: {e}")
        time.sleep(1)
        clear_screen()

    def run(self):
        self.setup_signal_handlers()
        try:
            self.logger.info("Iniciando bucle principal")
            input("Presione Enter para comenzar el bucle principal...")
            while self.running:
                self.execute_main_operations()
        except KeyboardInterrupt:
            self.logger.info("Interrupción (Ctrl+C) recibida. Terminando el bucle principal...")