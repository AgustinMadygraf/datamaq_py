import os
import platform

def clear_screen():
    """Limpia la consola dependiendo del sistema operativo."""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
