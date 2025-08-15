"""
Interfaz gráfica para el módulo de termodinámica
Permite calcular problemas de la Ley de los Gases Ideales y visualizar sus relaciones.
"""

import numpy as np
import seaborn as sns
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QSplitter,
    QGroupBox, QLabel, QLineEdit, QPushButton,
    QTextEdit, QScrollArea, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from modules.thermodynamics import ThermodynamicsCalculator
# from utils.validators import InputValidator

class ThermodynamicsFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.calculator = ThermodynamicsCalculator()
        # self.validator = InputValidator()
        self.results = {}
        self.input_fields = {}
        self.setup_ui()

    # Initializa la interfaz de usuario
    def setup_ui(self):
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

    # Crea el panel de control con los campos de entrada y botones
    def create_control_panel(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumWidth(400)

        container = QWidget()
        scroll_area.setWidget(container)

        layout = QVBoxLayout(container)
        layout.setSpacing(15)

        title = QLabel("Termodinámica - Ejemplo")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #ecf0f1; padding: 10px 0px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        params_group = self.create_parameters_section()
        layout.addWidget(params_group)

        buttons_layout = self.create_action_buttons()
        layout.addLayout(buttons_layout)

        results_group = self.create_results_section()
        layout.addWidget(results_group)

        layout.addStretch()
        return scroll_area

    # Crea la sección de parámetros de entrada
    def create_parameters_section(self):
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
            ('P', 'Presión (atm):'),
            ('V', 'Volumen (L):'),
            ('n', 'Moles (mol):'),
            ('T', 'Temperatura (K):'),
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

    # Crea los botones de acción para calcular, limpiar y graficar
    def create_action_buttons(self):
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

    # Crea la sección de resultados para mostrar los cálculos
    def create_results_section(self):
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

    # Crea el panel de gráficos para visualizar relaciones
    def create_plot_panel(self):
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

    # Obtiene los valores de entrada de los campos
    def get_input_values(self):
        params = {}
        for var_name, field in self.input_fields.items():
            text = field.text().strip()
            params[var_name] = float(text) if text else None
        return params

    # Calcula los resultados usando la Ley de los Gases Ideales
    def calculate(self):
        try:
            params = self.get_input_values()
            self.results = self.calculator.calculate_ideal_gas_law(params)
            self.display_results()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # Muestra los resultados en el área de texto
    def display_results(self):
        if not self.results:
            self.results_text.setText("No hay resultados.")
            return
        res = self.results
        txt = "Parámetros de entrada:\n"
        for k, v in res['input_params'].items():
            txt += f"  {k}: {v}\n"
        txt += "\nResultado calculado:\n"
        for k, v in res['calculated_values'].items():
            txt += f"  {k}: {v}\n"
        txt += "\nEcuaciones usadas:\n"
        for eq in res['equations']:
            txt += f"  {eq}\n"
        self.results_text.setText(txt)

    # Limpia todos los campos de entrada y resultados
    def clear_all(self):
        for field in self.input_fields.values():
            field.clear()
        self.results_text.clear()
        self.results = {}

    # Plotea los resultados usando seaborn
    def plot_results(self):
        """Ejemplo de gráfico usando seaborn"""
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
        # Ejemplo: graficar P vs T si V y n son fijos
        V = self.input_fields['V'].text()
        n = self.input_fields['n'].text()
        try:
            V = float(V) if V else 1.0
            n = float(n) if n else 1.0
        except Exception:
            V = 1.0
            n = 1.0
        T = np.linspace(200, 600, 20)
        P = (n * self.calculator.R * T) / V
        sns.lineplot(x=T, y=P, ax=ax, color='#e74c3c', linewidth=2.5, label='P vs T (V y n fijos)')
        ax.set_xlabel("Temperatura (K)", fontsize=12, color='#ecf0f1')
        ax.set_ylabel("Presión (atm)", fontsize=12, color='#ecf0f1')
        ax.set_title("Relación P vs T (Ley de Gases Ideales)", fontsize=14, fontweight='bold', color='#ecf0f1')
        ax.legend()
        self.figure.tight_layout(pad=3.0)
        self.canvas.draw()