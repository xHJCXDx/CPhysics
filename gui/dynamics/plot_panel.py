
import numpy as np
import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QLabel, 
                                QLineEdit, QComboBox, QPushButton, QMessageBox)
from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtGui import QFont

from modules.dynamics import DynamicsCalculator
from utils.validators import InputValidator

class PlotPanel(QWidget):
    # Signal to request data needed for plotting from the main frame
    plot_data_requested = Signal(str, str, str) # x_var, y_var, constant_value

    def __init__(self, parent=None):
        super().__init__(parent)
        self.calculator = DynamicsCalculator()
        self.validator = InputValidator()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        title = QLabel("Gráfico de Relaciones")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: #ecf0f1; padding: 5px 0px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        controls_layout = self.create_controls()
        layout.addLayout(controls_layout)

        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        self.initialize_plot()
        self.update_constant_variable()

    def create_controls(self):
        controls_layout = QGridLayout()
        self.x_axis_combo = QComboBox()
        self.y_axis_combo = QComboBox()
        self.constant_value_input = QLineEdit()
        self.constant_value_input.setPlaceholderText("Valor de la constante")
        self.constant_label = QLabel("Constante:")

        variables = {"Fuerza": "f", "Masa": "m", "Aceleración": "a"}
        for name, key in variables.items():
            self.x_axis_combo.addItem(name, key)
            self.y_axis_combo.addItem(name, key)

        self.plot_btn = QPushButton("Graficar")
        self.plot_btn.setStyleSheet('''QPushButton { background-color: #8e44ad; border: none; color: white; padding: 8px 16px; font-size: 12px; font-weight: bold; border-radius: 4px; min-width: 80px; } QPushButton:hover { background-color: #9b59b6; } QPushButton:pressed { background-color: #7d3c98; }''')

        controls_layout.addWidget(QLabel("Eje X:"), 0, 0)
        controls_layout.addWidget(self.x_axis_combo, 0, 1)
        controls_layout.addWidget(QLabel("Eje Y:"), 1, 0)
        controls_layout.addWidget(self.y_axis_combo, 1, 1)
        controls_layout.addWidget(self.constant_label, 2, 0)
        controls_layout.addWidget(self.constant_value_input, 2, 1)
        controls_layout.addWidget(self.plot_btn, 3, 0, 1, 2)

        self.x_axis_combo.currentIndexChanged.connect(self.update_constant_variable)
        self.y_axis_combo.currentIndexChanged.connect(self.update_constant_variable)
        self.plot_btn.clicked.connect(self.request_plot_data)
        return controls_layout

    @Slot()
    def request_plot_data(self):
        x_var = self.x_axis_combo.currentData()
        y_var = self.y_axis_combo.currentData()
        constant_text = self.constant_value_input.text().strip()

        if x_var == y_var:
            QMessageBox.warning(self, "Selección Inválida", "Las variables de los ejes X e Y no pueden ser iguales.")
            return
        if not constant_text or not self.validator.is_valid_number(constant_text):
            QMessageBox.warning(self, "Valor Inválido", "Por favor, ingrese un valor numérico válido para la constante.")
            return
        
        self.plot_data_requested.emit(x_var, y_var, constant_text)

    @Slot(dict)
    def plot(self, plot_params):
        try:
            plot_data = self.calculator.generate_custom_plot_data(**plot_params)
            self.draw_plot(plot_data)
        except Exception as e:
            QMessageBox.critical(self, "Error al Graficar", f"Ocurrió un error inesperado al generar el gráfico:\n{e}")

    def draw_plot(self, plot_data):
        self.figure.clear()
        self.figure.set_facecolor('#34495e')
        sns.set_theme(style="darkgrid", rc={
            "axes.facecolor": "#2c3e50", "figure.facecolor": "#34495e",
            "text.color": "#ecf0f1", "axes.labelcolor": "#ecf0f1",
            "xtick.color": "#ecf0f1", "ytick.color": "#ecf0f1", "grid.color": "#4a627a",
        })
        ax = self.figure.add_subplot(1, 1, 1)
        sns.lineplot(x=plot_data['x_data'], y=plot_data['y_data'], ax=ax, color='#e74c3c', linewidth=2.5, label='Relación teórica')
        ax.set_xlabel(plot_data['x_label'], fontsize=12)
        ax.set_ylabel(plot_data['y_label'], fontsize=12)
        ax.set_title(plot_data['title'], fontsize=14, fontweight='bold')
        ax.legend()
        self.figure.tight_layout(pad=3.0)
        self.canvas.draw()

    @Slot()
    def initialize_plot(self):
        self.figure.clear()
        self.figure.set_facecolor('#34495e')
        ax = self.figure.add_subplot(1, 1, 1)
        ax.set_title("Gráfico de Relaciones")
        ax.set_xlabel("Seleccione variable para el eje X")
        ax.set_ylabel("Seleccione variable para el eje Y")
        self.canvas.draw()

    def update_constant_variable(self):
        x_var = self.x_axis_combo.currentData()
        y_var = self.y_axis_combo.currentData()
        all_vars = {"f", "m", "a"}
        selected_vars = {x_var, y_var}
        if len(selected_vars) < 2:
            self.constant_label.setText("Inválido")
            self.constant_value_input.setEnabled(False)
            return
        constant_var_key = list(all_vars - selected_vars)[0]
        var_map = {"f": "Fuerza (N)", "m": "Masa (kg)", "a": "Aceleración (m/s²)"}
        self.constant_label.setText(f"{var_map[constant_var_key]} (constante):")
        self.constant_value_input.setEnabled(True)
