"""
Path: run.py
Punto de entrada principal del programa.
"""

import sys
from src.main import MainApplication

if __name__ == "__main__":
    # Mostrar ayuda si se solicita
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Uso: python run.py [opciones]")
        print("Opciones:")
        print("  --verbose             Activa el modo verbose (mensajes de depuración)")
        sys.exit(0)
        
    app = MainApplication()
    app.run()
