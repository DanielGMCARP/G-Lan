#!/usr/bin/env python3
"""
Aplicación GUI de Games-Lan
Interfaz gráfica para la plataforma de juegos Games-Lan
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import InterfazGamesLan

def main():
    """Función principal para ejecutar la aplicación GUI"""
    try:
        
        print("Iniciando Games-Lan GUI...")
        app = InterfazGamesLan()
        app.run()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 