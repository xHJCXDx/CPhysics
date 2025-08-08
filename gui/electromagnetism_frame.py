"""
Interfaz gráfica para el módulo de electromagnetismo
Permite calcular problemas relacionados con la Ley de Coulomb y campos eléctricos.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QSplitter,
                                QGroupBox, QLabel, QLineEdit, QPushButton,
                                QTextEdit, QScrollArea, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import seaborn as sns
import numpy as np

from modules.electromagnetism import ElectromagnetismCalculator
from utils.validators import InputValidator

class ElectromagnetismFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Inicializar calculadora y validador
        self.calculator = ElectromagnetismCalculator()
        self.validator = InputValidator()
        
        # Variables para almacenar resultados
        self.results = {}
        self.input_fields = {}
        
        # Configurar la interfaz
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        main_layout = QHBoxLayout(self) # Layout principal
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
        splitter.setStretchFactor(0, 1) # Panel izquierdo
        splitter.setStretchFactor(1, 1) # Panel derecho
    
    def create_control_panel(self):
        """Crear panel de controles y resultados"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumWidth(400)
        
        container = QWidget()
        scroll_area.setWidget(container)
        
        layout = QVBoxLayout(container)
        layout.setSpacing(15)
        
        # Título del módulo
        title = QLabel("Electromagnetismo - Ley de Coulomb")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #ecf0f1; padding: 10px 0px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Sección de parámetros
        params_group = self.create_parameters_section()
        layout.addWidget(params_group)
        
        # Botones de acción
        buttons_layout = self.create_action_buttons()
        layout.addLayout(buttons_layout)
        
        # Sección de resultados
        results_group = self.create_results_section()
        layout.addWidget(results_group)
        
        layout.addStretch()
        
        return scroll_area
    
    def create_parameters_section(self):
        """Crear sección de parámetros"""
        group = QGroupBox("Parámetros (deje uno en blanco para calcular)")
        group.setStyleSheet("""
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
        """)
        
        layout = QGridLayout(group)
        layout.setSpacing(8)
        
        params_info = [
            ('q1', 'Carga 1 (C):'),
            ('q2', 'Carga 2 (C):'),
            ('r', 'Distancia (m):'),
            ('F', 'Fuerza (N):'),
        ]
        
        for i, (var_name, label_text) in enumerate(params_info):
            label = QLabel(label_text)
            line_edit = QLineEdit()
            line_edit.setPlaceholderText("Valor conocido")
            line_edit.setStyleSheet("""
                QLineEdit {
                    background-color: #2c3e50;
                    color: #ecf0f1;
                    border: 1px solid #4a627a;
                    border-radius: 4px;
                    padding: 6px;
                }
                QLineEdit:focus { border: 1px solid #8e44ad; }
            """)
            self.input_fields[var_name] = line_edit
            layout.addWidget(label, i, 0)
            layout.addWidget(line_edit, i, 1)
        
        return group
    
    def create_action_buttons(self):
        """Crear botones de acción"""
        layout = QHBoxLayout()
        layout.setSpacing(10)
        
        self.calculate_btn = QPushButton("Calcular")
        self.clear_btn = QPushButton("Limpiar")
        self.plot_btn = QPushButton("Graficar")
        
        button_style = """
            QPushButton { 
                background-color: #8e44ad; border: none; color: white; padding: 8px 16px; 
                font-size: 12px; font-weight: bold; border-radius: 4px; min-width: 80px; 
            }
            QPushButton:hover { background-color: #9b59b6; }
            QPushButton:pressed { background-color: #7d3c98; }
        """
        for btn in [self.calculate_btn, self.clear_btn, self.plot_btn]:
            btn.setStyleSheet(button_style)
        
        self.calculate_btn.clicked.connect(self.calculate)
        self.clear_btn.clicked.connect(self.clear_all)
        self.plot_btn.clicked.connect(self.plot_results)
        
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
                font-weight: bold; font-size: 14px; padding-top: 10px; margin-top: 5px; 
                color: #ecf0f1; border: 1px solid #4a627a; border-radius: 5px;
            }
            QGroupBox::title { 
                color: #ecf0f1; subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px; 
            }
        """)
        
        layout = QVBoxLayout(group)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(150)
        self.results_text.setStyleSheet("""
            QTextEdit { 
                background-color: #2c3e50; border: 1px solid #4a627a; border-radius: 4px; 
                padding: 8px; font-family: 'Consolas', 'Monaco', monospace; font-size: 12px; color: #ecf0f1; 
            }
        """)
        
        layout.addWidget(self.results_text)
        return group

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
        self.figure.patch.set_facecolor('#34495e')
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, container)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        return container
        
    def get_input_values(self):
        """Obtener valores de entrada del formulario"""
        params = {}
        for var_name, field in self.input_fields.items():
            text = field.text().strip()
            params[var_name] = float(text) if text and self.validator.is_valid_number(text) else None
        return params

    def calculate(self):
        """Realizar cálculos de la Ley de Coulomb"""
        try:
            params = self.get_input_values()
            self.results = self.calculator.calculate_coulomb_force(params)
            self.display_results()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en el cálculo:\n{str(e)}")

    def display_results(self):
        """Mostrar resultados en el área de texto y en el campo de entrada correspondiente"""
        if not self.results: return

        # Rellenar el campo de entrada calculado
        calculated_values = self.results.get('calculated_values', {})
        if calculated_values:
            calculated_var, calculated_val = list(calculated_values.items())[0]
            self.input_fields[calculated_var].setText(f"{calculated_val:.4e}") # Usar notación científica para cargas y fuerza

        # Formatear el texto de resultados de manera detallada
        text = "<b style='font-size:13px;'>RESULTADOS DEL CÁLCULO</b><br>"
        text += "=" * 50 + "<br><br>"

        # Mostrar parámetros utilizados
        text += "<b>Parámetros utilizados:</b><br>"
        text += "-" * 25 + "<br>"
        param_map = {'q1': 'Carga 1 (C)', 'q2': 'Carga 2 (C)', 'r': 'Distancia (m)', 'F': 'Fuerza (N)'}
        for key, value in self.results.get('input_params', {}).items():
            if value is not None:
                text += f"&nbsp;&nbsp;• {param_map.get(key, key)}: {value:.4e}<br>" # Notación científica

        text += "<br><b>Resultado calculado:</b><br>"
        text += "-" * 25 + "<br>"
        for key, value in calculated_values.items():
            text += f"&nbsp;&nbsp;• <span style='color:#3498db;'>{param_map.get(key, key)}</span>: {value:.4e}<br>" # Notación científica

        # Mostrar ecuaciones utilizadas
        text += "<br><b style='color:#9b59b6;'>Ecuación utilizada:</b><br>"
        text += "-" * 25 + "<br>"
        text += f"&nbsp;&nbsp;• {self.results['equations'][0]}<br>"
        self.results_text.setHtml(text)

    def clear_all(self):
        """Limpiar todos los campos y resultados"""
        for field in self.input_fields.values():
            field.clear()
        self.results = {}
        self.results_text.clear()
        
        # Limpiar gráficos
        if hasattr(self, 'figure'):
            self.figure.clear()
            ax = self.figure.add_subplot(1, 1, 1)
            self.plot_results() # Redraw empty plot with dark theme
            self.canvas.draw()

    def plot_results(self):
        """Generar gráficos de los resultados"""
        if not self.results:
            QMessageBox.warning(self, "Advertencia", "Primero debe realizar un cálculo")
            return

        try:
            self.figure.clear()
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
            
            # La Ley de Coulomb es F = K * |q1*q2| / r^2
            # Podemos graficar F vs r, o F vs q1 (manteniendo q2 y r constantes)
            # Para simplificar, graficaremos F vs r, asumiendo q1 y q2 son las cargas dadas
            
            input_params = self.results.get('input_params', {})
            calculated_values = self.results.get('calculated_values', {})
            all_values = {**input_params, **calculated_values}

            q1 = all_values.get('q1')
            q2 = all_values.get('q2')
            F_calc = all_values.get('F')
            r_calc = all_values.get('r')

            if q1 is None or q2 is None:
                QMessageBox.warning(self, "Advertencia", "Se necesitan los valores de q1 y q2 para graficar la relación F vs r.")
                return
            
            # Rango de distancia (r) para la gráfica
            # Si r fue calculado, usarlo como referencia, si no, usar un rango por defecto
            r_min_plot = 0.1 # Evitar división por cero
            r_max_plot = 10.0
            if r_calc is not None:
                r_min_plot = max(0.01, r_calc * 0.1)
                r_max_plot = r_calc * 2.0

            r_values = np.linspace(r_min_plot, r_max_plot, 100)
            F_values = (self.calculator.K * abs(q1 * q2)) / (r_values**2)

            sns.lineplot(x=r_values, y=F_values, ax=ax, color='#3498db', linewidth=2.5, label='Fuerza vs Distancia')
            
            # Marcar el punto calculado si r y F están disponibles
            if r_calc is not None and F_calc is not None:
                ax.plot(r_calc, F_calc, 'o', color='#e74c3c', markersize=8, label=f'Punto calculado (r={r_calc:.2f}m, F={F_calc:.2e}N)')

            ax.set_xlabel('Distancia (r) [m]', fontsize=12, color='#ecf0f1')
            ax.set_ylabel('Fuerza (F) [N]', fontsize=12, color='#ecf0f1')
            ax.set_title('Ley de Coulomb: Fuerza vs Distancia', fontsize=14, fontweight='bold', color='#ecf0f1')
            ax.legend()
            self.figure.tight_layout(pad=3.0)

            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar gráfico:\n{str(e)}")