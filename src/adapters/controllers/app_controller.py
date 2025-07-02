import time
from src.adapters.controllers.modbus_processor import run_modbus_processing
from src.application.use_cases import main_transfer_controller
from src.adapters.controllers.app_view import clear_screen
from src.adapters.controllers.decorators import log_and_handle_errors
from src.domain.ports.database_repository import IDatabaseRepository  # Para tipado
from src.infrastructure.di.repository_factory import get_database_repository  # Nueva factoría

class AppController:
    def __init__(self, logger=None, repository: IDatabaseRepository = None):
        from src.crosscutting.logging.dependency_injection import get_logger
        self.logger = logger or get_logger()
        self.repository = repository or get_database_repository()  # Usar factoría
        self.running = True

    def setup_signal_handlers(self):
        import signal
        import platform
        current_os = platform.system()
        self.logger.info(f"Sistema operativo detectado: {current_os}")  # Útil para diagnóstico multiplataforma
        self.logger.debug(f"Sistema operativo detectado: {current_os}")
        if current_os != "Windows":
            self.logger.info("Configurando manejadores de señales para sistema Unix")  # Útil solo en Unix
            signal.signal(signal.SIGINT, self.handle_signal)
            signal.signal(signal.SIGTERM, self.handle_signal)
        else:
            self.logger.info("Sistema Windows detectado, se manejará mediante KeyboardInterrupt")  # Útil para usuarios Windows

    def handle_signal(self, signum, _frame):
        self.logger.info(f"Señal {signum} recibida. Terminando el bucle principal...")  # Útil para trazabilidad de apagado
        self.running = False

    @log_and_handle_errors
    def execute_main_operations(self):
        self.logger.debug("Ejecutando iteración del bucle principal.")
        repository = self.repository  # Usar el repositorio inyectado

        def obtener_datos(consulta):
            return repository.ejecutar_consulta(consulta, {})

        def insertar_datos(datos, consulta_insercion, campos):
            for fila in datos:
                parametros = dict(zip(campos, fila))
                repository.actualizar_registro(consulta_insercion, parametros)

        try:
            run_modbus_processing(repository)
            self.logger.info("Procesamiento Modbus ejecutado.")
            main_transfer_controller(self.logger, obtener_datos, insertar_datos, repository)
        except Exception as e:
            self.logger.error(f"Error en operaciones principales: {e}")
        time.sleep(1)
        clear_screen()

    def run(self):
        self.setup_signal_handlers()
        try:
            self.logger.info("Iniciando bucle principal")  # Marca inicio de ciclo principal
            input("Presione Enter para comenzar el bucle principal...")
            while self.running:
                self.execute_main_operations()
        except KeyboardInterrupt:
            self.logger.info("Interrupción (Ctrl+C) recibida. Terminando el bucle principal...")  # Útil para trazabilidad de apagado