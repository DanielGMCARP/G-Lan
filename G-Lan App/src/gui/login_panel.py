import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Agregar el directorio padre al path para importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dal.dal import verificar_usuario, crear_usuario

class PanelInicioSesion(tk.Frame):
    def __init__(self, parent, on_login_success, on_go_to_register):
        super().__init__(parent, bg='#2b2b2b')
        self.on_login_success = on_login_success
        self.on_go_to_register = on_go_to_register
        
        self.create_widgets()
        
    def create_widgets(self):
        """Crear los widgets del panel de login"""
        # Título principal
        title_label = tk.Label(
            self, 
            text="Games-Lan", 
            font=('Arial', 24, 'bold'),
            fg='#4a90e2',
            bg='#2b2b2b'
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            self,
            text="Iniciar Sesión",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#2b2b2b'
        )
        subtitle_label.pack(pady=10)
        
        # Frame para el formulario
        form_frame = tk.Frame(self, bg='#2b2b2b')
        form_frame.pack(pady=20)
        
        # Variables para los campos
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        # Campos de entrada
        tk.Label(form_frame, text="Correo electrónico:", fg='white', bg='#2b2b2b', font=('Arial', 10)).pack(anchor='w')
        self.email_entry = tk.Entry(form_frame, textvariable=self.email_var, width=30, font=('Arial', 10))
        self.email_entry.pack(pady=5, fill='x')
        
        tk.Label(form_frame, text="Contraseña:", fg='white', bg='#2b2b2b', font=('Arial', 10)).pack(anchor='w', pady=(10,0))
        self.password_entry = tk.Entry(form_frame, textvariable=self.password_var, show="*", width=30, font=('Arial', 10))
        self.password_entry.pack(pady=5, fill='x')
        
        # Botones
        button_frame = tk.Frame(form_frame, bg='#2b2b2b')
        button_frame.pack(pady=20)
        
        login_btn = tk.Button(
            button_frame,
            text="Iniciar Sesión",
            command=self.login,
            bg='#4a90e2',
            fg='white',
            font=('Arial', 12, 'bold'),
            width=15,
            height=2
        )
        login_btn.pack(side='left', padx=5)
        
        register_btn = tk.Button(
            button_frame,
            text="Crear Cuenta",
            command=self.on_go_to_register,
            bg='#28a745',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=15,
            height=2
        )
        register_btn.pack(side='left', padx=5)
        
    def login(self):
        """Procesar el login"""
        email = self.email_var.get().strip()
        password = self.password_var.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Por favor complete todos los campos.")
            return
            
        try:
            user = verificar_usuario(email, password)
            if user:
                self.on_login_success(user[0], user[1])  # user_id, user_name
            else:
                messagebox.showerror("Error", "Correo electrónico o contraseña incorrectos.")
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el inicio de sesión: {str(e)}")
            
    def clear_fields(self):
        """Limpiar todos los campos del formulario"""
        self.email_var.set("")
        self.password_var.set("")
        
    def reset_panel(self):
        """Resetear el panel cuando se vuelve al login"""
        self.clear_fields() 