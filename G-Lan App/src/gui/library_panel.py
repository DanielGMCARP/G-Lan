import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Agregar el directorio padre al path para importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dal.dal import obtener_biblioteca, desinstalar_juego, actualizar_estado_descarga

class PanelBiblioteca(tk.Frame):
    def __init__(self, parent, user_id, show_panel_callback):
        super().__init__(parent, bg='#2b2b2b')
        self.user_id = user_id
        self.show_panel_callback = show_panel_callback
        self.games = []
        
        self.create_widgets()
        
    def create_widgets(self):
        """Crear los widgets del panel de biblioteca"""
        # Encabezado
        header_frame = tk.Frame(self, bg='#2b2b2b')
        header_frame.pack(fill='x', pady=10)
        
        title_label = tk.Label(
            header_frame,
            text="🎮 Biblioteca de Juegos",
            font=('Arial', 18, 'bold'),
            fg='#28a745',
            bg='#2b2b2b'
        )
        title_label.pack(side='left')
        
        back_btn = tk.Button(
            header_frame,
            text="← Volver al Menú",
            command=lambda: self.show_panel_callback('menu'),
            bg='#6c757d',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat'
        )
        back_btn.pack(side='right')
        
        # Frame para la lista de juegos
        self.games_frame = tk.Frame(self, bg='#2b2b2b')
        self.games_frame.pack(fill='both', expand=True, pady=10)
        
        # Crear Treeview para mostrar los juegos
        columns = ('Nombre', 'Estado de Descarga', 'Acción')
        self.tree = ttk.Treeview(self.games_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        self.tree.heading('Nombre', text='Nombre del Juego')
        self.tree.heading('Estado de Descarga', text='Estado de Descarga')
        self.tree.heading('Acción', text='Acción')
        
        self.tree.column('Nombre', width=300, anchor='w')
        self.tree.column('Estado de Descarga', width=200, anchor='center')
        self.tree.column('Acción', width=150, anchor='center')
        
        # Barra de desplazamiento
        scrollbar = ttk.Scrollbar(self.games_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar Treeview y scrollbar
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Configurar estilo del Treeview
        style = ttk.Style()
        style.configure("Treeview", 
                       background="#3c3c3c",
                       foreground="white",
                       fieldbackground="#3c3c3c",
                       rowheight=30)
        style.configure("Treeview.Heading", 
                       background="#28a745",
                       foreground="white",
                       font=('Arial', 10, 'bold'))
        
        # Frame para estadísticas
        stats_frame = tk.Frame(self, bg='#2b2b2b')
        stats_frame.pack(fill='x', pady=10)
        
        self.total_games_label = tk.Label(
            stats_frame,
            text="Total de juegos: 0",
            font=('Arial', 12, 'bold'),
            fg='#28a745',
            bg='#2b2b2b'
        )
        self.total_games_label.pack(side='left')
        
        self.downloaded_games_label = tk.Label(
            stats_frame,
            text="Juegos descargados: 0",
            font=('Arial', 12, 'bold'),
            fg='#17a2b8',
            bg='#2b2b2b'
        )
        self.downloaded_games_label.pack(side='right')
        
        # Botón de actualizar
        refresh_btn = tk.Button(
            self,
            text="🔄 Actualizar Biblioteca",
            command=self.load_library,
            bg='#17a2b8',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            padx=20,
            pady=10
        )
        refresh_btn.pack(pady=10)
        
        self.tree.bind('<Double-1>', self.on_double_click)

    def set_user_id(self, user_id):
        """Establecer el ID del usuario"""
        self.user_id = user_id
        
    def load_library(self):
        """Cargar la biblioteca de juegos del usuario"""
        if not self.user_id:
            messagebox.showerror("Error", "Debe iniciar sesión para ver su biblioteca.")
            return
        try:
            # Resetear juegos atascados en 'descargandose' a 'pendiente'
            juegos_reset = 0
            juegos = obtener_biblioteca(self.user_id)
            for gid, name, status in juegos:
                if status == 'descargandose':
                    actualizar_estado_descarga(self.user_id, gid, 'pendiente')
                    juegos_reset += 1
            if juegos_reset > 0:
                messagebox.showinfo("Descargas reiniciadas", f"{juegos_reset} juego(s) atascado(s) en 'descargándose' fueron reiniciados a 'pendiente'.")
            # Limpiar la lista actual
            for item in self.tree.get_children():
                self.tree.delete(item)
            # Obtener juegos de la biblioteca (ya reseteados)
            self.games = obtener_biblioteca(self.user_id)
            # Contadores para estadísticas
            total_games = len(self.games)
            downloaded_games = 0
            # Agregar juegos al Treeview
            for game in self.games:
                game_id, name, download_status = game
                if download_status == 'descargado':
                    downloaded_games += 1
                    status_text = "✅ Descargado"
                    action_text = "Desinstalar"
                    status_color = "#28a745"
                elif download_status == 'descargandose':
                    status_text = "⬇️ Descargándose"
                    action_text = "-"
                    status_color = "#ffc107"
                else:
                    status_text = "⏳ Pendiente"
                    action_text = "Descargar"
                    status_color = "#ffc107"
                # Insertar en el Treeview
                item = self.tree.insert('', 'end', values=(name, status_text, action_text))
                # Colorear la fila según el estado
                if download_status == 'descargado':
                    self.tree.tag_configure('downloaded', background='#1e4d2b')
                    self.tree.item(item, tags=('downloaded',))
                else:
                    self.tree.tag_configure('pending', background='#4d3e1e')
                    self.tree.item(item, tags=('pending',))
            # Actualizar estadísticas
            self.total_games_label.config(text=f"Total de juegos: {total_games}")
            self.downloaded_games_label.config(text=f"Juegos descargados: {downloaded_games}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la biblioteca: {str(e)}")

    def on_double_click(self, event):
        item_id = self.tree.focus()
        if not item_id:
            return
        values = self.tree.item(item_id, 'values')
        if not values:
            return
        name, status_text, action_text = values
        if action_text == 'Desinstalar':
            self.uninstall_game(name)

    def uninstall_game(self, game_name):
        # Buscar el ID del juego
        game_id = None
        for gid, name, status in self.games:
            if name == game_name:
                game_id = gid
                break
        if game_id is None:
            messagebox.showerror("Error", "No se pudo obtener el ID del juego.")
            return
        if messagebox.askyesno("Confirmar desinstalación", f"¿Seguro que quieres desinstalar '{game_name}'?"):
            try:
                desinstalar_juego(self.user_id, game_id)
                messagebox.showinfo("Desinstalado", f"'{game_name}' ha sido desinstalado.")
                self.load_library()
            except Exception as e:
                messagebox.showerror("Error", f"Error al desinstalar: {str(e)}")

    def get_game_status(self, game_name):
        """Obtener el estado de descarga de un juego específico"""
        for game in self.games:
            game_id, name, status = game
            if name == game_name:
                return status
        return None 