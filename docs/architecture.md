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

---

Actualiza este documento si se agregan nuevas capas, adaptadores o flujos relevantes.
