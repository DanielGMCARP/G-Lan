import sqlite3
from bd.db import Database
from errores import JuegoNoEncontradoError, JuegoYaDescargadoError, JuegoYaCompradoError

def crear_usuario(nombre, gmail, contrasena):
    db = Database()
    cursor = db.get_cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nombre, gmail, contrasena) VALUES (?, ?, ?)", (nombre, gmail, contrasena))
        db.commit()
    except sqlite3.IntegrityError:
        print("Error: El correo electrónico ya está registrado.")
        return False
    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
        return False
    finally:
        db.close()
    return True

def verificar_usuario(gmail, contrasena):
    db = Database()
    cursor = db.get_cursor()
    cursor.execute("SELECT * FROM usuarios WHERE gmail = ? AND contrasena = ?", (gmail, contrasena))
    usuario = cursor.fetchone()
    db.close()
    return usuario

def obtener_catalogo():
    db = Database()
    cursor = db.get_cursor()
    cursor.execute("SELECT id, nombre, precio, genero FROM juegos")
    juegos = cursor.fetchall()
    db.close()
    return juegos

def procesar_compra(id_usuario, id_juego):
    db = Database()
    cursor = db.get_cursor()

    cursor.execute("SELECT id FROM juegos WHERE id = ?", (id_juego,))
    juego = cursor.fetchone()
    if not juego:
        db.close()
        raise JuegoNoEncontradoError()

    cursor.execute("""
    SELECT id_juego FROM juegosBiblioteca
    WHERE id_usuario = ? AND id_juego = ?
    """, (id_usuario, id_juego))
    juego_en_biblioteca = cursor.fetchone()
    if juego_en_biblioteca:
        db.close()
        raise JuegoYaCompradoError(f"El juego con ID {id_juego} ya está en tu biblioteca.")

    # Insertar el juego en la biblioteca del usuario
    cursor.execute("INSERT INTO juegosBiblioteca (id_usuario, id_juego) VALUES (?, ?)", (id_usuario, id_juego))
    cursor.execute("UPDATE juegos SET veces_adquirido = veces_adquirido + 1 WHERE id = ?", (id_juego,))
    db.commit()
    db.close()
    print("Compra realizada exitosamente.")
    return True

def obtener_biblioteca(id_usuario):
    db = Database()
    cursor = db.get_cursor()
    cursor.execute("""
    SELECT juegos.id, juegos.nombre, juegosBiblioteca.estado_descarga
    FROM juegosBiblioteca
    JOIN juegos ON juegosBiblioteca.id_juego = juegos.id
    WHERE juegosBiblioteca.id_usuario = ?
    """, (id_usuario,))
    biblioteca = cursor.fetchall()
    db.close()
    return biblioteca

def actualizar_estado_descarga(id_usuario, id_juego, nuevo_estado='descargado'):
    db = Database()
    cursor = db.get_cursor()
    cursor.execute("""
    SELECT estado_descarga FROM juegosBiblioteca
    WHERE id_usuario = ? AND id_juego = ?
    """, (id_usuario, id_juego))
    estado = cursor.fetchone()
    if not estado:
        db.close()
        raise JuegoNoEncontradoError()
    if estado[0] == nuevo_estado:
        db.close()
        raise JuegoYaDescargadoError()
    cursor.execute("""
    UPDATE juegosBiblioteca
    SET estado_descarga = ?
    WHERE id_usuario = ? AND id_juego = ?
    """, (nuevo_estado, id_usuario, id_juego))
    db.commit()
    db.close()
    print(f"El estado del juego con ID {id_juego} ha sido actualizado a '{nuevo_estado}'.")

def desinstalar_juego(id_usuario, id_juego):
    db = Database()
    cursor = db.get_cursor()
    cursor.execute("""
    UPDATE juegosBiblioteca
    SET estado_descarga = 'pendiente'
    WHERE id_usuario = ? AND id_juego = ?
    """, (id_usuario, id_juego))
    db.commit()
    db.close()
    print(f"Juego con ID {id_juego} marcado como pendiente para el usuario {id_usuario}.")