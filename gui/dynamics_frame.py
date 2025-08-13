
"""
Interfaz gráfica para el módulo de dinámica
Permite calcular problemas de la Segunda Ley de Newton
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QSplitter,
                                QGroupBox, QLabel, QLineEdit, QPushButton,
                                QTextEdit, QScrollArea, QMessageBox, QCheckBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import seaborn as sns
import numpy as np

from modules.dynamics import DynamicsCalculator
from utils.validators import InputValidator

class DynamicsFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.calculator = DynamicsCalculator()
        self.validator = InputValidator()
        
        self.results = {}
        self.input_fields = {}
        self.energy_input_fields = {}
        self.momentum_input_fields = {}
        self.friction_checkbox = None
        self.mu_input = None
        self.incline_checkbox = None
        self.angle_input = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        left_panel = self.create_control_panel()
        splitter.addWidget(left_panel)
        
        right_panel = self.create_plot_panel()
        splitter.addWidget(right_panel)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
    
    def create_control_panel(self):
        """Crear panel de controles y resultados"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumWidth(400)
        
        container = QWidget()
        scroll_area.setWidget(container)
        
        layout = QVBoxLayout(container)
        layout.setSpacing(15)
        
        title = QLabel("Dinámica - Segunda Ley de Newton")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #ecf0f1; padding: 10px 0px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        params_group = self.create_parameters_section()
        layout.addWidget(params_group)
        
        incline_group = self.create_incline_section()
        layout.addWidget(incline_group)
        
        friction_group = self.create_friction_section()
        layout.addWidget(friction_group)
        
        buttons_layout = self.create_action_buttons()
        layout.addLayout(buttons_layout)
        
        energy_group = self.create_energy_section()
        layout.addWidget(energy_group)

        momentum_group = self.create_momentum_section()
        layout.addWidget(momentum_group)

        results_group = self.create_results_section()
        layout.addWidget(results_group)
        
        layout.addStretch()
        
        return scroll_area
    
    # Create Parameters Section
    def create_parameters_section(self):
        """Crear sección de parámetros"""
        group = QGroupBox("Parámetros (deje uno en blanco para calcular)")
        group.setStyleSheet('''
            QGroupBox { 
                font-weight: bold; font-size: 14px; padding-top: 10px; margin-top: 5px; 
                color: #ecf0f1; border: 1px solid #4a627a; border-radius: 5px;
            }
            QGroupBox::title { 
                color: #ecf0f1; subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px;
            }
            QGroupBox QLabel {
                color: #ecf0f1; font-size: 12px;
            }
        ''')
        
        layout = QGridLayout(group)
        layout.setSpacing(8)
        
        params_info = [
            ('f', 'Fuerza Aplicada (N):'),
            ('m', 'Masa (kg):'),
            ('a', 'Aceleración (m/s²):'),
        ]
        
        for i, (var_name, label_text) in enumerate(params_info):
            label = QLabel(label_text)
            line_edit = QLineEdit()
            line_edit.setPlaceholderText("Valor conocido")
            line_edit.setStyleSheet('''
                QLineEdit {
                    background-color: #2c3e50;
                    color: #ecf0f1;
                    border: 1px solid #4a627a;
                    border-radius: 4px;
                    padding: 6px;
                }
                QLineEdit:focus { border: 1px solid #8e44ad; }
            ''')
            self.input_fields[var_name] = line_edit
            layout.addWidget(label, i, 0)
            layout.addWidget(line_edit, i, 1)
        
        return group
    
    # Create Friction and Incline Sections
    def create_friction_section(self):
        """Crear sección para la fricción opcional."""
        group = QGroupBox("Fricción (Opcional)")
        group.setCheckable(True)
        group.setChecked(False)
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold; font-size: 14px; padding-top: 10px; margin-top: 5px;
                color: #ecf0f1; border: 1px solid #4a627a; border-radius: 5px;
            }
            QGroupBox::title {
                color: #ecf0f1; subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px;
            }
            QGroupBox QLabel { color: #ecf0f1; font-size: 12px; }
        """)

        layout = QGridLayout(group)
        layout.setSpacing(8)

        mu_label = QLabel("Coeficiente de Fricción (μ):")
        self.mu_input = QLineEdit()
        self.mu_input.setPlaceholderText("ex. 0.2")
        self.mu_input.setStyleSheet("""
            QLineEdit {
                background-color: #2c3e50; color: #ecf0f1;
                border: 1px solid #4a627a; border-radius: 4px; padding: 6px;
            }
            QLineEdit:focus { border: 1px solid #8e44ad; }
        """)
        layout.addWidget(mu_label, 0, 0)
        layout.addWidget(self.mu_input, 0, 1)

        self.friction_checkbox = group
        group.toggled.connect(self.mu_input.setEnabled)
        self.mu_input.setEnabled(False)

        return group

    # Create Incline Section
    def create_incline_section(self):
        """Crear sección para el plano inclinado opcional."""
        group = QGroupBox("Plano Inclinado (Opcional)")
        group.setCheckable(True)
        group.setChecked(False)
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold; font-size: 14px; padding-top: 10px; margin-top: 5px;
                color: #ecf0f1; border: 1px solid #4a627a; border-radius: 5px;
            }
            QGroupBox::title {
                color: #ecf0f1; subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px;
            }
            QGroupBox QLabel { color: #ecf0f1; font-size: 12px; }
        """)

        layout = QGridLayout(group)
        layout.setSpacing(8)

        angle_label = QLabel("Ángulo del Plano (θ°):")
        self.angle_input = QLineEdit()
        self.angle_input.setPlaceholderText("ex. 30")
        self.angle_input.setStyleSheet("""
            QLineEdit {
                background-color: #2c3e50; color: #ecf0f1;
                border: 1px solid #4a627a; border-radius: 4px; padding: 6px;
            }
            QLineEdit:focus { border: 1px solid #8e44ad; }
        """)
        layout.addWidget(angle_label, 0, 0)
        layout.addWidget(self.angle_input, 0, 1)

        self.incline_checkbox = group
        group.toggled.connect(self.angle_input.setEnabled)
        self.angle_input.setEnabled(False)

        return group

    # Create Action Buttons
    def create_action_buttons(self):
        """Crear botones de acción"""
        layout = QHBoxLayout()
        layout.setSpacing(10)
        
        self.calculate_btn = QPushButton("Calcular Ley de Newton")
        self.clear_btn = QPushButton("Limpiar Todo")
        self.plot_btn = QPushButton("Graficar")
        
        button_style = '''
            QPushButton { 
                background-color: #8e44ad; border: none; color: white; padding: 8px 16px; 
                font-size: 12px; font-weight: bold; border-radius: 4px; min-width: 80px; 
            }
            QPushButton:hover { background-color: #9b59b6; }
            QPushButton:pressed { background-color: #7d3c98; }
        '''
        for btn in [self.calculate_btn, self.clear_btn, self.plot_btn]:
            btn.setStyleSheet(button_style)
        
        self.calculate_btn.clicked.connect(self.calculate_newton)
        self.clear_btn.clicked.connect(self.clear_all)
        self.plot_btn.clicked.connect(self.plot_results)
        
        layout.addWidget(self.calculate_btn)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.plot_btn)
        layout.addStretch()
        
        return layout

    # Section for Energy Calculations
    def create_energy_section(self):
        """Crear sección para cálculos de Trabajo y Energía."""
        main_group = QGroupBox("Trabajo y Energía")
        main_group.setStyleSheet('''
            QGroupBox { 
                font-weight: bold; font-size: 14px; padding-top: 10px; margin-top: 10px; 
                color: #ecf0f1; border: 1px solid #4a627a; border-radius: 5px;
            }
            QGroupBox::title { 
                color: #ecf0f1; subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px;
            }
        ''')
        main_layout = QVBoxLayout(main_group)
        main_layout.setSpacing(10)

        # --- Sub-sección de Trabajo ---
        work_group = QGroupBox("Calcular Trabajo (W)")
        work_layout = QGridLayout(work_group)
        work_params = {
            'work_force': 'Fuerza (N):',
            'work_distance': 'Distancia (m):',
            'work_angle': 'Ángulo (θ°):',
        }
        for i, (key, label) in enumerate(work_params.items()):
            work_layout.addWidget(QLabel(label), i, 0)
            line_edit = QLineEdit()
            line_edit.setPlaceholderText("Valor")
            self.energy_input_fields[key] = line_edit
            work_layout.addWidget(line_edit, i, 1)
        
        calc_work_btn = QPushButton("Calcular Trabajo")
        calc_work_btn.clicked.connect(self.calculate_work)
        work_layout.addWidget(calc_work_btn, len(work_params), 0, 1, 2)
        main_layout.addWidget(work_group)

        # --- Sub-sección de Energía Cinética ---
        ke_group = QGroupBox("Calcular Energía Cinética (KE)")
        ke_layout = QGridLayout(ke_group)
        ke_params = {
            'ke_mass': 'Masa (kg):',
            'ke_velocity': 'Velocidad (m/s):',
        }
        for i, (key, label) in enumerate(ke_params.items()):
            ke_layout.addWidget(QLabel(label), i, 0)
            line_edit = QLineEdit()
            line_edit.setPlaceholderText("Valor")
            self.energy_input_fields[key] = line_edit
            ke_layout.addWidget(line_edit, i, 1)

        calc_ke_btn = QPushButton("Calcular Energía Cinética")
        calc_ke_btn.clicked.connect(self.calculate_kinetic_energy)
        ke_layout.addWidget(calc_ke_btn, len(ke_params), 0, 1, 2)
        main_layout.addWidget(ke_group)

        # --- Sub-sección de Energía Potencial ---
        pe_group = QGroupBox("Calcular Energía Potencial (PE)")
        pe_layout = QGridLayout(pe_group)
        pe_params = {
            'pe_mass': 'Masa (kg):',
            'pe_height': 'Altura (m):',
        }
        for i, (key, label) in enumerate(pe_params.items()):
            pe_layout.addWidget(QLabel(label), i, 0)
            line_edit = QLineEdit()
            line_edit.setPlaceholderText("Valor")
            self.energy_input_fields[key] = line_edit
            pe_layout.addWidget(line_edit, i, 1)

        calc_pe_btn = QPushButton("Calcular Energía Potencial")
        calc_pe_btn.clicked.connect(self.calculate_potential_energy)
        pe_layout.addWidget(calc_pe_btn, len(pe_params), 0, 1, 2)
        main_layout.addWidget(pe_group)

        # Estilo común para QLineEdit y QPushButton dentro de esta sección
        style = '''
            QLineEdit {
                background-color: #2c3e50; color: #ecf0f1;
                border: 1px solid #4a627a; border-radius: 4px; padding: 6px;
            }
            QLineEdit:focus { border: 1px solid #8e44ad; }
            QPushButton { 
                background-color: #16a085; border: none; color: white; padding: 8px; 
                font-size: 12px; font-weight: bold; border-radius: 4px; margin-top: 5px;
            }
            QPushButton:hover { background-color: #1abc9c; }
            QPushButton:pressed { background-color: #148f77; }
            QGroupBox { 
                font-weight: bold; font-size: 12px; padding-top: 8px; margin-top: 5px; 
                color: #bdc3c7; border: 1px solid #3e5062; border-radius: 5px;
            }
            QGroupBox::title { color: #bdc3c7; }
            QLabel { font-size: 12px; color: #ecf0f1; }
        '''
        main_group.setStyleSheet(style)

        return main_group

    # Section for Momentum Calculations
    def create_momentum_section(self):
        """Crear sección para cálculos de Impulso y Momento Lineal."""
        main_group = QGroupBox("Impulso y Momento Lineal")
        main_group.setStyleSheet('''
            QGroupBox { 
                font-weight: bold; font-size: 14px; padding-top: 10px; margin-top: 10px; 
                color: #ecf0f1; border: 1px solid #4a627a; border-radius: 5px;
            }
            QGroupBox::title { 
                color: #ecf0f1; subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px;
            }
        ''')
        main_layout = QVBoxLayout(main_group)
        main_layout.setSpacing(10)

        # --- Sub-sección de Impulso ---
        impulse_group = QGroupBox("Calcular Impulso (I)")
        impulse_layout = QGridLayout(impulse_group)
        impulse_params = {
            'impulse_force': 'Fuerza (N):',
            'impulse_time': 'Tiempo (s):',
            'impulse_impulse': 'Impulso (N·s):',
        }
        for i, (key, label) in enumerate(impulse_params.items()):
            impulse_layout.addWidget(QLabel(label), i, 0)
            line_edit = QLineEdit()
            line_edit.setPlaceholderText("Dejar en blanco para calcular")
            self.momentum_input_fields[key] = line_edit
            impulse_layout.addWidget(line_edit, i, 1)
        
        calc_impulse_btn = QPushButton("Calcular Impulso")
        calc_impulse_btn.clicked.connect(self.calculate_impulse)
        impulse_layout.addWidget(calc_impulse_btn, len(impulse_params), 0, 1, 2)
        main_layout.addWidget(impulse_group)

        # --- Sub-sección de Momento Lineal ---
        momentum_group = QGroupBox("Calcular Momento Lineal (p)")
        momentum_layout = QGridLayout(momentum_group)
        momentum_params = {
            'momentum_mass': 'Masa (kg):',
            'momentum_velocity': 'Velocidad (m/s):',
            'momentum_momentum': 'Momento (kg·m/s):',
        }
        for i, (key, label) in enumerate(momentum_params.items()):
            momentum_layout.addWidget(QLabel(label), i, 0)
            line_edit = QLineEdit()
            line_edit.setPlaceholderText("Dejar en blanco para calcular")
            self.momentum_input_fields[key] = line_edit
            momentum_layout.addWidget(line_edit, i, 1)

        calc_momentum_btn = QPushButton("Calcular Momento Lineal")
        calc_momentum_btn.clicked.connect(self.calculate_linear_momentum)
        momentum_layout.addWidget(calc_momentum_btn, len(momentum_params), 0, 1, 2)
        main_layout.addWidget(momentum_group)

        # Estilo común para QLineEdit y QPushButton dentro de esta sección
        style = '''
            QLineEdit {
                background-color: #2c3e50; color: #ecf0f1;
                border: 1px solid #4a627a; border-radius: 4px; padding: 6px;
            }
            QLineEdit:focus { border: 1px solid #8e44ad; }
            QPushButton { 
                background-color: #16a085; border: none; color: white; padding: 8px; 
                font-size: 12px; font-weight: bold; border-radius: 4px; margin-top: 5px;
            }
            QPushButton:hover { background-color: #1abc9c; }
            QPushButton:pressed { background-color: #148f77; }
            QGroupBox { 
                font-weight: bold; font-size: 12px; padding-top: 8px; margin-top: 5px; 
                color: #bdc3c7; border: 1px solid #3e5062; border-radius: 5px;
            }
            QGroupBox::title { color: #bdc3c7; }
            QLabel { font-size: 12px; color: #ecf0f1; }
        '''
        main_group.setStyleSheet(style)

        return main_group

    # Section for Results Display
    def create_results_section(self):
        """Crear sección de resultados"""
        group = QGroupBox("Resultados")
        group.setStyleSheet('''
            QGroupBox { 
                font-weight: bold; font-size: 14px; padding-top: 10px; margin-top: 5px; 
                color: #ecf0f1; border: 1px solid #4a627a; border-radius: 5px;
            }
            QGroupBox::title { 
                color: #ecf0f1; subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px; 
            }
        ''')
        
        layout = QVBoxLayout(group)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(150)
        self.results_text.setStyleSheet('''
            QTextEdit { 
                background-color: #2c3e50; border: 1px solid #4a627a; border-radius: 4px; 
                padding: 8px; font-family: 'Consolas', 'Monaco', monospace; font-size: 12px; color: #ecf0f1; 
            }
        ''')
        
        layout.addWidget(self.results_text)
        return group

    # Section for Plotting
    def create_plot_panel(self):
        """Crear panel de gráficos"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)

        title = QLabel("Gráfico de Relaciones")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: #ecf0f1; padding: 5px 0px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, container)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        self.initialize_plot()

        return container    

    # Initialize Plot
    def initialize_plot(self):
        """Inicializa o resetea el gráfico a su estado vacío por defecto."""
        self.figure.clear()
        self.figure.set_facecolor('#34495e')
        sns.set_theme(style="darkgrid", rc={
            "axes.facecolor": "#2c3e50", 
            "figure.facecolor": "#34495e",
            "text.color": "#ecf0f1",
            "axes.labelcolor": "#ecf0f1",
            "xtick.color": "#ecf0f1",
            "ytick.color": "#ecf0f1",
            "grid.color": "#4a627a",
        })
        ax = self.figure.add_subplot(1, 1, 1)
        ax.set_title("Gráfico de Relaciones", fontsize=14, fontweight='bold', color='#ecf0f1')
        ax.set_xlabel("")
        ax.set_ylabel("")
        self.canvas.draw()

    # Get All Inputs and Results
    def get_input_values(self):
        """Obtener valores de entrada del formulario"""
        params = {}
        for var_name, field in self.input_fields.items():
            text = field.text().strip()
            params[var_name] = float(text) if text and self.validator.is_valid_number(text) else None
        
        mu = None
        if self.friction_checkbox and self.friction_checkbox.isChecked():
            mu_text = self.mu_input.text().strip()
            if mu_text and self.validator.is_valid_number(mu_text):
                mu = float(mu_text)
                if mu < 0:
                    QMessageBox.warning(self, "Valor Inválido", "El coeficiente de fricción no puede ser negativo.")
                    mu = None # Treat as no friction

        angle = None
        if self.incline_checkbox and self.incline_checkbox.isChecked():
            angle_text = self.angle_input.text().strip()
            if angle_text and self.validator.is_valid_number(angle_text):
                angle = float(angle_text)
                if not (0 <= angle <= 90):
                    QMessageBox.warning(self, "Valor Inválido", "El ángulo debe estar entre 0 y 90 grados.")
                    angle = None

        return params, mu, angle

    #Calculate Newton's Second Law
    def calculate_newton(self):
        """Realizar cálculos de la Segunda Ley de Newton"""
        try:
            params, mu, angle = self.get_input_values()
            self.results = self.calculator.calculate_newton_second_law(params, mu=mu, angle=angle)
            self.display_newton_results()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en el cálculo:\n{str(e)}")

    #Get Imput Values
    def get_input_value(self, field_dict, key):
        field = field_dict.get(key)
        if field:
            text = field.text().strip()
            if text and self.validator.is_valid_number(text):
                return float(text)
        return None

    #Get Input Values for Energy
    def get_energy_input_value(self, key):
        return self.get_input_value(self.energy_input_fields, key)

    # Get Input Values for Momentum Calculations
    def get_momentum_input_value(self, key):
        return self.get_input_value(self.momentum_input_fields, key)

    #Calculate Work
    def calculate_work(self):
        try:
            force = self.get_energy_input_value('work_force')
            distance = self.get_energy_input_value('work_distance')
            angle = self.get_energy_input_value('work_angle') or 0
            
            result = self.calculator.calculate_work(force, distance, angle)
            self.display_energy_result("Trabajo", result['work'], result['equation'], {
                'Fuerza': force, 'Distancia': distance, 'Ángulo': angle
            })
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en el cálculo de trabajo:\n{str(e)}")

    #Calculate Kinetic Energy
    def calculate_kinetic_energy(self):
        try:
            mass = self.get_energy_input_value('ke_mass')
            velocity = self.get_energy_input_value('ke_velocity')
            
            result = self.calculator.calculate_kinetic_energy(mass, velocity)
            self.display_energy_result("Energía Cinética", result['kinetic_energy'], result['equation'], {
                'Masa': mass, 'Velocidad': velocity
            })
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en el cálculo de energía cinética:\n{str(e)}")

    #Calculate Potential Energy
    def calculate_potential_energy(self):
        try:
            mass = self.get_energy_input_value('pe_mass')
            height = self.get_energy_input_value('pe_height')
            
            result = self.calculator.calculate_potential_energy(mass, height)
            self.display_energy_result("Energía Potencial", result['potential_energy'], result['equation'], {
                'Masa': mass, 'Altura': height
            })
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en el cálculo de energía potencial:\n{str(e)}")

    def display_newton_results(self):
        """Mostrar resultados en el área de texto y en el campo de entrada correspondiente"""
        if not self.results: return

        calculated_values = self.results.get('calculated_values', {})
        if calculated_values:
            calculated_var, calculated_val = list(calculated_values.items())[0]
            self.input_fields[calculated_var].setText(f"{calculated_val:.4f}")

        text = "<b style='font-size:13px;'>RESULTADOS DEL CÁLCULO (2ª Ley de Newton)</b><br>"
        text += "=" * 50 + "<br><br>"

        text += "<b>Parámetros utilizados:</b><br>"
        text += "-" * 25 + "<br>"
        param_map = {
            'f': 'Fuerza Aplicada (N)', 
            'm': 'Masa (kg)', 
            'a': 'Aceleración (m/s²)',
            'mu': 'Coef. Fricción (μ)',
            'angle': 'Ángulo del Plano (°)'
        }
        for key, value in self.results.get('input_params', {}).items():
            if value is not None:
                text += f"&nbsp;&nbsp;• {param_map.get(key, key)}: {value}<br>"

        text += "<br><b>Resultado calculado:</b><br>"
        text += "-" * 25 + "<br>"
        for key, value in calculated_values.items():
            text += f"&nbsp;&nbsp;• <span style='color:#3498db;'>{param_map.get(key, key)}</span>: {value:.4f}<br>"

        normal_force = self.results.get('normal_force')
        if normal_force is not None:
            text += "<br><b>Fuerza Normal:</b><br>"
            text += "-" * 25 + "<br>"
            text += f"&nbsp;&nbsp;• F_normal: {normal_force:.4f} N<br>"

        friction_force = self.results.get('friction_force')
        if friction_force is not None:
            text += "<br><b>Fuerza de Fricción:</b><br>"
            text += "-" * 25 + "<br>"
            text += f"&nbsp;&nbsp;• F_fricción: {friction_force:.4f} N<br>"

        text += "<br><b style='color:#9b59b6;'>Ecuaciones utilizadas:</b><br>"
        text += "-" * 25 + "<br>"
        for eq in self.results.get('equations', []):
            text += f"&nbsp;&nbsp;• {eq}<br>"
        self.results_text.setHtml(text)

    def calculate_impulse(self):
        try:
            force = self.get_momentum_input_value('impulse_force')
            time = self.get_momentum_input_value('impulse_time')
            impulse = self.get_momentum_input_value('impulse_impulse')

            result = self.calculator.calculate_impulse(force, time, impulse)
            
            # Determine which value was calculated and update the corresponding input field
            if 'impulse' in result:
                self.momentum_input_fields['impulse_impulse'].setText(f"{result['impulse']:.4f}")
                self.display_momentum_result("Impulso", result['impulse'], result['equation'], {
                    'Fuerza': force, 'Tiempo': time, 'Impulso': None
                })
            elif 'force' in result:
                self.momentum_input_fields['impulse_force'].setText(f"{result['force']:.4f}")
                self.display_momentum_result("Fuerza (Impulso)", result['force'], result['equation'], {
                    'Fuerza': None, 'Tiempo': time, 'Impulso': impulse
                })
            elif 'time' in result:
                self.momentum_input_fields['impulse_time'].setText(f"{result['time']:.4f}")
                self.display_momentum_result("Tiempo (Impulso)", result['time'], result['equation'], {
                    'Fuerza': force, 'Tiempo': None, 'Impulso': impulse
                })
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en el cálculo de impulso:\n{str(e)}")

    def calculate_linear_momentum(self):
        try:
            mass = self.get_momentum_input_value('momentum_mass')
            velocity = self.get_momentum_input_value('momentum_velocity')
            momentum = self.get_momentum_input_value('momentum_momentum')

            result = self.calculator.calculate_linear_momentum(mass, velocity, momentum)

            # Determine which value was calculated and update the corresponding input field
            if 'momentum' in result:
                self.momentum_input_fields['momentum_momentum'].setText(f"{result['momentum']:.4f}")
                self.display_momentum_result("Momento Lineal", result['momentum'], result['equation'], {
                    'Masa': mass, 'Velocidad': velocity, 'Momento': None
                })
            elif 'mass' in result:
                self.momentum_input_fields['momentum_mass'].setText(f"{result['mass']:.4f}")
                self.display_momentum_result("Masa (Momento)", result['mass'], result['equation'], {
                    'Masa': None, 'Velocidad': velocity, 'Momento': momentum
                })
            elif 'velocity' in result:
                self.momentum_input_fields['momentum_velocity'].setText(f"{result['velocity']:.4f}")
                self.display_momentum_result("Velocidad (Momento)", result['velocity'], result['equation'], {
                    'Masa': mass, 'Velocidad': None, 'Momento': momentum
                })

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en el cálculo de momento lineal:\n{str(e)}")

    def display_newton_results(self):
        """Mostrar resultados en el área de texto y en el campo de entrada correspondiente"""
        if not self.results: return

        calculated_values = self.results.get('calculated_values', {})
        if calculated_values:
            calculated_var, calculated_val = list(calculated_values.items())[0]
            self.input_fields[calculated_var].setText(f"{calculated_val:.4f}")

        text = "<b style='font-size:13px;'>RESULTADOS DEL CÁLCULO (2ª Ley de Newton)</b><br>"
        text += "=" * 50 + "<br><br>"

        text += "<b>Parámetros utilizados:</b><br>"
        text += "-" * 25 + "<br>"
        param_map = {
            'f': 'Fuerza Aplicada (N)', 
            'm': 'Masa (kg)', 
            'a': 'Aceleración (m/s²)',
            'mu': 'Coef. Fricción (μ)',
            'angle': 'Ángulo del Plano (°)'
        }
        for key, value in self.results.get('input_params', {}).items():
            if value is not None:
                text += f"&nbsp;&nbsp;• {param_map.get(key, key)}: {value}<br>"

        text += "<br><b>Resultado calculado:</b><br>"
        text += "-" * 25 + "<br>"
        for key, value in calculated_values.items():
            text += f"&nbsp;&nbsp;• <span style='color:#3498db;'>{param_map.get(key, key)}</span>: {value:.4f}<br>"

        normal_force = self.results.get('normal_force')
        if normal_force is not None:
            text += "<br><b>Fuerza Normal:</b><br>"
            text += "-" * 25 + "<br>"
            text += f"&nbsp;&nbsp;• F_normal: {normal_force:.4f} N<br>"

        friction_force = self.results.get('friction_force')
        if friction_force is not None:
            text += "<br><b>Fuerza de Fricción:</b><br>"
            text += "-" * 25 + "<br>"
            text += f"&nbsp;&nbsp;• F_fricción: {friction_force:.4f} N<br>"

        text += "<br><b style='color:#9b59b6;'>Ecuaciones utilizadas:</b><br>"
        text += "-" * 25 + "<br>"
        for eq in self.results.get('equations', []):
            text += f"&nbsp;&nbsp;• {eq}<br>"
        self.results_text.setHtml(text)

    def display_energy_result(self, title, value, equation, params):
        text = f"<b style='font-size:13px;'>RESULTADO - {title.upper()}</b><br>"
        text += "=" * 50 + "<br><br>"

        text += "<b>Parámetros:</b><br>"
        for name, val in params.items():
            if val is not None:
                text += f"&nbsp;&nbsp;• {name}: {val}<br>"
        
        text += f"<br><b>Ecuación:</b><br>&nbsp;&nbsp;• {equation}<br>"
        text += f"<br><b>Resultado:</b><br>&nbsp;&nbsp;• <span style='color:#2ecc71;'>{title}</span>: {value:.4f} Joules<br>"
        
        self.results_text.setHtml(text)

    def display_momentum_result(self, title, value, equation, params):
        text = f"<b style='font-size:13px;'>RESULTADO - {title.upper()}</b><br>"
        text += "=" * 50 + "<br><br>"

        text += "<b>Parámetros:</b><br>"
        for name, val in params.items():
            if val is not None:
                text += f"&nbsp;&nbsp;• {name}: {val}<br>"
        
        text += f"<br><b>Ecuación:</b><br>&nbsp;&nbsp;• {equation}<br>"
        
        unit = ""
        if "Impulso" in title:
            unit = "N·s"
        elif "Momento" in title:
            unit = "kg·m/s"
        elif "Fuerza" in title:
            unit = "N"
        elif "Tiempo" in title:
            unit = "s"
        elif "Masa" in title:
            unit = "kg"
        elif "Velocidad" in title:
            unit = "m/s"

        text += f"<br><b>Resultado:</b><br>&nbsp;&nbsp;• <span style='color:#2ecc71;'>{title}</span>: {value:.4f} {unit}<br>"
        
        self.results_text.setHtml(text)

    def clear_all(self):
        """Limpiar todos los campos y resultados"""
        for field in self.input_fields.values():
            field.clear()
        for field in self.energy_input_fields.values():
            field.clear()
        for field in self.momentum_input_fields.values():
            field.clear()
        if self.mu_input:
            self.mu_input.clear()
        if self.friction_checkbox:
            self.friction_checkbox.setChecked(False)
        if self.angle_input:
            self.angle_input.clear()
        if self.incline_checkbox:
            self.incline_checkbox.setChecked(False)
        
        self.results = {}
        self.results_text.clear()
        
        if hasattr(self, 'figure'):
            self.initialize_plot()

    def plot_results(self):
        """Generar gráficos de los resultados"""
        if not self.results:
            QMessageBox.warning(self, "Advertencia", "Primero debe realizar un cálculo de la Ley de Newton")
            return

        try:
            plot_data = self.calculator.generate_plot_data(self.results)
            
            if not isinstance(plot_data, dict) or not all(k in plot_data for k in ['x_data', 'y_data', 'x_label', 'y_label', 'title']):
                raise TypeError("Los datos para el gráfico son inválidos o incompletos.")

            x_data = plot_data['x_data']
            y_data = plot_data['y_data']

            if not isinstance(x_data, np.ndarray) or not isinstance(y_data, np.ndarray) or x_data.ndim != 1 or y_data.ndim != 1 or len(x_data) != len(y_data):
                raise TypeError("El formato de los datos para graficar es incorrecto.")

            if len(x_data) == 0:
                self.initialize_plot()
                return

            self.figure.clear()
            self.figure.set_facecolor('#34495e')
            sns.set_theme(style="darkgrid", rc={
                "axes.facecolor": "#2c3e50", 
                "figure.facecolor": "#34495e",
                "text.color": "#ecf0f1",
                "axes.labelcolor": "#ecf0f1",
                "xtick.color": "#ecf0f1",
                "ytick.color": "#ecf0f1",
                "grid.color": "#4a627a",
            })
            ax = self.figure.add_subplot(1, 1, 1)
            
            y_scatter = y_data.copy()
            if np.any(y_data):
                noise_scale = np.mean(np.abs(y_data)) * 0.08
                if noise_scale > 1e-9:
                    noise = np.random.normal(0, noise_scale, len(x_data))
                    y_scatter += noise

            sns.lineplot(x=x_data, y=y_data, ax=ax, color='#e74c3c', linewidth=2.5, label='Relación teórica')
            sns.scatterplot(x=x_data, y=y_scatter, ax=ax, color='#3498db', alpha=0.7, label='Datos experimentales')

            ax.set_xlabel(plot_data['x_label'], fontsize=12, color='#ecf0f1')
            ax.set_ylabel(plot_data['y_label'], fontsize=12, color='#ecf0f1')
            ax.set_title(plot_data['title'], fontsize=14, fontweight='bold', color='#ecf0f1')
            ax.legend()
            self.figure.tight_layout(pad=3.0)

            self.canvas.draw()

        except (ValueError, TypeError) as e:
            QMessageBox.critical(self, "Error de Datos", f"Ocurrió un error con los datos para el gráfico:\n\n{type(e).__name__}: {e}")
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            QMessageBox.critical(self, "Error Inesperado", f"Ocurrió un error inesperado al generar el gráfico:\n\n{type(e).__name__}: {e}\n\nDetalles:\n{error_details}")
