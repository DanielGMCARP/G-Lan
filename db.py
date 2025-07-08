import sqlite3

class Database:
    def __init__(self, db_name="steam_clone.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def crear_tablas(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            gmail TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL
        );
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS juegos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL,
            genero TEXT NOT NULL,
            veces_adquirido INTEGER DEFAULT 0
        );
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS juegosBiblioteca (
            id_biblioteca INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            id_juego INTEGER NOT NULL,
            estado_descarga TEXT DEFAULT 'no descargado',
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
            FOREIGN KEY (id_juego) REFERENCES juegos(id)
        );
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS catalogo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_juego INTEGER NOT NULL,
            FOREIGN KEY (id_juego) REFERENCES juegos(id)
        );
        """)
        self.conn.commit()

    def get_cursor(self):
        return self.cursor

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()