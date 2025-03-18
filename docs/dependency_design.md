# Diseño de Dependencias

## Inyección de la Dependencia en DatabaseConnector

Se ha modificado la clase `DatabaseConnector` para que ya no cree internamente una instancia de `SQLAlchemyDatabaseRepository`, sino que reciba explícitamente una implementación que cumpla con la interfaz `IDatabaseRepository`. De esta manera, se reduce el acoplamiento y se facilita la realización de pruebas unitarias, cumpliendo con el Principio de Inversión de Dependencias (DIP).

- La dependencia se inyecta desde los puntos centrales de la aplicación (por ejemplo, en `main.py`).
- Esto permite intercambiar la implementación del repositorio sin afectar la lógica de conexión ni la transferencia de datos.

...existing documentation...
