import numpy as np
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QSplitter, QMessageBox, QVBoxLayout, QScrollArea
)
from PySide6.QtCore import Qt
import seaborn as sns

from modules.waves import WavesCalculator
from utils.validators import InputValidator
from gui.waves.control_panel import ControlPanel
from gui.waves.results_panel import ResultsPanel
from gui.waves.plot_panel import PlotPanel

class WavesFrame(QWidget):
    """
    A widget for wave physics calculations and visualizations,
    assembled from control, results, and plot panels.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.calculator = WavesCalculator()
        self.validator = InputValidator()
        self.results = {}
        self.setup_ui()

    def setup_ui(self):
        """Initializes and organizes the user interface components."""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Left panels (control and results)
        left_panel_container = QWidget()
        left_layout = QVBoxLayout(left_panel_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(15)

        self.control_panel = ControlPanel()
        self.results_panel = ResultsPanel()

        left_layout.addWidget(self.control_panel)
        left_layout.addWidget(self.results_panel)
        left_layout.addStretch()

        # Wrap the left panel in a QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(left_panel_container)
        scroll_area.setMinimumWidth(400)

        splitter.addWidget(scroll_area)

        # Right panel (plot)
        self.plot_panel = PlotPanel()
        splitter.addWidget(self.plot_panel)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        self.connect_signals()

    def connect_signals(self):
        """Connects button signals to event handlers."""
        self.control_panel.calc_button.clicked.connect(self.calculate_and_display)
        self.control_panel.plot_button.clicked.connect(self.plot_wave)
        self.control_panel.clear_button.clicked.connect(self.clear_all)

    def get_input_values(self):
        """Retrieves and validates input values from the control panel."""
        values = {}
        raw_values = self.control_panel.get_input_values()
        for name, value in raw_values.items():
            if value is not None:
                if not self.validator.is_valid_number(str(value)):
                    raise ValueError(f"Invalid value for {name}: '{value}'")
                values[name] = float(value)
            else:
                values[name] = None
        return values

    def calculate_and_display(self):
        """Calculates properties and updates the results and input panels."""
        try:
            params = self.get_input_values()
            self.results = self.calculator.calculate_wave_properties(params)
            self.results_panel.display_results(self.results)
            self.update_inputs_with_results()
        except ValueError as e:
            QMessageBox.warning(self, "Insufficient Data", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Calculation Error", f"An error occurred: {e}")

    def update_inputs_with_results(self):
        """Fills input fields with calculated values."""
        if 'calculated_values' in self.results:
            for key, value in self.results['calculated_values'].items():
                if key in self.control_panel.inputs:
                    self.control_panel.inputs[key].setText(f"{value:.4f}")

    def plot_wave(self):
        """Generates a plot of the wave at an instant t=0."""
        if not self.results or 'all_values' not in self.results:
            self.calculate_and_display()
            if not self.results or 'all_values' not in self.results:
                QMessageBox.warning(self, "Warning", "You must first perform a calculation.")
                return

        vals = self.results['all_values']
        A = vals.get('amplitude')
        wavelength = vals.get('wavelength')
        k = vals.get('wave_number')
        phi = vals.get('phase', 0)

        if not all(v is not None for v in [A, wavelength, k]):
            QMessageBox.warning(self, "Insufficient Data",
                                "Amplitude and Wavelength are needed to plot.")
            return

        try:
            canvas = self.plot_panel.canvas
            canvas.axes.clear()

            x = np.linspace(0, 2 * wavelength, 500)
            y = A * np.cos(k * x + phi)

            sns.lineplot(x=x, y=y, ax=canvas.axes, color='#3498db', linewidth=2.5, label='Wave at t=0')
            canvas.axes.set_xlabel('Position (x) [m]', fontsize=12, color='#ecf0f1')
            canvas.axes.set_ylabel('Amplitude (y) [m]', fontsize=12, color='#ecf0f1')
            canvas.axes.set_title('Wave Profile (y vs x)', fontsize=14, fontweight='bold', color='#ecf0f1')
            canvas.axes.grid(True, color='#4a627a', linestyle='--', linewidth=0.5)
            canvas.axes.axhline(0, color='#7f8c8d', linewidth=0.8)
            
            legend = canvas.axes.legend(fontsize=11)
            legend.get_frame().set_facecolor('#34495e')
            legend.get_frame().set_edgecolor('#4a627a')
            for text in legend.get_texts():
                text.set_color('#ecf0f1')

            canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Plotting Error", f"An error occurred while plotting: {e}")

    def clear_all(self):
        """Clears all input fields, results, and the plot."""
        self.control_panel.clear()
        self.results_panel.clear()
        self.results = {}

        canvas = self.plot_panel.canvas
        canvas.axes.clear()
        canvas.axes.set_title("Wave Plot", color='#ecf0f1')
        canvas.axes.grid(True, color='#4a627a', linestyle='--', linewidth=0.5)
        canvas.draw()