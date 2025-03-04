class DeviceModel:
    """Entidad que representa un dispositivo Modbus."""

    def __init__(self, device_id: int, name: str, status: str):
        self.device_id = device_id
        self.name = name
        self.status = status

    def to_dict(self):
        """Convierte la entidad a un diccionario."""
        return {
            "device_id": self.device_id,
            "name": self.name,
            "status": self.status
        }

    # Posibles métodos adicionales...
