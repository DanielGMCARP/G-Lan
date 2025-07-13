import tkinter as tk
from tkinter import ttk

class MenuPanel(tk.Frame):
    def __init__(self, parent, show_panel_callback, user_name=None):
        super().__init__(parent, bg='#2b2b2b')
        self.show_panel_callback = show_panel_callback
        self.user_name = user_name
        
        self.create_widgets()
        
    def create_widgets(self):
        """Crear los widgets del menú principal"""
        # Título
        title_label = tk.Label(
            self, 
            text="Menú Principal", 
            font=('Arial', 20, 'bold'),
            fg='#4a90e2',
            bg='#2b2b2b'
        )
        title_label.pack(pady=20)
        
        # Información del usuario
        self.user_label = tk.Label(
            self,
            text=f"Bienvenido, {self.user_name or 'Usuario'}",
            font=('Arial', 12),
            fg='white',
            bg='#2b2b2b'
        )
        self.user_label.pack(pady=10)
        
        # Frame para botones
        button_frame = tk.Frame(self, bg='#2b2b2b')
        button_frame.pack(pady=30)
        
        # Botones del menú
        buttons = [
            ("📚 Mostrar Catálogo", 'catalog', '#4a90e2'),
            ("🎮 Biblioteca de Juegos", 'library', '#28a745'),
            ("⬇️ Descargar Juego", 'download', '#ffc107'),
            ("🚪 Cerrar Sesión", 'logout', '#dc3545')
        ]
        
        for text, panel, color in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                command=lambda p=panel: self.navigate_to_panel(p),
                bg=color,
                fg='white',
                font=('Arial', 12, 'bold'),
                width=25,
                height=3,
                relief='flat',
                cursor='hand2'
            )
            btn.pack(pady=10)
            
            # Efecto hover
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg=self.lighten_color(color)))
            btn.bind('<Leave>', lambda e, b=btn, c=color: b.configure(bg=c))
            
    def navigate_to_panel(self, panel_name):
        """Navegar a un panel específico"""
        if panel_name == 'logout':
            # Volver al login
            self.show_panel_callback('login')
        else:
            self.show_panel_callback(panel_name)
            
    def update_user_name(self, user_name):
        """Actualizar el nombre del usuario mostrado"""
        self.user_name = user_name
        self.user_label.config(text=f"Bienvenido, {user_name}")
        
    def lighten_color(self, color):
        """Aclarar un color para el efecto hover"""
        # Convertir color hex a RGB
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        
        # Aclarar el color
        r = min(255, int(r * 1.2))
        g = min(255, int(g * 1.2))
        b = min(255, int(b * 1.2))
        
        return f'#{r:02x}{g:02x}{b:02x}' 