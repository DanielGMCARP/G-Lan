import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Agregar el directorio padre al path para importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dal.dal import crear_usuario, verificar_usuario

class PanelRegistro(tk.Frame):
    def __init__(self, parent, on_register_success, on_back_to_login):
        super().__init__(parent, bg='#2b2b2b')
        self.on_register_success = on_register_success
        self.on_back_to_login = on_back_to_login
        
        self.create_widgets()
        
    def create_widgets(self):
        """Crear los widgets del panel de registro"""
        # Título principal
        title_label = tk.Label(
            self, 
            text="Registro - Games-Lan", 
            font=('Arial', 24, 'bold'),
            fg='#28a745',
            bg='#2b2b2b'
        )
        title_label.pack(pady=20)
        
        # Frame para el formulario
        form_frame = tk.Frame(self, bg='#2b2b2b')
        form_frame.pack(pady=20)
        
        # Variables para los campos
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()
        
        # Campos de entrada
        tk.Label(form_frame, text="Nombre completo:", fg='white', bg='#2b2b2b', font=('Arial', 10)).pack(anchor='w')
        self.name_entry = tk.Entry(form_frame, textvariable=self.name_var, width=30, font=('Arial', 10))
        self.name_entry.pack(pady=5, fill='x')
        
        tk.Label(form_frame, text="Correo electrónico:", fg='white', bg='#2b2b2b', font=('Arial', 10)).pack(anchor='w', pady=(10,0))
        self.email_entry = tk.Entry(form_frame, textvariable=self.email_var, width=30, font=('Arial', 10))
        self.email_entry.pack(pady=5, fill='x')
        
        tk.Label(form_frame, text="Contraseña:", fg='white', bg='#2b2b2b', font=('Arial', 10)).pack(anchor='w', pady=(10,0))
        self.password_entry = tk.Entry(form_frame, textvariable=self.password_var, show="*", width=30, font=('Arial', 10))
        self.password_entry.pack(pady=5, fill='x')
        
        tk.Label(form_frame, text="Confirmar contraseña:", fg='white', bg='#2b2b2b', font=('Arial', 10)).pack(anchor='w', pady=(10,0))
        self.confirm_password_entry = tk.Entry(form_frame, textvariable=self.confirm_password_var, show="*", width=30, font=('Arial', 10))
        self.confirm_password_entry.pack(pady=5, fill='x')
        
        # Botones
        button_frame = tk.Frame(form_frame, bg='#2b2b2b')
        button_frame.pack(pady=20)
        
        register_btn = tk.Button(
            button_frame,
            text="Crear Cuenta",
            command=self.register,
            bg='#28a745',
            fg='white',
            font=('Arial', 12, 'bold'),
            width=15,
            height=2
        )
        register_btn.pack(side='left', padx=5)
        
        back_btn = tk.Button(
            button_frame,
            text="Volver al Login",
            command=self.on_back_to_login,
            bg='#6c757d',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=15,
            height=2
        )
        back_btn.pack(side='left', padx=5)
        
    def register(self):
        """Procesar el registro"""
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        password = self.password_var.get().strip()
        confirm_password = self.confirm_password_var.get().strip()
        
        # Validaciones
        if not name or not email or not password or not confirm_password:
            messagebox.showerror("Error", "Por favor complete todos los campos.")
            return
            
        if password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return
            
        if len(password) < 6:
            messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres.")
            return
            
        # Validar formato de correo electrónico básico
        if '@' not in email or '.' not in email:
            messagebox.showerror("Error", "Por favor ingrese un correo electrónico válido.")
            return
            
        try:
            if crear_usuario(name, email, password):
                messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
                # Buscar el usuario para obtener su ID
                user = verificar_usuario(email, password)
                if user:
                    self.on_register_success(user[0], user[1])  # user_id, user_name
                else:
                    messagebox.showerror("Error", "Error al obtener datos del usuario registrado.")
            else:
                messagebox.showerror("Error", "El correo electrónico ya está registrado.")
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el registro: {str(e)}")
            
    def clear_fields(self):
        """Limpiar todos los campos del formulario"""
        self.name_var.set("")
        self.email_var.set("")
        self.password_var.set("")
        self.confirm_password_var.set("") 