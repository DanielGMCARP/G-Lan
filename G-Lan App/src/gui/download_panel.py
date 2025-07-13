import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import sys
import os

# Agregar el directorio padre al path para importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dal.dal import obtener_biblioteca, actualizar_estado_descarga

class PanelDescarga(tk.Frame):
    def __init__(self, parent, user_id, show_panel_callback, start_download_callback, download_lock):
        super().__init__(parent, bg='#2b2b2b')
        self.user_id = user_id
        self.show_panel_callback = show_panel_callback
        self.start_download_callback = start_download_callback
        self.download_lock = download_lock
        self.games = []
        self.download_thread = None
        self.descarga_en_curso = False  # Flag para controlar descargas simultáneas
        self.create_widgets()
        
    def create_widgets(self):
        """Crear los widgets del panel de descargas"""
        # Encabezado
        header_frame = tk.Frame(self, bg='#2b2b2b')
        header_frame.pack(fill='x', pady=10)
        
        title_label = tk.Label(
            header_frame,
            text="⬇️ Descargar Juego",
            font=('Arial', 18, 'bold'),
            fg='#ffc107',
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
        
        # Frame principal
        main_frame = tk.Frame(self, bg='#2b2b2b')
        main_frame.pack(fill='both', expand=True, pady=20)
        
        # Frame izquierdo - Lista de juegos disponibles
        left_frame = tk.Frame(main_frame, bg='#2b2b2b')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Título de la lista
        list_title = tk.Label(
            left_frame,
            text="Juegos en tu Biblioteca",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#2b2b2b'
        )
        list_title.pack(pady=(0, 10))
        
        # Lista de juegos
        self.games_listbox = tk.Listbox(
            left_frame,
            bg='#3c3c3c',
            fg='white',
            font=('Arial', 10),
            selectmode='single',
            height=15
        )
        self.games_listbox.pack(fill='both', expand=True)
        
        # Barra de desplazamiento para la lista
        list_scrollbar = tk.Scrollbar(left_frame, orient='vertical', command=self.games_listbox.yview)
        self.games_listbox.configure(yscrollcommand=list_scrollbar.set)
        list_scrollbar.pack(side='right', fill='y')
        
        # Frame derecho - Información y controles
        right_frame = tk.Frame(main_frame, bg='#2b2b2b')
        right_frame.pack(side='right', fill='both', padx=(10, 0))
        
        # Información del juego seleccionado
        info_frame = tk.Frame(right_frame, bg='#2b2b2b')
        info_frame.pack(fill='x', pady=(0, 20))
        
        self.game_info_label = tk.Label(
            info_frame,
            text="Selecciona un juego de la lista",
            font=('Arial', 12),
            fg='white',
            bg='#2b2b2b',
            wraplength=300
        )
        self.game_info_label.pack()
        
        # Frame para la barra de progreso
        progress_frame = tk.Frame(right_frame, bg='#2b2b2b')
        progress_frame.pack(fill='x', pady=20)
        
        self.progress_label = tk.Label(
            progress_frame,
            text="Estado: Listo",
            font=('Arial', 10),
            fg='white',
            bg='#2b2b2b'
        )
        self.progress_label.pack()
        
        # Barra de progreso
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            orient='horizontal',
            length=300,
            mode='determinate'
        )
        self.progress_bar.pack(pady=10)
        
        # Porcentaje
        self.percentage_label = tk.Label(
            progress_frame,
            text="0%",
            font=('Arial', 10, 'bold'),
            fg='#ffc107',
            bg='#2b2b2b'
        )
        self.percentage_label.pack()
        
        # Botones
        button_frame = tk.Frame(right_frame, bg='#2b2b2b')
        button_frame.pack(fill='x', pady=20)
        
        self.download_btn = tk.Button(
            button_frame,
            text="⬇️ Descargar",
            command=self.start_download,
            bg='#28a745',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief='flat',
            state='disabled'
        )
        self.download_btn.pack(fill='x', pady=5)
        
        refresh_btn = tk.Button(
            button_frame,
            text="🔄 Actualizar Lista",
            command=self.load_games,
            bg='#17a2b8',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat'
        )
        refresh_btn.pack(fill='x', pady=5)
        
        # Vincular eventos
        self.games_listbox.bind('<<ListboxSelect>>', self.on_game_select)
        
    def set_user_id(self, user_id):
        """Establecer el ID del usuario"""
        self.user_id = user_id
        
    def load_games(self):
        """Cargar la lista de juegos del usuario"""
        if not self.user_id:
            messagebox.showerror("Error", "Debe iniciar sesión para descargar juegos.")
            return
        try:
            # Limpiar la lista
            self.games_listbox.delete(0, tk.END)
            # Obtener juegos de la biblioteca (ahora: id, nombre, estado)
            self.games = obtener_biblioteca(self.user_id)
            # Agregar juegos a la lista (solo los no descargados)
            for game in self.games:
                game_id, name, status = game
                if status != 'descargado':
                    self.games_listbox.insert(tk.END, name)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los juegos: {str(e)}")

    def on_game_select(self, event):
        """Manejar la selección de un juego"""
        selection = self.games_listbox.curselection()
        if selection:
            game_name = self.games_listbox.get(selection[0])
            self.selected_game = game_name
            self.game_info_label.config(text=f"Juego seleccionado:\n{game_name}")
            self.download_btn.config(state='normal')
        else:
            self.selected_game = None
            self.game_info_label.config(text="Selecciona un juego de la lista")
            self.download_btn.config(state='disabled')
            
    def start_download(self):
        """Iniciar la descarga del juego seleccionado"""
        if self.descarga_en_curso:
            messagebox.showinfo("Descarga en curso", "Ya hay una descarga en progreso. Espera a que termine antes de iniciar otra.")
            return
        if not hasattr(self, 'selected_game') or not self.selected_game:
            messagebox.showwarning("Advertencia", "Por favor selecciona un juego para descargar.")
            return
        # Buscar el ID y estado del juego
        game_id = None
        estado_actual = None
        from dal.dal import obtener_biblioteca
        biblioteca_actual = obtener_biblioteca(self.user_id)
        for gid, name, status in biblioteca_actual:
            if name == self.selected_game:
                game_id = gid
                estado_actual = status
                break
        if game_id is None:
            messagebox.showerror("Error", "No se pudo obtener el ID del juego.")
            return
        if estado_actual == 'descargado':
            messagebox.showinfo("Información", "El juego ya está descargado.")
            return
        if estado_actual == 'descargandose':
            messagebox.showinfo("Información", "El juego ya se está descargando.")
            return
        # Cambiar estado a 'descargandose'
        try:
            actualizar_estado_descarga(self.user_id, game_id, 'descargandose')
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar la descarga: {str(e)}")
            return
        self.descarga_en_curso = True
        self.download_btn.config(state='disabled')
        self.progress_label.config(text="Estado: Descargando...")
        self.start_progress_animation()

    def start_progress_animation(self):
        """Iniciar la animación de la barra de progreso y actualizar el estado al final"""
        def animate_progress():
            for i in range(101):
                self.progress_bar['value'] = i
                self.percentage_label.config(text=f"{i}%")
                time.sleep(0.1)
            # Al llegar al 100%, actualizar el estado en la base de datos solo si no está descargado
            try:
                # Buscar el ID y estado del juego seleccionado
                game_id = None
                estado_actual = None
                from dal.dal import obtener_biblioteca
                biblioteca_actual = obtener_biblioteca(self.user_id)
                for gid, name, status in biblioteca_actual:
                    if name == self.selected_game:
                        game_id = gid
                        estado_actual = status
                        break
                if game_id is not None:
                    if estado_actual != 'descargado':
                        actualizar_estado_descarga(self.user_id, game_id, 'descargado')
                        self.progress_label.config(text="Estado: Completado")
                        self.download_btn.config(state='normal')
                        self.load_games()
                        messagebox.showinfo("Descarga", f"El juego '{self.selected_game}' se ha descargado correctamente.")
                    else:
                        self.progress_label.config(text="Estado: Completado")
                        self.download_btn.config(state='normal')
                        self.load_games()
                        messagebox.showinfo("Descarga", f"El juego '{self.selected_game}' ya estaba descargado.")
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el estado del juego.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar el estado: {str(e)}")
            finally:
                self.descarga_en_curso = False
        self.download_thread = threading.Thread(target=animate_progress)
        self.download_thread.start() 