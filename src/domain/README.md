# Dominio (`domain`)

Este directorio contiene las entidades, value objects, agregados y servicios de dominio puro del sistema.

## Propósito
- Representar el núcleo del negocio, libre de dependencias hacia infraestructura, frameworks o detalles externos.
- Centralizar la lógica y reglas de negocio fundamentales.
- Facilitar la mantenibilidad, testeo y evolución del modelo de dominio.

## Contenido esperado
- Entidades (por ejemplo: ModbusRegister, ProductionCounter, IntervalProduction)
- Value Objects
- Agregados
- Servicios de dominio (lógica de negocio pura)

## Notas
- No debe haber dependencias hacia capas de aplicación, infraestructura o adaptadores.
- Cualquier cambio en este directorio debe ser revisado para asegurar su pureza y alineación con la arquitectura limpia.
