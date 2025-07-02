# Convenciones y Nombres para Módulos (Clean Architecture)

## 1. Dominio (`domain/`)
- `entities/`: Clases de negocio puras (ej: `Machine`, `User`)
- `value_objects/`: Objetos inmutables con lógica de validación (ej: `Email`, `SerialNumber`)
- `exceptions/`: Excepciones específicas del dominio (ej: `InvalidMachineStateError`)

## 2. Aplicación (`application/`)
- `use_cases/`: Casos de uso (ej: `CreateMachineUseCase`, `AuthenticateUserUseCase`)
- `ports/`: Interfaces/puertos para dependencias externas (ej: `IMachineRepository`, `IUserRepository`)
- `dtos/`: Objetos de transferencia de datos entre capas (ej: `MachineDTO`, `UserDTO`)

## 3. Infraestructura (`infrastructure/`)
- `repositories/`: Implementaciones concretas de puertos (ej: `SQLAlchemyMachineRepository`)
- `orm/`: Modelos y mapeos ORM (ej: `MachineModel`, `UserModel`)
- `config/`: Configuración de base de datos, logging, etc.

## 4. Interfaces (`interfaces/`)
- `api/`: Adaptadores de entrada/salida (ej: controladores FastAPI, Flask, etc.)
- `ui/`: Adaptadores de interfaz de usuario (web, CLI, etc.)

## 5. Nomenclatura General
- Prefijar interfaces con "I" (ej: `IMachineRepository`)
- Sufijar implementaciones concretas (ej: `SQLAlchemyMachineRepository`)
- Usar PascalCase para clases y snake_case para archivos
- DTOs y UseCases deben ser explícitos en su propósito
