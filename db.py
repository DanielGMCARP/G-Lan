import sqlite3

# Conexión global a la base de datos
conn = sqlite3.connect("steam_clone.db")
cursor = conn.cursor()

# Crear las tablas
def crear_tablas():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        gmail TEXT NOT NULL UNIQUE,
        contrasena TEXT NOT NULL,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS juegos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        desarrollador TEXT,
        precio REAL,
        veces_adquirido INTEGER DEFAULT 0,
        veces_descargado INTEGER DEFAULT 0,
        fecha_lanzamiento DATE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS adquisiciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        juego_id INTEGER,
        fecha_adquisicion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(usuario_id, juego_id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY (juego_id) REFERENCES juegos(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS descargas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        juego_id INTEGER,
        fecha_descarga TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY (juego_id) REFERENCES juegos(id)
    );
    """)
    conn.commit()

# Agregar un nuevo usuario
def registrar_usuario(nombre, gmail, contrasena):
    try:
        cursor.execute("""
            INSERT INTO usuarios (nombre, gmail, contrasena) VALUES (?, ?, ?)
        """, (nombre, gmail, contrasena))
        conn.commit()
        print("✅ Usuario registrado correctamente.")
    except sqlite3.IntegrityError:
        print("⚠️ El correo ya está registrado.")

# Agregar un nuevo juego
def agregar_juego(nombre, descripcion, desarrollador, precio, fecha_lanzamiento):
    cursor.execute("""
        INSERT INTO juegos (nombre, descripcion, desarrollador, precio, fecha_lanzamiento)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, descripcion, desarrollador, precio, fecha_lanzamiento))
    conn.commit()
    print("🎮 Juego agregado con éxito.")

# Registrar adquisición de un juego
def adquirir_juego(usuario_id, juego_id):
    try:
        cursor.execute("""
            INSERT INTO adquisiciones (usuario_id, juego_id) VALUES (?, ?)
        """, (usuario_id, juego_id))

        cursor.execute("""
            UPDATE juegos SET veces_adquirido = veces_adquirido + 1 WHERE id = ?
        """, (juego_id,))
        conn.commit()
        print("✅ Juego adquirido.")
    except sqlite3.IntegrityError:
        print("⚠️ El usuario ya tiene este juego.")

# Registrar una descarga
def descargar_juego(usuario_id, juego_id):
    cursor.execute("""
        INSERT INTO descargas (usuario_id, juego_id) VALUES (?, ?)
    """, (usuario_id, juego_id))

    cursor.execute("""
        UPDATE juegos SET veces_descargado = veces_descargado + 1 WHERE id = ?
    """, (juego_id,))
    conn.commit()
    print("⬇️ Juego descargado.")

# Obtener todos los juegos
def listar_juegos():
    cursor.execute("SELECT * FROM juegos")
    return cursor.fetchall()

# Obtener todos los usuarios
def listar_usuarios():
    cursor.execute("SELECT * FROM usuarios")
    return cursor.fetchall()

# Ejecutar la creación de tablas si se corre el archivo directamente
if __name__ == "__main__":
    crear_tablas()
    print("✅ Base de datos inicializada.")
