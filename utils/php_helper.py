"""
Path: utils/php_helper.py
Este módulo contiene funciones auxiliares para interactuar con PHP y diagnosticar problemas.
"""

import os
import subprocess
from utils.logging.dependency_injection import get_logger

logger = get_logger()

def check_php_installation(php_path="C://AppServ//php7//php.exe"):
    """
    Verifica si la instalación de PHP es correcta ejecutando php -v
    
    Args:
        php_path: Ruta al intérprete de PHP
        
    Returns:
        bool: True si PHP está correctamente instalado, False en caso contrario
    """
    try:
        if not os.path.exists(php_path):
            logger.error("El intérprete PHP no existe en la ruta: %s", php_path)
            return False
            
        result = subprocess.run(
            [php_path, "-v"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            logger.info("Instalación PHP verificada correctamente: %s", result.stdout.splitlines()[0])
            return True
        else:
            logger.error("Error al verificar PHP. Código: %s, Error: %s", 
                         result.returncode, result.stderr)
            return False
    except Exception as e:
        logger.error("Error al verificar la instalación de PHP: %s", str(e))
        return False

def check_php_script_exists(script_path="C://AppServ//www//DataMaq//includes//SendData_python.php"):
    """
    Verifica si el script PHP existe
    
    Args:
        script_path: Ruta al script PHP
        
    Returns:
        bool: True si el script existe, False en caso contrario
    """
    if os.path.exists(script_path):
        logger.info("Script PHP encontrado en: %s", script_path)
        return True
    else:
        logger.error("Script PHP no encontrado en: %s", script_path)
        return False

def retry_php_execution(php_path, script_path, max_attempts=3):
    """
    Intenta ejecutar un script PHP varias veces antes de darse por vencido
    
    Args:
        php_path: Ruta al intérprete PHP
        script_path: Ruta al script PHP
        max_attempts: Número máximo de intentos
        
    Returns:
        bool: True si la ejecución tuvo éxito, False en caso contrario
    """
    for attempt in range(1, max_attempts + 1):
        try:
            logger.info("Intento %d de %d para ejecutar script PHP", attempt, max_attempts)
            result = subprocess.run(
                [php_path, script_path],
                capture_output=True,
                text=True,
                timeout=30,
                shell=True
            )
            
            if result.returncode == 0:
                logger.info("Script PHP ejecutado exitosamente en el intento %d", attempt)
                return True
            else:
                logger.warning("Falló el intento %d. Código: %s, Error: %s", 
                               attempt, result.returncode, result.stderr)
        except Exception as e:
            logger.warning("Excepción en el intento %d: %s", attempt, str(e))
            
        # Esperar un poco más en cada intento fallido
        if attempt < max_attempts:
            import time
            time.sleep(2 * attempt)
    
    logger.error("Todos los intentos de ejecución del script PHP fallaron")
    return False
