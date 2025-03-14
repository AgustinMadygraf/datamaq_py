# Diseño Inicial del Contenedor de Dependencias

## 1. Análisis del flujo actual
- El AppController crea internamente el ModbusConnectionManager, SQLAlchemyDatabaseRepository y DataTransferController.
- Cada módulo (modbus_connection_manager, modbus_processor, data_transfer_controller) recibe su logger en el constructor, lo que facilita la inyección.

## 2. Propuesta de inyección
- Extraer la creación de dependencias para centralizarla en un módulo (p.ej. src/container.py).
- Modificar el AppController para que reciba las dependencias ya creadas (logger, connection manager, repositorio y controlador de transferencias) en su constructor.

## 3. Beneficios
- Mayor modularidad y facilidad de pruebas.
- Organización centralizada de la configuración y creación de instancias.

## 4. Esquema de Inyección de Dependencias
- Instanciación centralizada en src/container.py.
- Inyección de logger, ModbusConnectionManager, SQLAlchemyDatabaseRepository y DataTransferController en AppController.
- Para operaciones específicas (lectura Modbus y actualización en BD), se propone definir métodos fábrica que permitan inyectar implementaciones alternativas (por ejemplo, para pruebas).
