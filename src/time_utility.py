"""
Path: src/time_utility.py
"""

import time
from datetime import datetime

class TimeUtility:
    """
    Utilidad para manejar operaciones relacionadas con el tiempo.
    Sigue el principio de responsabilidad única (SRP) al extraer esta funcionalidad.
    """
    @staticmethod
    def get_unix_time():
        """
        Calcula el tiempo UNIX redondeado al múltiplo de 300 segundos.
        """
        unixtime = int(time.time())
        return round(unixtime / 300) * 300
    
    @staticmethod
    def is_near_five_minute_multiple(tolerance=5):
        """
        Verifica si el tiempo actual está cercano (dentro de la tolerancia)
        a un múltiplo de 5 minutos.
        """
        now = datetime.now()
        current_minute = now.minute
        current_second = now.second
        near_multiple = (
            (current_minute % 5) <= (tolerance / 60) and current_second <= tolerance
        )
        return near_multiple, now
