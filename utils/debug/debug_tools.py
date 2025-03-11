"""
Path: utils/debug/debug_tools.py
Herramientas específicas para depuración en desarrollo.
Proporciona utilidades para inspeccionar variables, tiempos de ejecución y más.
"""

import time
import json
import inspect
import traceback
from typing import Any, Dict, List, Optional, Union, Callable
from utils.logging.simple_logger import get_logger, is_debug_verbose, get_debug_level

logger = get_logger()

class DebugTimer:
    """
    Clase para medir tiempos de ejecución con precisión.
    Útil para detectar cuellos de botella.
    """
    _timers: Dict[str, Dict[str, Union[float, int]]] = {}
    
    @classmethod
    def start(cls, name: str) -> None:
        """
        Inicia un cronómetro con el nombre especificado.
        
        Args:
            name: Identificador del cronómetro
        """
        # Always start the timer regardless of debug mode
        cls._timers[name] = {
            'start': time.time(),
            'laps': [],
            'count': 0
        }
        
        # Only log if debug is enabled
        if is_debug_verbose():
            logger.debug(f"Timer '{name}' iniciado")
    
    @classmethod
    def lap(cls, name: str, lap_name: str = None) -> Optional[float]:
        """
        Registra un tiempo parcial para el cronómetro.
        
        Args:
            name: Identificador del cronómetro
            lap_name: Nombre opcional para la vuelta
            
        Returns:
            Tiempo transcurrido desde el inicio o None si el cronómetro no existe
        """
        if name not in cls._timers:
            return None
            
        timer = cls._timers[name]
        current_time = time.time()
        elapsed = current_time - timer['start']
        lap_id = lap_name or f"lap_{len(timer['laps']) + 1}"
        timer['laps'].append((lap_id, elapsed))
        
        if is_debug_verbose():
            logger.debug(f"Timer '{name}' - {lap_id}: {elapsed:.4f}s")
            
        return elapsed
    
    @classmethod
    def stop(cls, name: str) -> float:
        """
        Detiene el cronómetro y devuelve el tiempo transcurrido.
        
        Args:
            name: Identificador del cronómetro
            
        Returns:
            Tiempo total transcurrido o 0.0 si el cronómetro no existe
        """
        if name not in cls._timers:
            return 0.0
            
        timer = cls._timers[name]
        current_time = time.time()
        elapsed = current_time - timer['start']
        timer['elapsed'] = elapsed
        
        # Mostrar resumen sólo en modo debug
        if is_debug_verbose():
            logger.debug(f"Timer '{name}' finalizado: {elapsed:.4f}s")
            if timer['laps']:
                for lap_name, lap_time in timer['laps']:
                    logger.debug(f"  - {lap_name}: {lap_time:.4f}s")
        
        # Always clean up the timer
        cls._timers.pop(name, None)
        
        return elapsed
    
    @classmethod
    def profile(cls, func: Callable) -> Callable:
        """
        Decorador para perfilar el tiempo de ejecución de una función.
        
        Args:
            func: Función a perfilar
            
        Returns:
            Función envuelta con medición de tiempo
        """
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            cls.start(func_name)
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                cls.stop(func_name)
        
        return wrapper


def inspect_variable(var: Any, name: str = "variable", detailed: bool = False) -> None:
    """
    Inspecciona una variable mostrando información detallada.
    
    Args:
        var: Variable a inspeccionar
        name: Nombre para identificar la variable
        detailed: Si es True, muestra información más detallada
    """
    if not is_debug_verbose():
        return
        
    logger.debug(f"Inspección de '{name}' ({type(var).__name__}):")
    
    try:
        # Para objetos simples
        if isinstance(var, (str, int, float, bool)) or var is None:
            logger.debug(f"  Valor: {var}")
            
        # Para listas o tuplas
        elif isinstance(var, (list, tuple)):
            logger.debug(f"  Tipo: {type(var).__name__}, Longitud: {len(var)}")
            if detailed:
                for i, item in enumerate(var[:5]):
                    logger.debug(f"    [{i}]: {item}")
                if len(var) > 5:
                    logger.debug(f"    ... y {len(var) - 5} elementos más")
        
        # Para diccionarios
        elif isinstance(var, dict):
            logger.debug(f"  Tipo: dict, Claves: {len(var)}")
            if detailed:
                for i, (key, value) in enumerate(list(var.items())[:5]):
                    logger.debug(f"    {key}: {value}")
                if len(var) > 5:
                    logger.debug(f"    ... y {len(var) - 5} elementos más")
        
        # Para objetos más complejos
        else:
            logger.debug(f"  Tipo: {type(var).__name__}")
            if detailed:
                try:
                    if hasattr(var, '__dict__'):
                        attrs = vars(var)
                        logger.debug(f"  Atributos: {len(attrs)}")
                        for i, (key, value) in enumerate(list(attrs.items())[:5]):
                            logger.debug(f"    {key}: {value}")
                        if len(attrs) > 5:
                            logger.debug(f"    ... y {len(attrs) - 5} atributos más")
                except:
                    logger.debug("  No se pudo inspeccionar atributos")
    except Exception as e:
        logger.debug(f"Error al inspeccionar '{name}': {e}")


def trace_call_stack(skip_frames: int = 1, max_frames: int = 10) -> None:
    """
    Muestra el stack de llamadas actual para depuración.
    
    Args:
        skip_frames: Número de frames a omitir (empieza por el actual)
        max_frames: Número máximo de frames a mostrar
    """
    if not is_debug_verbose():
        return
        
    stack = inspect.stack()
    logger.debug("Call Stack:")
    
    for i, frame_info in enumerate(stack[skip_frames:skip_frames + max_frames]):
        filename = frame_info.filename
        lineno = frame_info.lineno
        function = frame_info.function
        context = frame_info.code_context[0].strip() if frame_info.code_context else "?"
        
        logger.debug(f"  [{i}] {function} en {filename}:{lineno}")
        logger.debug(f"      {context}")


class ModbusDebug:
    """
    Herramientas específicas para la depuración de operaciones Modbus.
    """
    
    @staticmethod
    def log_register_read(register_address: int, register_value: Any, register_name: str = None) -> None:
        """
        Registra la lectura de un registro Modbus.
        
        Args:
            register_address: Dirección del registro
            register_value: Valor leído
            register_name: Nombre descriptivo del registro
        """
        if not is_debug_verbose():
            return
            
        name_info = f" ({register_name})" if register_name else ""
        logger.debug(f"Modbus READ: Registro 0x{register_address:04X}{name_info} = {register_value}")
    
    @staticmethod
    def log_register_write(register_address: int, register_value: Any, register_name: str = None) -> None:
        """
        Registra la escritura a un registro Modbus.
        
        Args:
            register_address: Dirección del registro
            register_value: Valor escrito
            register_name: Nombre descriptivo del registro
        """
        if not is_debug_verbose():
            return
            
        name_info = f" ({register_name})" if register_name else ""
        logger.debug(f"Modbus WRITE: Registro 0x{register_address:04X}{name_info} = {register_value}")
    
    @staticmethod
    def log_modbus_error(operation: str, register_address: int, error: Exception) -> None:
        """
        Registra un error ocurrido durante una operación Modbus.
        
        Args:
            operation: Tipo de operación (READ, WRITE)
            register_address: Dirección del registro
            error: Excepción ocurrida
        """
        if not is_debug_verbose():
            return
            
        logger.debug(f"Modbus ERROR en {operation}: Registro 0x{register_address:04X}, Error: {error}")
        if get_debug_level() >= 3:
            logger.debug(f"Traceback: {traceback.format_exc()}")
