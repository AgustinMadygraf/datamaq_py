"""
Entidad de dominio: ProductionCounter
Representa un contador de producción industrial.
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class ProductionCounter:
    id: int
    count: int
    timestamp: Optional[str] = None
    description: Optional[str] = None
