import os
import sys
import threading
from db import Database
from gui import iniciar_sesion, registrar_usuario, mostrar_catalogo, mostrar_biblioteca, descargar_juego
from errores import UsuarioNoEncontradoError, JuegoNoEncontradoError, IDInvalidoError

def main():
    db = Database()
    db.crear_tablas()
    db.close()

    id_usuario = None
    while not id_usuario:
        os.system('cls')
        print("Bienvenido a Games-Lan")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        choice = input("Seleccione una opción: ")

        if choice == '1':
            registrar_usuario()
        elif choice == '2':
            try:
                id_usuario = iniciar_sesion()
            except UsuarioNoEncontradoError as e:
                print(e)
                print("Redirigiendo al inicio...")
        elif choice == '3':
            print("Saliendo...")
            sys.exit()
        else:
            print("Opción no válida. Intente de nuevo.")

    while True:
        os.system('cls')
        print("=== Menú Principal ===")
        print("1. Mostrar catálogo")
        print("2. Biblioteca de juegos")
        print("3. Descargar un juego")
        print("4. Salir")
        choice = input("Seleccione una opción: ")

        if choice == '1':
            mostrar_catalogo(id_usuario)  
        elif choice == '2':
            mostrar_biblioteca(id_usuario)
        elif choice == '3':
            descargar_juego(id_usuario)
        elif choice == '4':
            print("Saliendo...")
            sys.exit()
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()