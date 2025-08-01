"""
Ventana principal de la aplicación CPHYSICS
Contiene la navegación y el contenedor para los diferentes módulos
"""

import tkinter as tk
from tkinter import ttk
from gui.kinematics_frame import KinematicsFrame

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.current_frame = None
        
        # Configurar el estilo
        self.setup_styles()
        
        # Crear la interfaz
        self.create_widgets()
        
        # Mostrar el módulo de cinemática por defecto
        self.show_kinematics()
    
    def setup_styles(self):
        """Configurar estilos personalizados para la aplicación"""
        style = ttk.Style()
        
        # Configurar tema
        style.theme_use('clam')
        
        # Estilo para botones de navegación
        style.configure('Nav.TButton',
                        padding=(20, 10),
                        font=('Arial', 11, 'bold'))
        
        # Estilo para el título
        style.configure('Title.TLabel',
                        font=('Arial', 16, 'bold'),
                        foreground='#2c3e50')
        
        # Estilo para subtítulos
        style.configure('Subtitle.TLabel',
                        font=('Arial', 12, 'bold'),
                        foreground='#34495e')
    
    def create_widgets(self):
        """Crear los widgets principales de la ventana"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título de la aplicación
        title_label = ttk.Label(main_frame, 
                                text="CPHYSICS - Física Computacional",
                                style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Frame de navegación
        nav_frame = ttk.Frame(main_frame)
        nav_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Botones de navegación
        self.create_navigation_buttons(nav_frame)
        
        # Separador
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=(0, 10))
        
        # Frame contenedor para los módulos
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
    
    def create_navigation_buttons(self, parent):
        """Crear botones de navegación"""
        buttons_info = [
            ("Cinemática", self.show_kinematics),
            ("Dinámica", self.show_dynamics),
            ("Termodinámica", self.show_thermodynamics),
            ("Ondas", self.show_waves),
            ("Electromagnetismo", self.show_electromagnetism)
        ]
        
        for text, command in buttons_info:
            btn = ttk.Button(parent, 
                            text=text,
                            style='Nav.TButton',
                            command=command)
            btn.pack(side=tk.LEFT, padx=(0, 10))
    
    def clear_content_frame(self):
        """Limpiar the contenido actual"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.current_frame = None
    
    def show_kinematics(self):
        """Mostrar el módulo de cinemática"""
        self.clear_content_frame()
        self.current_frame = KinematicsFrame(self.content_frame)
    
    def show_dynamics(self):
        """Mostrar el módulo de dinámica (placeholder)"""
        self.clear_content_frame()
        placeholder = ttk.Label(self.content_frame,
                                text="Módulo de Dinámica\n(En desarrollo)",
                                style='Subtitle.TLabel')
        placeholder.pack(expand=True)
    
    def show_thermodynamics(self):
        """Mostrar el módulo de termodinámica (placeholder)"""
        self.clear_content_frame()
        placeholder = ttk.Label(self.content_frame,
                                text="Módulo de Termodinámica\n(En desarrollo)",
                                style='Subtitle.TLabel')
        placeholder.pack(expand=True)
    
    def show_waves(self):
        """Mostrar el módulo de ondas (placeholder)"""
        self.clear_content_frame()
        placeholder = ttk.Label(self.content_frame,
                                text="Módulo de Ondas\n(En desarrollo)",
                                style='Subtitle.TLabel')
        placeholder.pack(expand=True)
    
    def show_electromagnetism(self):
        """Mostrar el módulo de electromagnetismo (placeholder)"""
        self.clear_content_frame()
        placeholder = ttk.Label(self.content_frame,
                                text="Módulo de Electromagnetismo\n(En desarrollo)",
                                style='Subtitle.TLabel')
        placeholder.pack(expand=True)