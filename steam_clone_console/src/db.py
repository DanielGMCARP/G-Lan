import sqlite3

class Database:
    def __init__(self, db_name="steam_clone.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def borrar_tabla_juegos(self):
        """Elimina la tabla 'juegos' si existe."""
        self.cursor.execute("DROP TABLE IF EXISTS juegos")
        self.conn.commit()

    def crear_tablas(self):
        # Borrar la tabla juegos antes de recrearla
        self.borrar_tabla_juegos()

        # Crear tabla usuarios
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            gmail TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL
        );
        """)

        # Crear tabla juegos
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS juegos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL,
            genero TEXT NOT NULL,
            veces_adquirido INTEGER DEFAULT 0
        );
        """)

        # Crear tabla juegosBiblioteca
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

        # Crear tabla catalogo
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS catalogo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_juego INTEGER NOT NULL,
            FOREIGN KEY (id_juego) REFERENCES juegos(id)
        );
        """)

        # Insertar juegos predeterminados en la tabla juegos
        juegos_predeterminados = [
            ("Minecraft", 20.0, "Sandbox"),
            ("Fortnite", 0.0, "Battle Royale"),
            ("League of Legends", 0.0, "MOBA"),
            ("Valorant", 0.0, "FPS"),
            ("The Witcher 3", 30.0, "RPG")
        ]

        for juego in juegos_predeterminados:
            self.cursor.execute("""
            INSERT INTO juegos (nombre, precio, genero) VALUES (?, ?, ?)
            """, juego)

        # Asociar los juegos predeterminados al catálogo
        self.cursor.execute("SELECT id FROM juegos")
        juegos_ids = self.cursor.fetchall()
        for juego_id in juegos_ids:
            self.cursor.execute("""
            INSERT INTO catalogo (id_juego) VALUES (?)
            """, (juego_id[0],))

        self.conn.commit()

    def get_cursor(self):
        return self.cursor

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()