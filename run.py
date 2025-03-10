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
        print("  --debug-level=N       Establece el nivel de detalle (1-5, donde 5 es el más detallado)")
        print("  --help, -h            Muestra este mensaje de ayuda")
        sys.exit(0)
        
    app = MainApplication()
    app.run()
