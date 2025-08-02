"""
Interfaz gráfica para el módulo de cinemática
Permite calcular y visualizar problemas de movimiento
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                                QGroupBox, QLabel, QLineEdit, QPushButton, QRadioButton,
                                QTextEdit, QSplitter, QScrollArea, QMessageBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

import matplotlib
matplotlib.use('QtAgg')  # Usar el backend genérico y agnóstico de Qt (PySide/PyQt)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from modules.kinematics import KinematicsCalculator
from utils.validators import InputValidator

class KinematicsFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Inicializar calculadora y validador
        self.calculator = KinematicsCalculator()
        self.validator = InputValidator()
        
        # Variables para almacenar resultados
        self.results = {}
        
        # Variables de entrada
        self.input_vars = {}
        self.input_fields = {}
        
        # Configurar la interfaz
        self.setup_ui()
        
        # Configurar estado inicial
        self.on_movement_type_changed()
    
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Layout principal
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Crear splitter para dividir la interfaz
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Panel izquierdo: Controles
        left_panel = self.create_control_panel()
        splitter.addWidget(left_panel)
        
        # Panel derecho: Gráficos
        right_panel = self.create_plot_panel()
        splitter.addWidget(right_panel)
        
        # Configurar tamaños relativos
        splitter.setStretchFactor(0, 1)  # Panel izquierdo
        splitter.setStretchFactor(1, 2)  # Panel derecho (más grande)
    
    def create_control_panel(self):
        """Crear panel de controles"""
        # Scroll area para el panel de controles
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumWidth(400)
        
        # Widget contenedor
        container = QWidget()
        scroll_area.setWidget(container)
        
        # Layout del contenedor
        layout = QVBoxLayout(container)
        layout.setSpacing(15)
        
        # Título del módulo
        title = QLabel("Cinemática - Movimiento Rectilíneo")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; padding: 10px 0px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Sección de tipo de movimiento
        movement_group = self.create_movement_type_section()
        layout.addWidget(movement_group)
        
        # Sección de parámetros
        params_group = self.create_parameters_section()
        layout.addWidget(params_group)
        
        # Botones de acción
        buttons_layout = self.create_action_buttons()
        layout.addLayout(buttons_layout)
        
        # Sección de resultados
        results_group = self.create_results_section()
        layout.addWidget(results_group)
        
        # Espacio flexible
        layout.addStretch()
        
        return scroll_area
    
    def create_movement_type_section(self):
        """Crear sección de tipo de movimiento"""
        group = QGroupBox("Tipo de Movimiento")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                padding-top: 10px;
                margin-top: 5px;
            }
            QGroupBox::title {
                color: #34495e;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout(group)
        
        # Radio buttons para tipo de movimiento
        self.mru_radio = QRadioButton("Movimiento Rectilíneo Uniforme (MRU)")
        self.mrua_radio = QRadioButton("Movimiento Rectilíneo Uniformemente Acelerado (MRUA)")
        
        # MRU seleccionado por defecto
        self.mru_radio.setChecked(True)
        
        # Conectar señales
        self.mru_radio.toggled.connect(self.on_movement_type_changed)
        self.mrua_radio.toggled.connect(self.on_movement_type_changed)
        
        layout.addWidget(self.mru_radio)
        layout.addWidget(self.mrua_radio)
        
        return group
    
    def create_parameters_section(self):
        """Crear sección de parámetros"""
        group = QGroupBox("Parámetros")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                padding-top: 10px;
                margin-top: 5px;
            }
            QGroupBox::title {
                color: #34495e;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        # Layout en grid para los parámetros
        layout = QGridLayout(group)
        layout.setSpacing(8)
        
        # Definir parámetros
        params_info = [
            ('x0', 'Posición inicial (m):', True),
            ('v0', 'Velocidad inicial (m/s):', True),
            ('a', 'Aceleración (m/s²):', False),
            ('t', 'Tiempo (s):', True),
            ('x', 'Posición final (m):', False),
            ('v', 'Velocidad final (m/s):', False)
        ]
        
        # Crear campos de entrada
        for i, (var_name, label_text, is_enabled) in enumerate(params_info):
            # Label
            label = QLabel(label_text)
            label.setMinimumWidth(150)
            
            # Campo de entrada
            line_edit = QLineEdit()
            line_edit.setMinimumWidth(120)
            line_edit.setEnabled(is_enabled)
            
            # Estilo para campos deshabilitados
            if not is_enabled:
                line_edit.setStyleSheet("background-color: #f0f0f0;")
            
            # Guardar referencias
            self.input_fields[var_name] = line_edit
            
            # Agregar al layout
            layout.addWidget(label, i, 0)
            layout.addWidget(line_edit, i, 1)
        
        return group
    
    def create_action_buttons(self):
        """Crear botones de acción"""
        layout = QHBoxLayout()
        layout.setSpacing(10)
        
        # Crear botones
        self.calculate_btn = QPushButton("Calcular")
        self.clear_btn = QPushButton("Limpiar")
        self.plot_btn = QPushButton("Graficar")
        
        # Estilo para botones
        button_style = """
            QPushButton {
                background-color: #3498db;
                border: none;
                color: white;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """
        
        for btn in [self.calculate_btn, self.clear_btn, self.plot_btn]:
            btn.setStyleSheet(button_style)
        
        # Conectar señales
        self.calculate_btn.clicked.connect(self.calculate)
        self.clear_btn.clicked.connect(self.clear_all)
        self.plot_btn.clicked.connect(self.plot_results)
        
        # Agregar botones al layout
        layout.addWidget(self.calculate_btn)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.plot_btn)
        layout.addStretch()
        
        return layout
    
    def create_results_section(self):
        """Crear sección de resultados"""
        group = QGroupBox("Resultados")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                padding-top: 10px;
                margin-top: 5px;
            }
            QGroupBox::title {
                color: #34495e;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout(group)
        
        # Área de texto para resultados
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(200)
        self.results_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                color: #2c3e50; /* Color de texto oscuro */
            }
        """)
        
        layout.addWidget(self.results_text)
        
        return group
    
    def create_plot_panel(self):
        """Crear panel de gráficos"""
        # Widget contenedor
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Título de la sección
        title = QLabel("Gráficos")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: #34495e; padding: 5px 0px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Crear figura de matplotlib
        self.figure = Figure(figsize=(10, 8), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        
        # Toolbar de navegación
        self.toolbar = NavigationToolbar(self.canvas, container)
        
        # Agregar al layout
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        return container
    
    def on_movement_type_changed(self):
        """Manejar cambio de tipo de movimiento"""
        is_mru = self.mru_radio.isChecked()
        
        # Habilitar/deshabilitar campo de aceleración
        self.input_fields['a'].setEnabled(not is_mru)
        
        if is_mru:
            # MRU: aceleración = 0
            self.input_fields['a'].setText('0')
            self.input_fields['a'].setStyleSheet("background-color: #f0f0f0;")
        else:
            # MRUA: habilitar aceleración
            self.input_fields['a'].setText('')
            self.input_fields['a'].setStyleSheet("")
    
    def get_input_values(self):
        """Obtener valores de entrada del formulario"""
        params = {}
        for var_name, field in self.input_fields.items():
            text = field.text().strip()
            if text:
                if not self.validator.is_valid_number(text):
                    raise ValueError(f"Valor inválido para {var_name}: {text}")
                params[var_name] = float(text)
            else:
                params[var_name] = None
        return params
    
    def calculate(self):
        """Realizar cálculos de cinemática"""
        try:
            # Obtener valores de entrada
            params = self.get_input_values()
            
            # Realizar cálculo según el tipo de movimiento
            if self.mru_radio.isChecked():
                self.results = self.calculator.calculate_mru(params)
            else:
                self.results = self.calculator.calculate_mrua(params)
            
            # Mostrar resultados
            self.display_results()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en el cálculo:\n{str(e)}")
    
    def display_results(self):
        """Mostrar resultados en el área de texto"""
        if not self.results:
            return
        
        text = "RESULTADOS DEL CÁLCULO\n"
        text += "=" * 50 + "\n\n"
        
        # Mostrar parámetros utilizados
        text += "Parámetros utilizados:\n"
        text += "-" * 25 + "\n"
        for key, value in self.results.get('input_params', {}).items():
            if value is not None:
                text += f"  {key}: {value}\n"
        
        text += "\nResultados calculados:\n"
        text += "-" * 25 + "\n"
        for key, value in self.results.get('calculated_values', {}).items():
            text += f"  {key}: {value:.4f}\n"
        
        # Mostrar ecuaciones utilizadas
        if 'equations' in self.results:
            text += "\nEcuaciones utilizadas:\n"
            text += "-" * 25 + "\n"
            for eq in self.results['equations']:
                text += f"  • {eq}\n"
        
        self.results_text.setPlainText(text)
    
    def plot_results(self):
        """Generar gráficos de los resultados"""
        if not self.results:
            QMessageBox.warning(self, "Advertencia", "Primero debe realizar un cálculo")
            return
        
        try:
            # Limpiar figura
            self.figure.clear()
            
            # Crear subplots
            ax1 = self.figure.add_subplot(2, 1, 1)
            ax2 = self.figure.add_subplot(2, 1, 2)
            
            # Generar datos para graficar
            plot_data = self.calculator.generate_plot_data(self.results)
            
            # Gráfico de posición vs tiempo
            ax1.plot(plot_data['time'], plot_data['position'], 'b-', linewidth=2.5, label='Posición')
            ax1.set_xlabel('Tiempo (s)', fontsize=12)
            ax1.set_ylabel('Posición (m)', fontsize=12)
            ax1.set_title('Posición vs Tiempo', fontsize=14, fontweight='bold')
            ax1.grid(True, alpha=0.3)
            ax1.legend(fontsize=11)
            
            # Gráfico de velocidad vs tiempo
            ax2.plot(plot_data['time'], plot_data['velocity'], 'r-', linewidth=2.5, label='Velocidad')
            ax2.set_xlabel('Tiempo (s)', fontsize=12)
            ax2.set_ylabel('Velocidad (m/s)', fontsize=12)
            ax2.set_title('Velocidad vs Tiempo', fontsize=14, fontweight='bold')
            ax2.grid(True, alpha=0.3)
            ax2.legend(fontsize=11)
            
            # Ajustar layout y estilo
            self.figure.tight_layout(pad=3.0)
            
            # Configurar colores de fondo
            self.figure.patch.set_facecolor('white')
            for ax in [ax1, ax2]:
                ax.set_facecolor('#f8f9fa')
            
            # Actualizar canvas
            self.canvas.draw()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar gráfico:\n{str(e)}")
    
    def clear_all(self):
        """Limpiar todos los campos y resultados"""
        # Limpiar campos de entrada
        for field in self.input_fields.values():
            if field.isEnabled():
                field.clear()
        
        # Limpiar resultados
        self.results = {}
        self.results_text.clear()
        
        # Limpiar gráficos
        self.figure.clear()
        self.canvas.draw()
        
        # Restaurar estado según tipo de movimiento
        self.on_movement_type_changed()