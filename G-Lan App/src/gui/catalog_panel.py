import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Agregar el directorio padre al path para importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dal.dal import obtener_catalogo, procesar_compra, obtener_biblioteca, actualizar_estado_descarga

class PanelCatalogo(tk.Frame):
    def __init__(self, parent, id_usuario, callback_mostrar_panel):
        super().__init__(parent, bg='#2b2b2b')
        self.id_usuario = id_usuario
        self.callback_mostrar_panel = callback_mostrar_panel
        self.juegos = []
        self.biblioteca = []
        self.crear_widgets()
        
    def crear_widgets(self):
        """Crear los widgets del panel de catálogo"""
        # Encabezado
        marco_encabezado = tk.Frame(self, bg='#2b2b2b')
        marco_encabezado.pack(fill='x', pady=10)
        
        etiqueta_titulo = tk.Label(
            marco_encabezado,
            text="📚 Catálogo de Juegos",
            font=('Arial', 18, 'bold'),
            fg='#4a90e2',
            bg='#2b2b2b'
        )
        etiqueta_titulo.pack(side='left')
        
        boton_volver = tk.Button(
            marco_encabezado,
            text="← Volver al Menú",
            command=lambda: self.callback_mostrar_panel('menu'),
            bg='#6c757d',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat'
        )
        boton_volver.pack(side='right')
        
        # Marco para la lista de juegos
        self.marco_juegos = tk.Frame(self, bg='#2b2b2b')
        self.marco_juegos.pack(fill='both', expand=True, pady=10)
        
        # Crear Treeview para mostrar los juegos
        columnas = ('ID', 'Nombre', 'Precio', 'Género', 'Acción')
        self.arbol = ttk.Treeview(self.marco_juegos, columns=columnas, show='headings', height=15)
        
        # Configurar columnas
        self.arbol.heading('ID', text='ID')
        self.arbol.heading('Nombre', text='Nombre')
        self.arbol.heading('Precio', text='Precio')
        self.arbol.heading('Género', text='Género')
        self.arbol.heading('Acción', text='Acción')
        
        self.arbol.column('ID', width=50, anchor='center')
        self.arbol.column('Nombre', width=200, anchor='w')
        self.arbol.column('Precio', width=100, anchor='center')
        self.arbol.column('Género', width=150, anchor='w')
        self.arbol.column('Acción', width=150, anchor='center')
        
        # Barra de desplazamiento
        barra_desplazamiento = ttk.Scrollbar(self.marco_juegos, orient='vertical', command=self.arbol.yview)
        self.arbol.configure(yscrollcommand=barra_desplazamiento.set)
        
        # Empaquetar Treeview y scrollbar
        self.arbol.pack(side='left', fill='both', expand=True)
        barra_desplazamiento.pack(side='right', fill='y')
        
        # Configurar estilo del Treeview
        estilo = ttk.Style()
        estilo.configure("Treeview", 
                       background="#3c3c3c",
                       foreground="white",
                       fieldbackground="#3c3c3c",
                       rowheight=30)
        estilo.configure("Treeview.Heading", 
                       background="#4a90e2",
                       foreground="white",
                       font=('Arial', 10, 'bold'))
        
        # Botón de actualizar
        boton_actualizar = tk.Button(
            self,
            text="🔄 Actualizar Catálogo",
            command=self.cargar_catalogo,
            bg='#17a2b8',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            padx=20,
            pady=10
        )
        boton_actualizar.pack(pady=10)
        
    def establecer_id_usuario(self, id_usuario):
        """Establecer el ID del usuario"""
        self.id_usuario = id_usuario
        
    def cargar_catalogo(self):
        """Cargar el catálogo de juegos"""
        try:
            # Limpiar la lista actual
            for elemento in self.arbol.get_children():
                self.arbol.delete(elemento)
            # Obtener juegos de la base de datos
            self.juegos = obtener_catalogo()
            self.biblioteca = obtener_biblioteca(self.id_usuario) if self.id_usuario else []
            juegos_biblioteca = {nombre: estado for _, nombre, estado in self.biblioteca}
            # Agregar juegos al Treeview
            for juego in self.juegos:
                id_juego, nombre, precio, genero = juego
                accion = "Comprar"
                if nombre in juegos_biblioteca:
                    if juegos_biblioteca[nombre] == 'descargado':
                        accion = "Descargado"
                    else:
                        accion = "Descargar"
                elemento = self.arbol.insert('', 'end', values=(id_juego, nombre, f"${precio}", genero, accion))
            # Vincular evento de doble clic
            self.arbol.bind('<Double-1>', self.al_hacer_doble_clic)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el catálogo: {str(e)}")
            
    def al_hacer_doble_clic(self, evento):
        id_elemento = self.arbol.focus()
        if not id_elemento:
            return
        valores = self.arbol.item(id_elemento, 'values')
        if not valores:
            return
        id_juego, nombre, precio, genero, accion = valores
        if accion == "Comprar":
            self.comprar_juego(int(id_juego))
        elif accion == "Descargar":
            self.descargar_juego(int(id_juego), nombre)
        else:
            messagebox.showinfo("Información", "Este juego ya está descargado.")
    
    def comprar_juego(self, id_juego):
        if not self.id_usuario:
            messagebox.showerror("Error", "Debe iniciar sesión para comprar juegos.")
            return
        try:
            if procesar_compra(self.id_usuario, id_juego):
                messagebox.showinfo("Éxito", "Juego comprado exitosamente.")
                self.cargar_catalogo()
            else:
                messagebox.showerror("Error", "No se pudo procesar la compra.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al comprar el juego: {str(e)}")
    
    def descargar_juego(self, id_juego, nombre):
        # En vez de actualizar el estado aquí, redirige al panel de descargas y selecciona el juego
        messagebox.showinfo("Descarga", f"Para descargar '{nombre}', ve al panel de descargas donde verás la barra de progreso.")
        self.callback_mostrar_panel('download') 