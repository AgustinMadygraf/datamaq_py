# Arquitectura de DigiRail

## Visión General
DigiRail sigue los principios de Arquitectura Limpia, separando responsabilidades en capas bien definidas para facilitar la mantenibilidad, escalabilidad y testeo.

## Capas y Responsabilidades

- **Infraestructura**: Entrypoint, configuración, frameworks, detalles de base de datos.
  - `run.py`, `src/config.py`, `src/infrastructure/db/sqlalchemy_repository.py`
- **Interface Adapters**: Adaptadores, controladores, vistas, gateways a hardware.
  - `src/adapters/controllers/`, `src/adapters/controllers/app_view.py`, `src/adapters/controllers/modbus_processor.py`
- **Application**: Casos de uso, lógica de orquestación de procesos.
  - `src/application/use_cases.py`
- **Domain**: Entidades de negocio, interfaces de repositorio, lógica de dominio.
  - `src/domain/entities.py`, `src/domain/services.py`

## Flujo de Dependencias
```
(UI / Infraestructura) → (Adaptadores) → (Aplicación) → (Dominio)
```
Las dependencias siempre fluyen hacia adentro. Las capas internas no conocen detalles de las externas.

## Ejemplo de flujo de dependencias desacoplado

```
[Infraestructura]
  SQLAlchemyDatabaseRepository
        │
        ▼
[Adaptador]
  AppController
        │
        ▼
[Aplicación]
  DataTransferController (usa IDatabaseRepository)
        │
        ▼
[Dominio]
  IDatabaseRepository (puerto)
```

- Para agregar una nueva infraestructura (ej. otro motor DB), implementar `IDatabaseRepository` y pasar la instancia en el punto de entrada.
- Los casos de uso y controladores nunca deben importar implementaciones concretas, solo la interfaz.

## Preocupaciones Transversales
- Logging y manejo de errores centralizados mediante decoradores en adaptadores.
- Configuración centralizada en `src/config.py`.

## Puntos de Entrada
- `run.py` inicia la aplicación y delega en `MainApplication`.
- `AppController` orquesta el ciclo principal y delega en adaptadores y casos de uso.

## Notas de Evolución
- El acceso a base de datos está unificado en `sqlalchemy_repository.py`.
- El código muerto y duplicado ha sido eliminado.
- La lógica de grabación periódica está centralizada y desacoplada.
- Se eliminaron clases y métodos no referenciados en Application y Domain (`TransferirDatosCasoUso`, `ProduccionService`).
- El adaptador Modbus ahora implementa una función real de lectura (`process_modbus_operations`).

## [2025-06-30] Refactor: Inversión de Dependencias Application → Infrastructure

- La capa Application (`use_cases.py`) ahora depende solo de la interfaz `IDatabaseRepository` definida en Domain.
- La implementación concreta (`SQLAlchemyDatabaseRepository`) se inyecta desde el punto de entrada (`AppController`).
- Se eliminó el import directo de infraestructura en Application.
- Cumple Clean Architecture: Application es independiente de detalles de infraestructura.

---

Actualiza este documento si se agregan nuevas capas, adaptadores o flujos relevantes.
