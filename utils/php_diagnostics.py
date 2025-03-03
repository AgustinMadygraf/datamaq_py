"""
Path: utils/php_diagnostics.py
Utilidades para diagnosticar y resolver problemas con scripts PHP.
"""

import os
import shutil
import subprocess
from utils.logging.dependency_injection import get_logger

logger = get_logger()

def locate_file(filename, start_dir, max_depth=3):
    """
    Busca un archivo recursivamente a partir de un directorio.
    
    Args:
        filename (str): Nombre del archivo a buscar
        start_dir (str): Directorio donde comenzar la búsqueda
        max_depth (int): Profundidad máxima de búsqueda
        
    Returns:
        str: Ruta del archivo encontrado o None si no se encuentra
    """
    logger.info(f"Buscando archivo {filename} a partir de {start_dir}")
    found_paths = []
    
    for root, _, files in os.walk(start_dir):
        # Verificar la profundidad para no buscar demasiado profundo
        rel_path = os.path.relpath(root, start_dir)
        if rel_path.count(os.sep) > max_depth:
            continue
            
        if filename in files:
            file_path = os.path.join(root, filename)
            found_paths.append(file_path)
            logger.info(f"Archivo encontrado: {file_path}")
    
    if found_paths:
        # Retornar la primera coincidencia
        return found_paths[0]
    else:
        logger.warning(f"No se encontró el archivo {filename}")
        return None

def fix_php_include_path(php_script_path, missing_file):
    """
    Intenta arreglar problemas de inclusión de archivos PHP copiando 
    el archivo faltante al directorio del script.
    
    Args:
        php_script_path (str): Ruta al script PHP que tiene problemas
        missing_file (str): Nombre del archivo faltante
        
    Returns:
        bool: True si se pudo solucionar, False en caso contrario
    """
    script_dir = os.path.dirname(php_script_path)
    
    # 1. Comprobar si el archivo ya existe
    target_path = os.path.join(script_dir, missing_file)
    if os.path.exists(target_path):
        logger.info(f"El archivo {missing_file} ya existe en {script_dir}")
        return True
        
    # 2. Buscar el archivo en directorios superiores
    parent_dir = os.path.dirname(script_dir)
    source_path = locate_file(missing_file, parent_dir)
    
    if not source_path:
        # Intentar buscar en toda la estructura de AppServ si no se encuentra
        appserv_dir = "C://AppServ"
        source_path = locate_file(missing_file, appserv_dir)
    
    if source_path:
        try:
            # Copiar el archivo al directorio del script PHP
            shutil.copy2(source_path, target_path)
            logger.info(f"Archivo {missing_file} copiado de {source_path} a {target_path}")
            return True
        except Exception as e:
            logger.error(f"Error al copiar {missing_file}: {str(e)}")
            return False
    
    logger.error(f"No se pudo encontrar el archivo {missing_file} para arreglar el script PHP")
    return False

def create_simple_php_wrapper(php_script_path):
    """
    Crea un script PHP wrapper que incluye el directorio correcto para resolver 
    problemas de inclusión.
    
    Args:
        php_script_path (str): Ruta al script PHP original
        
    Returns:
        str: Ruta al nuevo script wrapper o None si falla
    """
    script_dir = os.path.dirname(php_script_path)
    script_name = os.path.basename(php_script_path)
    wrapper_path = os.path.join(script_dir, f"wrapper_{script_name}")
    
    try:
        with open(wrapper_path, 'w') as f:
            f.write("<?php\n")
            f.write(f"// Auto-generated wrapper to fix include path issues\n")
            f.write(f"chdir('{script_dir.replace('\\', '\\\\')}');\n")
            f.write(f"// Set include path to parent directory as well\n")
            f.write(f"set_include_path(get_include_path() . PATH_SEPARATOR . dirname('{script_dir.replace('\\', '\\\\')}'));\n")
            f.write(f"require_once('{script_name}');\n")
            f.write("?>\n")
            
        logger.info(f"Creado script wrapper en {wrapper_path}")
        return wrapper_path
    except Exception as e:
        logger.error(f"Error al crear script wrapper: {str(e)}")
        return None
