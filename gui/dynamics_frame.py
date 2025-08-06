"""
Interfaz gráfica para el módulo de dinámica
Permite calcular problemas de la Segunda Ley de Newton
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

from modules.dynamics import DynamicsCalculator
from utils.validators import InputValidator

class DynamicsFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Inicializar calculadora y validador
        self.calculator = DynamicsCalculator()
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
        title = QLabel("Dinámica - Segunda Ley de Newton")
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
            ('f', 'Fuerza (N):'),
            ('m', 'Masa (kg):'),
            ('a', 'Aceleración (m/s²):'),
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
        """Realizar cálculos de la Segunda Ley de Newton"""
        try:
            params = self.get_input_values()
            self.results = self.calculator.calculate_newton_second_law(params)
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
            self.input_fields[calculated_var].setText(f"{calculated_val:.4f}")

        # Formatear el texto de resultados de manera detallada
        text = "<b style='font-size:13px;'>RESULTADOS DEL CÁLCULO</b><br>"
        text += "=" * 50 + "<br><br>"

        # Mostrar parámetros utilizados
        text += "<b>Parámetros utilizados:</b><br>"
        text += "-" * 25 + "<br>"
        param_map = {'f': 'Fuerza (N)', 'm': 'Masa (kg)', 'a': 'Aceleración (m/s²)'}
        for key, value in self.results.get('input_params', {}).items():
            if value is not None:
                text += f"&nbsp;&nbsp;• {param_map.get(key, key)}: {value}<br>"

        text += "<br><b>Resultado calculado:</b><br>"
        text += "-" * 25 + "<br>"
        for key, value in calculated_values.items():
            text += f"&nbsp;&nbsp;• <span style='color:#3498db;'>{param_map.get(key, key)}</span>: {value:.4f}<br>"

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
            
            plot_data = self.calculator.generate_plot_data(self.results)

            # Para hacer el gráfico más ilustrativo, simulamos puntos de datos con algo de ruido
            # y usamos regplot de seaborn para mostrar la tendencia lineal.
            x_data = plot_data['x_data']
            y_data = plot_data['y_data']
            
            # Añadir ruido gausiano para simular datos experimentales
            noise = np.random.normal(0, np.mean(np.abs(y_data)) * 0.08, len(x_data))
            y_scatter = y_data + noise
            
            # Usar regplot para mostrar los puntos y la línea de regresión
            sns.regplot(x=x_data, y=y_scatter, ax=ax,
                        scatter_kws={'color': '#3498db', 'alpha': 0.7},
                        line_kws={'color': '#e74c3c', 'linewidth': 2.5, 'label': 'Ajuste lineal (F=ma)'})

            ax.set_xlabel(plot_data['x_label'], fontsize=12, color='#ecf0f1')
            ax.set_ylabel(plot_data['y_label'], fontsize=12, color='#ecf0f1')
            ax.set_title(plot_data['title'], fontsize=14, fontweight='bold', color='#ecf0f1')
            ax.legend()
            self.figure.tight_layout(pad=3.0)

            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar gráfico:\n{str(e)}")