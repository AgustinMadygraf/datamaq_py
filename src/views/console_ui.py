"""
Path: src/views/console_ui.py
Módulo que centraliza la lógica de presentación en consola.
Proporciona funciones para mostrar mensajes formateados y controlar la consola.
"""

import os
import platform
import time
from typing import Optional
from utils.logging.simple_logger import is_debug_verbose

# Colores ANSI para la consola (compatible con sistemas Unix/Linux)
COLORS = {
    "RESET": "\033[0m",
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "BLUE": "\033[94m",
    "MAGENTA": "\033[95m",
    "CYAN": "\033[96m",
    "WHITE": "\033[97m",
    "GRAY": "\033[90m",
}

def clear_screen() -> None:
    """Limpia la consola dependiendo del sistema operativo."""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def print_color(text: str, color: str = "WHITE") -> None:
    """
    Imprime texto coloreado en la consola si el sistema lo soporta.
    
    Args:
        text: Texto a mostrar
        color: Color a utilizar (debe ser una clave válida en COLORS)
    """
    # En Windows sin ANSI support, mostrar el texto sin color
    if platform.system() == "Windows" and os.name == "nt":
        print(text)
    else:
        color_code = COLORS.get(color.upper(), COLORS["WHITE"])
        print(f"{color_code}{text}{COLORS['RESET']}")

def show_error(message: str) -> None:
    """Muestra un mensaje de error en la consola."""
    print_color(f"ERROR: {message}", "RED")

def show_warning(message: str) -> None:
    """Muestra un mensaje de advertencia en la consola."""
    print_color(f"ADVERTENCIA: {message}", "YELLOW")

def show_success(message: str) -> None:
    """Muestra un mensaje de éxito en la consola."""
    print_color(f"ÉXITO: {message}", "GREEN")

def show_info(message: str) -> None:
    """Muestra un mensaje informativo en la consola."""
    print_color(f"INFO: {message}", "BLUE")

def show_processing(message: str) -> None:
    """Muestra un mensaje de procesamiento en la consola."""
    print_color(f"PROCESANDO: {message}", "CYAN")

def show_header(title: str) -> None:
    """Muestra un encabezado en la consola."""
    width = 60
    print_color("=" * width, "CYAN")
    print_color(f"{title.center(width)}", "CYAN")
    print_color("=" * width, "CYAN")

def pause(message: str = "Presione Enter para continuar...") -> None:
    """Pausa la ejecución hasta que el usuario presione Enter."""
    input(message)

def show_progress(current: int, total: int, prefix: str = "", suffix: str = "", length: int = 50) -> None:
    """
    Muestra una barra de progreso en la consola.
    
    Args:
        current: Valor actual del progreso
        total: Valor total para completar
        prefix: Texto antes de la barra
        suffix: Texto después de la barra
        length: Longitud de la barra en caracteres
    """
    percent = float(current) * 100 / total
    filled_length = int(length * current // total)
    bar = "█" * filled_length + "▒" * (length - filled_length)
    print_color(f"\r{prefix} |{bar}| {percent:.1f}% {suffix}", "BLUE")
    if current == total: 
        print()

def show_debug(message: str) -> None:
    """
    Muestra un mensaje de depuración en la consola solo si el modo verbose está activado.
    
    Args:
        message: Mensaje a mostrar
    """
    if is_debug_verbose():
        print_color(f"DEBUG: {message}", "GRAY")
