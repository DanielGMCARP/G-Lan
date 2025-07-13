import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Agregar el directorio padre al path para importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dal.dal import obtener_catalogo, procesar_compra, obtener_biblioteca, actualizar_estado_descarga

class CatalogPanel(tk.Frame):
    def __init__(self, parent, user_id, show_panel_callback):
        super().__init__(parent, bg='#2b2b2b')
        self.user_id = user_id
        self.show_panel_callback = show_panel_callback
        self.games = []
        self.biblioteca = []
        self.create_widgets()
        
    def create_widgets(self):
        """Crear los widgets del panel de catálogo"""
        # Header
        header_frame = tk.Frame(self, bg='#2b2b2b')
        header_frame.pack(fill='x', pady=10)
        
        title_label = tk.Label(
            header_frame,
            text="📚 Catálogo de Juegos",
            font=('Arial', 18, 'bold'),
            fg='#4a90e2',
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
        columns = ('ID', 'Nombre', 'Precio', 'Género', 'Acción')
        self.tree = ttk.Treeview(self.games_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Precio', text='Precio')
        self.tree.heading('Género', text='Género')
        self.tree.heading('Acción', text='Acción')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Nombre', width=200, anchor='w')
        self.tree.column('Precio', width=100, anchor='center')
        self.tree.column('Género', width=150, anchor='w')
        self.tree.column('Acción', width=150, anchor='center')
        
        # Scrollbar
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
                       background="#4a90e2",
                       foreground="white",
                       font=('Arial', 10, 'bold'))
        
        # Botón de actualizar
        refresh_btn = tk.Button(
            self,
            text="🔄 Actualizar Catálogo",
            command=self.load_catalog,
            bg='#17a2b8',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            padx=20,
            pady=10
        )
        refresh_btn.pack(pady=10)
        
    def set_user_id(self, user_id):
        """Establecer el ID del usuario"""
        self.user_id = user_id
        
    def load_catalog(self):
        """Cargar el catálogo de juegos"""
        try:
            # Limpiar la lista actual
            for item in self.tree.get_children():
                self.tree.delete(item)
            # Obtener juegos de la base de datos
            self.games = obtener_catalogo()
            self.biblioteca = obtener_biblioteca(self.user_id) if self.user_id else []
            juegos_biblioteca = {nombre: estado for _, nombre, estado in self.biblioteca}
            # Agregar juegos al Treeview
            for game in self.games:
                game_id, name, price, genre = game
                accion = "Comprar"
                if name in juegos_biblioteca:
                    if juegos_biblioteca[name] == 'descargado':
                        accion = "Descargado"
                    else:
                        accion = "Descargar"
                item = self.tree.insert('', 'end', values=(game_id, name, f"${price}", genre, accion))
            # Vincular evento de doble clic
            self.tree.bind('<Double-1>', self.on_double_click)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el catálogo: {str(e)}")
            
    def on_double_click(self, event):
        item_id = self.tree.focus()
        if not item_id:
            return
        values = self.tree.item(item_id, 'values')
        if not values:
            return
        game_id, name, price, genre, accion = values
        if accion == "Comprar":
            self.buy_game(int(game_id))
        elif accion == "Descargar":
            self.download_game(int(game_id), name)
        else:
            messagebox.showinfo("Info", "Este juego ya está descargado.")
    
    def buy_game(self, game_id):
        if not self.user_id:
            messagebox.showerror("Error", "Debe iniciar sesión para comprar juegos.")
            return
        try:
            if procesar_compra(self.user_id, game_id):
                messagebox.showinfo("Éxito", "Juego comprado exitosamente.")
                self.load_catalog()
            else:
                messagebox.showerror("Error", "No se pudo procesar la compra.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al comprar el juego: {str(e)}")
    
    def download_game(self, game_id, name):
        # En vez de actualizar el estado aquí, redirige al panel de descargas y selecciona el juego
        messagebox.showinfo("Descarga", f"Para descargar '{name}', ve al panel de descargas donde verás la barra de progreso.")
        self.show_panel_callback('download') 