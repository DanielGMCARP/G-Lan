#!/usr/bin/env python3
"""
Games-Lan GUI Application
Interfaz gráfica para la plataforma de juegos Games-Lan
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import GamesLanGUI

def main():
    """Función principal para ejecutar la aplicación GUI"""
    try:
        print("Iniciando Games-Lan GUI...")
        app = GamesLanGUI()
        app.run()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 