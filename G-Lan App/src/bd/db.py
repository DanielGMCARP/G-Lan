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
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (id_juego) REFERENCES juegos(id) ON DELETE CASCADE
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
            ("The Witcher 3", 30.0, "RPG"),
            ("Counter-Strike: Global Offensive", 0.0, "FPS"),
            ("Among Us", 5.0, "Party"),
            ("Stardew Valley", 15.0, "Simulation"),
            ("Terraria", 10.0, "Adventure"),
            ("Celeste", 20.0, "Platformer"),
            ("Hollow Knight", 15.0, "Metroidvania"),
            ("Apex Legends", 0.0, "Battle Royale"),
            ("Dota 2", 0.0, "MOBA"),
            ("Genshin Impact", 0.0, "Action RPG"),
            ("Call of Duty: Warzone", 0.0, "FPS"),
            ("Fall Guys", 20.0, "Party"),
            ("Rocket League", 20.0, "Sports"),
            ("Dead by Daylight", 20.0, "Horror"),
            ("ARK: Survival Evolved", 30.0, "Survival"),
            ("Rust", 40.0, "Survival"),
            ("Cyberpunk 2077", 60.0, "RPG"),
            ("Assassin's Creed Valhalla", 60.0, "Action RPG"),
            ("Ghost of Tsushima", 60.0, "Action Adventure"),
            ("Hades", 20.0, "Roguelike"),
            ("Slay the Spire", 15.0, "Card Game"),
            ("Ori and the Will of the Wisps", 30.0, "Platformer"),
            ("Monster Hunter: World", 40.0, "Action RPG"),
            ("Final Fantasy XIV", 15.0, "MMORPG"),
            ("World of Warcraft", 15.0, "MMORPG"),
            ("The Elder Scrolls V: Skyrim", 30.0, "RPG"),
            ("Dark Souls III", 40.0, "Action RPG"),
            ("Sekiro: Shadows Die Twice", 60.0, "Action RPG"),
            ("Bloodborne", 40.0, "Action RPG"),
            ("Persona 5 Royal", 60.0, "JRPG"),
            ("Nioh 2", 40.0, "Action RPG"),
            ("Monster Hunter Rise", 40.0, "Action RPG"),
            ("Ghostrunner", 30.0, "Action"),
            ("Control", 30.0, "Action Adventure"),
            ("Death Stranding", 60.0, "Adventure"),
            ("Returnal", 70.0, "Roguelike"),
            ("Ratchet & Clank: Rift Apart", 60.0, "Action Adventure")
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