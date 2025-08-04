"""
Ventana principal de la aplicación CPHYSICS
Contiene la navegación y el contenedor para los diferentes módulos
"""

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                                QPushButton, QLabel, QStackedWidget, QFrame)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont
from gui.kinematics_frame import KinematicsFrame
from gui.dynamics_frame import DynamicsFrame
from gui.thermodynamics_frame import ThermodynamicsFrame

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configurar la ventana principal
        self.setup_window()
        
        # Configurar estilos
        self.setup_styles()
        
        # Crear la interfaz
        self.create_widgets()
        
        # Establecer el estado inicial en la primera pestaña
        self.show_kinematics()
        
    
    def setup_window(self):
        """Configurar propiedades básicas de la ventana"""
        self.setWindowTitle("CPHYSICS - Física Computacional")
        self.setMinimumSize(QSize(1000, 700))
        self.resize(1200, 800)
        
        # Centrar la ventana en la pantalla
        self.center_window()
    
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        screen = self.screen().availableGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def setup_styles(self):
        """Configurar estilos de la aplicación"""
        # Aplicar hoja de estilos CSS-like
        style_sheet = """
            QMainWindow {
                background-color: #f5f5f5;
            }
            
            QLabel#title {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
            }
            
            QPushButton#nav_button {
                background-color: #3498db;
                border: none;
                color: white;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
                margin: 2px;
            }
            
            QPushButton#nav_button:hover {
                background-color: #2980b9;
            }
            
            QPushButton#nav_button:pressed {
                background-color: #21618c;
            }
            
            QPushButton#nav_button:checked {
                background-color: #e74c3c;
            }
            
            QFrame#separator {
                background-color: #bdc3c7;
                max-height: 2px;
                margin: 10px 0px;
            }
            
            QWidget#content_area {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #ddd;
            }
        """
        self.setStyleSheet(style_sheet)
    
    def create_widgets(self):
        """Crear los widgets principales de la ventana"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        
        # Título de la aplicación
        title_label = QLabel("CPHYSICS - Física Computacional")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Barra de navegación
        nav_layout = self.create_navigation()
        main_layout.addLayout(nav_layout)
        
        # Separador
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.HLine)
        main_layout.addWidget(separator)
        
        # Área de contenido con stack widget para cambiar entre módulos
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("content_area")
        main_layout.addWidget(self.content_stack)
        
        # Crear los módulos
        self.create_modules()
    
    def create_navigation(self):
        """Crear barra de navegación"""
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(10)
        
        # Lista de módulos con sus nombres y funciones
        modules_info = [
            ("Cinemática", self.show_kinematics),
            ("Dinámica", self.show_dynamics),
            ("Termodinámica", self.show_thermodynamics),
            ("Ondas", self.show_waves),
            ("Electromagnetismo", self.show_electromagnetism)
        ]
        
        # Crear botones de navegación
        self.nav_buttons = []
        for name, callback in modules_info:
            button = QPushButton(name)
            button.setObjectName("nav_button")
            button.setCheckable(True)  # Para poder marcar el botón activo
            button.clicked.connect(callback)
            nav_layout.addWidget(button)
            self.nav_buttons.append(button)
        
        # Agregar espacio flexible al final
        nav_layout.addStretch()
        
        return nav_layout
    
    def create_modules(self):
        """Crear todos los módulos y agregarlos al stack"""
        # Módulo de cinemática
        self.kinematics_frame = KinematicsFrame(self.content_stack)
        self.content_stack.addWidget(self.kinematics_frame)
        
        # Módulo de dinámica
        self.dynamics_frame = DynamicsFrame(self.content_stack)
        self.content_stack.addWidget(self.dynamics_frame)
        
        # Módulo de termodinámica
        self.thermodynamics_frame = ThermodynamicsFrame(self.content_stack)
        self.content_stack.addWidget(self.thermodynamics_frame)
        
        self.waves_frame = self.create_placeholder("Ondas\n(En desarrollo)")
        self.content_stack.addWidget(self.waves_frame)
        
        self.electromagnetism_frame = self.create_placeholder("Electromagnetismo\n(En desarrollo)")
        self.content_stack.addWidget(self.electromagnetism_frame)
    
    def create_placeholder(self, text, parent=None):
        """Crear un widget placeholder para módulos en desarrollo"""
        widget = QWidget(parent)
        layout = QVBoxLayout(widget)
        
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            font-size: 18px;
            color: #7f8c8d;
            font-style: italic;
        """)
        
        layout.addWidget(label)
        return widget
    
    def set_active_button(self, active_index):
        """Marcar el botón activo en la navegación"""
        for i, button in enumerate(self.nav_buttons):
            button.setChecked(i == active_index)
    
    def show_kinematics(self):
        """Mostrar el módulo de cinemática"""
        self.content_stack.setCurrentWidget(self.kinematics_frame)
        self.set_active_button(0)
    
    def show_dynamics(self):
        """Mostrar el módulo de dinámica"""
        self.content_stack.setCurrentWidget(self.dynamics_frame)
        self.set_active_button(1)
    
    def show_thermodynamics(self):
        """Mostrar el módulo de termodinámica"""
        self.content_stack.setCurrentWidget(self.thermodynamics_frame)
        self.set_active_button(2)
    
    def show_waves(self):
        """Mostrar el módulo de ondas"""
        self.content_stack.setCurrentWidget(self.waves_frame)
        self.set_active_button(3)
    
    def show_electromagnetism(self):
        """Mostrar el módulo de electromagnetismo"""
        self.content_stack.setCurrentWidget(self.electromagnetism_frame)
        self.set_active_button(4)