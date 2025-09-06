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

class MplCanvas(FigureCanvas):
    """Custom Matplotlib canvas widget to integrate with PySide6."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """Initializes the Matplotlib canvas."""
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        self.setParent(parent)
        
        # Apply a dark theme to the plot.
        fig.patch.set_facecolor('#34495e')
        self.axes.set_facecolor('#2c3e50')
        self.axes.tick_params(axis='x', colors='#ecf0f1')
        self.axes.tick_params(axis='y', colors='#ecf0f1')
        for spine in self.axes.spines.values():
            spine.set_edgecolor('#ecf0f1')

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

        title = QLabel("Relationship Plot")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        controls_layout = self.create_controls()
        layout.addLayout(controls_layout)

        self.canvas = MplCanvas(self, width=8, height=6, dpi=100)
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
        self.constant_value_input.setPlaceholderText("Value of the constant")
        self.constant_label = QLabel("Constant:")

        variables = {"Force": "f", "Mass": "m", "Acceleration": "a"}
        for name, key in variables.items():
            self.x_axis_combo.addItem(name, key)
            self.y_axis_combo.addItem(name, key)

        self.plot_btn = QPushButton("Plot")
        

        controls_layout.addWidget(QLabel("X-Axis:"), 0, 0)
        controls_layout.addWidget(self.x_axis_combo, 0, 1)
        controls_layout.addWidget(QLabel("Y-Axis:"), 1, 0)
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
            QMessageBox.warning(self, "Invalid Selection", "The X and Y axis variables cannot be the same.")
            return
        if not constant_text or not self.validator.is_valid_number(constant_text):
            QMessageBox.warning(self, "Invalid Value", "Please enter a valid numeric value for the constant.")
            return
        
        self.plot_data_requested.emit(x_var, y_var, constant_text)

    @Slot(dict)
    def plot(self, plot_params):
        try:
            plot_data = self.calculator.generate_custom_plot_data(**plot_params)
            self.draw_plot(plot_data)
        except Exception as e:
            QMessageBox.critical(self, "Plotting Error", f"An unexpected error occurred while generating the plot:\n{e}")

    def draw_plot(self, plot_data):
        self.canvas.axes.clear()
        sns.lineplot(x=plot_data['x_data'], y=plot_data['y_data'], ax=self.canvas.axes, color='#e74c3c', linewidth=2.5, label='Theoretical relationship')
        self.canvas.axes.set_xlabel(plot_data['x_label'], fontsize=12, color='#ecf0f1')
        self.canvas.axes.set_ylabel(plot_data['y_label'], fontsize=12, color='#ecf0f1')
        self.canvas.axes.set_title(plot_data['title'], fontsize=14, fontweight='bold', color='#ecf0f1')
        self.canvas.axes.grid(True, color='#4a627a', linestyle='--', linewidth=0.5)
        
        legend = self.canvas.axes.legend(fontsize=11)
        legend.get_frame().set_facecolor('#34495e')
        legend.get_frame().set_edgecolor('#4a627a')
        for text in legend.get_texts():
            text.set_color('#ecf0f1')

        self.canvas.draw()

    @Slot()
    def initialize_plot(self):
        self.canvas.axes.clear()
        self.canvas.axes.set_title("Relationship Plot", color='#ecf0f1')
        self.canvas.axes.set_xlabel("Select variable for X-axis", color='#ecf0f1')
        self.canvas.axes.set_ylabel("Select variable for Y-axis", color='#ecf0f1')
        self.canvas.axes.grid(True, color='#4a627a', linestyle='--', linewidth=0.5)
        self.canvas.draw()

    def update_constant_variable(self):
        x_var = self.x_axis_combo.currentData()
        y_var = self.y_axis_combo.currentData()
        all_vars = {"f", "m", "a"}
        selected_vars = {x_var, y_var}
        if len(selected_vars) < 2:
            self.constant_label.setText("Invalid")
            self.constant_value_input.setEnabled(False)
            return
        constant_var_key = list(all_vars - selected_vars)[0]
        var_map = {"f": "Force (N)", "m": "Mass (kg)", "a": "Acceleration (m/s²)"}
        self.constant_label.setText(f"{var_map[constant_var_key]} (constant):")
        self.constant_value_input.setEnabled(True)
