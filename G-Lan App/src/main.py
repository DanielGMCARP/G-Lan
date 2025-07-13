import os
import sys
import threading
import multiprocessing
import time
from bd.db import BaseDatos
from gui import iniciar_sesion, registrar_usuario, mostrar_catalogo, mostrar_biblioteca, descargar_juego
from errores import UsuarioNoEncontradoError, JuegoNoEncontradoError, IDInvalidoError
from dal import crear_usuario, verificar_usuario
from log import descarga_con_barra

hilo_descarga_activo = None
hilo_lock = threading.Lock()

def proceso_backup():
    print('[PROCESO HIJO] Backup automático ejecutándose...')
    print(f'[PROCESO HIJO] PID: {os.getpid()}')
    print(f'[PROCESO HIJO] PID del padre: {os.getppid()}')
    time.sleep(2)
    print('[PROCESO HIJO] Backup finalizado.')

def proceso_notificacion(nombre_usuario):
    print(f'[PROCESO HIJO] ¡Bienvenido, {nombre_usuario}! (Notificación especial)')
    print(f'[PROCESO HIJO] PID: {os.getpid()}')
    print(f'[PROCESO HIJO] PID del padre: {os.getppid()}')
    time.sleep(1)
    print('[PROCESO HIJO] Notificación mostrada.')

def proceso_registro(nombre, gmail, contrasena, q):
    print('[PROCESO HIJO] Registro de usuario')
    print(f'[PROCESO HIJO] PID: {os.getpid()}')
    print(f'[PROCESO HIJO] PID del padre: {os.getppid()}')
    if not nombre or not gmail or not contrasena:
        q.put((False, "Todos los campos son obligatorios."))
        return
    resultado = crear_usuario(nombre, gmail, contrasena)
    if resultado:
        q.put((True, "Usuario registrado exitosamente."))
    else:
        q.put((False, "Error: El correo ya está registrado."))

def proceso_login(gmail, contrasena, q):
    print('[PROCESO HIJO] Inicio de sesión')
    print(f'[PROCESO HIJO] PID: {os.getpid()}')
    print(f'[PROCESO HIJO] PID del padre: {os.getppid()}')
    usuario = verificar_usuario(gmail, contrasena)
    if usuario:
        q.put((True, usuario[0], usuario[1]))  # id_usuario, nombre
    else:
        q.put((False, "Usuario o contraseña incorrectos."))

def descarga_con_hilo(id_usuario):
    global hilo_descarga_activo
    def tarea_descarga():
        descarga_con_barra(id_usuario, descargar_juego)
        # Lanzar proceso de backup tras descarga
        p = multiprocessing.Process(target=proceso_backup)
        p.start()
        p.join()
        global hilo_descarga_activo
        with hilo_lock:
            hilo_descarga_activo = None
    with hilo_lock:
        if hilo_descarga_activo is not None and hilo_descarga_activo.is_alive():
            print('Ya hay una descarga en curso. Espere a que termine antes de iniciar otra.')
            return None
        hilo_descarga_activo = threading.Thread(target=tarea_descarga)
        hilo_descarga_activo.start()
        return hilo_descarga_activo

def main():
    print('[PROCESO PRINCIPAL] Proceso principal de Games-Lan')
    print(f'[PROCESO PRINCIPAL] PID: {os.getpid()}')
    print(f'[PROCESO PRINCIPAL] PID del padre: {os.getppid()}')

    db = BaseDatos()
    db.crear_tablas()
    db.close()

    id_usuario = None
    nombre_usuario = None
    while not id_usuario:
        print("Bienvenido a Games-Lan")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        choice = input("Seleccione una opción: ")

        if choice == '1':
            nombre = input("Ingrese su nombre: ").strip()
            gmail = input("Ingrese su correo electrónico: ").strip()
            contrasena = input("Ingrese su contraseña: ").strip()
            q = multiprocessing.Queue()
            p = multiprocessing.Process(target=proceso_registro, args=(nombre, gmail, contrasena, q))
            p.start()
            p.join()
            exito, mensaje = q.get()
            print(mensaje)
        elif choice == '2':
            gmail = input("Ingrese su correo electrónico: ").strip()
            contrasena = input("Ingrese su contraseña: ").strip()
            q = multiprocessing.Queue()
            p = multiprocessing.Process(target=proceso_login, args=(gmail, contrasena, q))
            p.start()
            p.join()
            resultado = q.get()
            if resultado[0]:
                id_usuario = resultado[1]
                nombre_usuario = resultado[2]
                # Lanzar proceso de notificación al iniciar sesión
                pnotif = multiprocessing.Process(target=proceso_notificacion, args=(nombre_usuario,))
                pnotif.start()
                pnotif.join()
            else:
                print(resultado[1])
                print("Redirigiendo al inicio...")
        elif choice == '3':
            print("Saliendo...")
            sys.exit()
        else:
            print("Opción no válida. Intente de nuevo.")

    while True:
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
            # Descargar juego en el hilo principal (flujo limpio)
            descarga_con_barra(id_usuario, descargar_juego)
            # Lanzar proceso de backup tras la descarga
            p = multiprocessing.Process(target=proceso_backup)
            p.start()
            p.join()
        elif choice == '4':
            print("Saliendo...")
            sys.exit()
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    main()