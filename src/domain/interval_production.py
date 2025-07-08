"""
Entidad de dominio: IntervalProduction
Representa los datos de producción en un intervalo de tiempo.
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class IntervalProduction:
    start_time: str
    end_time: str
    produced_units: int
    defective_units: int = 0
    notes: Optional[str] = None
