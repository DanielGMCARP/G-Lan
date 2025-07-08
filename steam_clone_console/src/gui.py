import os
from dal import verificar_usuario, crear_usuario, obtener_catalogo, procesar_compra, obtener_biblioteca, actualizar_estado_descarga
from errores import UsuarioNoEncontradoError, IDInvalidoError, JuegoNoEncontradoError, JuegoYaDescargadoError, ContraseñaIncorrectaError

def iniciar_sesion():
    os.system('cls')
    print("=== Iniciar Sesión ===")
    gmail = input("Ingrese su correo electrónico: ")
    contrasena = input("Ingrese su contraseña: ")

    usuario = verificar_usuario(gmail, contrasena)
    if usuario:
        print("Inicio de sesión exitoso.")
        return usuario[0]  # Retorna el ID del usuario
    else:
        raise UsuarioNoEncontradoError()
    if contraseña != usuario[2]:
        raise ContraseñaIncorrectaError("Contraseña incorrecta. Por favor, inténtelo de nuevo.")
    

def registrar_usuario():
    os.system('cls')
    print("=== Registrar Usuario ===")
    nombre = input("Ingrese su nombre: ")
    gmail = input("Ingrese su correo electrónico: ")
    contrasena = input("Ingrese su contraseña: ")

    if crear_usuario(nombre, gmail, contrasena):
        print("Usuario registrado exitosamente.")
    else:
        print("Error: El correo ya está registrado.")

def mostrar_catalogo(id_usuario):
    os.system('cls')
    print("=== Catálogo de Juegos ===")
    juegos = obtener_catalogo()
    for juego in juegos:
        print(f"ID: {juego[0]}, Nombre: {juego[1]}, Precio: {juego[2]}, Género: {juego[3]}")

    
    respuesta = input("¿Desea comprar un juego? (1-sí 2-no): ")
    if respuesta == "1":
        try:
            id_juego = int(input("Ingrese el ID del juego que desea comprar: "))
            if procesar_compra(id_usuario, id_juego):
                print("Juego comprado exitosamente.")
            else:
                print("No se pudo realizar la compra.")
        except ValueError:
            print("ID inválido. Por favor, ingrese un número.")
        except JuegoNoEncontradoError as e:
            print(e)
    elif respuesta == "2":
        print("Regresando al menú principal...")
    else:
        print("Respuesta inválida. Regresando al menú principal...")

def mostrar_biblioteca(id_usuario):
    print("=== Biblioteca de Juegos ===")
    biblioteca = obtener_biblioteca(id_usuario)
    for juego in biblioteca:
        print(f"Nombre: {juego[0]}, Estado de descarga: {juego[1]}")

def descargar_juego(id_usuario):
    print("=== Descargar Juego ===")
    try:
        id_juego = int(input("Ingrese el ID del juego que desea descargar: "))
        actualizar_estado_descarga(id_usuario, id_juego)
    except ValueError:
        raise IDInvalidoError()
    except JuegoNoEncontradoError as e:
        print(e)
    except JuegoYaDescargadoError as e:
        print(e)