import tkinter as tk
from tkinter import ttk, messagebox
import threading
import multiprocessing
import time
import sys
import os

# Agregar el directorio padre al path para importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.login_panel import LoginPanel
from gui.register_panel import RegisterPanel
from gui.menu_panel import MenuPanel
from gui.catalog_panel import CatalogPanel
from gui.library_panel import LibraryPanel
from gui.download_panel import DownloadPanel
from dal.dal import crear_usuario, verificar_usuario, obtener_catalogo, procesar_compra, obtener_biblioteca, actualizar_estado_descarga, desinstalar_juego
from bd.db import Database

def notification_process(user_name):
    time.sleep(1)
    # El messagebox solo funciona en el proceso principal, así que solo imprime
    print(f"[PROCESO] ¡Bienvenido a Games-Lan, {user_name}!")

def backup_process():
    import time
    time.sleep(2)
    print("[PROCESO] Backup automático completado")

class GamesLanGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Games-Lan")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        # Variables de estado
        self.current_user_id = None
        self.current_user_name = None
        self.download_thread = None
        self.download_lock = threading.Lock()
        
        # Configurar el estilo
        self.setup_styles()
        
        # Crear el contenedor principal
        self.main_container = tk.Frame(self.root, bg='#2b2b2b')
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Inicializar paneles
        self.panels = {}
        self.current_panel = None
        
        # Crear paneles
        self.create_panels()
        
        # Mostrar el panel de login inicialmente
        self.show_panel('login')
        
    def setup_styles(self):
        """Configurar estilos para la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores
        style.configure('TFrame', background='#2b2b2b')
        style.configure('TButton', 
                       background='#4a90e2', 
                       foreground='white',
                       font=('Arial', 10, 'bold'),
                       padding=10)
        style.configure('TLabel', 
                       background='#2b2b2b', 
                       foreground='white',
                       font=('Arial', 10))
        style.configure('Header.TLabel', 
                       background='#2b2b2b', 
                       foreground='#4a90e2',
                       font=('Arial', 16, 'bold'))
        
    def create_panels(self):
        """Crear todos los paneles de la aplicación"""
        # Panel de login
        self.panels['login'] = LoginPanel(
            self.main_container, 
            self.on_login_success,
            self.go_to_register
        )
        
        # Panel de registro
        self.panels['register'] = RegisterPanel(
            self.main_container,
            self.on_register_success,
            self.go_to_login
        )
        
        # Panel del menú principal
        self.panels['menu'] = MenuPanel(
            self.main_container,
            self.show_panel,
            self.current_user_name
        )
        
        # Panel del catálogo
        self.panels['catalog'] = CatalogPanel(
            self.main_container,
            self.current_user_id,
            self.show_panel
        )
        
        # Panel de biblioteca
        self.panels['library'] = LibraryPanel(
            self.main_container,
            self.current_user_id,
            self.show_panel
        )
        
        # Panel de descargas
        self.panels['download'] = DownloadPanel(
            self.main_container,
            self.current_user_id,
            self.show_panel,
            self.start_download,
            self.download_lock
        )
        
    def show_panel(self, panel_name):
        """Mostrar un panel específico"""
        # Ocultar el panel actual
        if self.current_panel:
            self.current_panel.pack_forget()
            
        # Mostrar el nuevo panel
        self.current_panel = self.panels[panel_name]
        self.current_panel.pack(fill=tk.BOTH, expand=True)
        
        # Actualizar el panel del menú con el nombre del usuario
        if panel_name == 'menu' and self.current_user_name:
            self.panels['menu'].update_user_name(self.current_user_name)
            
        # Actualizar datos en paneles específicos
        if panel_name == 'catalog' and self.current_user_id:
            self.panels['catalog'].load_catalog()
        elif panel_name == 'library' and self.current_user_id:
            self.panels['library'].load_library()
            
    def on_login_success(self, user_id, user_name):
        """Callback cuando el login es exitoso"""
        self.current_user_id = user_id
        self.current_user_name = user_name
        
        # Actualizar paneles con el ID del usuario
        self.panels['catalog'].set_user_id(user_id)
        self.panels['library'].set_user_id(user_id)
        self.panels['download'].set_user_id(user_id)
        
        # Lanzar proceso de notificación en background
        self.launch_notification_process(user_name)
        
        # Mostrar el menú principal
        self.show_panel('menu')
        
    def on_register_success(self, user_id, user_name):
        """Callback cuando el registro es exitoso"""
        self.on_login_success(user_id, user_name)
        
    def launch_notification_process(self, user_name):
        """Lanzar proceso de notificación en background"""
        process = multiprocessing.Process(target=notification_process, args=(user_name,))
        process.start()
        
    def start_download(self, game_id):
        """Iniciar descarga de un juego"""
        with self.download_lock:
            if self.download_thread and self.download_thread.is_alive():
                messagebox.showwarning("Descarga en curso", "Ya hay una descarga en progreso. Espere a que termine.")
                return False
                
            self.download_thread = threading.Thread(
                target=self.download_game,
                args=(game_id,)
            )
            self.download_thread.start()
            return True
            
    def download_game(self, game_id):
        """Proceso de descarga del juego"""
        try:
            # Actualizar estado de descarga
            actualizar_estado_descarga(self.current_user_id, game_id)
            
            # Lanzar proceso de backup en background
            self.launch_backup_process()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la descarga: {str(e)}")
            
    def launch_backup_process(self):
        """Lanzar proceso de backup en background"""
        process = multiprocessing.Process(target=backup_process)
        process.start()
        
    def go_to_register(self):
        """Ir al panel de registro"""
        self.show_panel('register')
        
    def go_to_login(self):
        """Ir al panel de login"""
        self.show_panel('login')
        
    def run(self):
        """Ejecutar la aplicación"""
        # Crear las tablas de la base de datos
        db = Database()
        db.crear_tablas()
        db.close()
        
        # Configurar multiprocessing para Windows
        multiprocessing.set_start_method('spawn', force=True)
        
        # Ejecutar la aplicación
        self.root.mainloop()

if __name__ == "__main__":
    app = GamesLanGUI()
    app.run() 