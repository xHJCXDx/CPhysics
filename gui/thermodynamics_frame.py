"""
Main frame for the Thermodynamics module.
Focuses on the Ideal Gas Law UI and logic.
"""

from PySide6.QtWidgets import (QWidget, QHBoxLayout, QSplitter, QMessageBox, 
                                QScrollArea, QVBoxLayout)
from PySide6.QtCore import Qt

from modules.thermodynamics import ThermodynamicsCalculator
from gui.thermodynamics.control_panel import ControlPanel
from gui.thermodynamics.results_panel import ResultsPanel
from gui.thermodynamics.plot_panel import PlotPanel

class ThermodynamicsFrame(QWidget):
    """Main widget for the Thermodynamics module. Integrates input, results, and plot panels."""
    def __init__(self, parent=None):
        """Initialize UI and components."""
        super().__init__(parent)
        self.calculator = ThermodynamicsCalculator()
        self.results = {}
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        """Set up the graphical user interface."""
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # --- Left Panel (Controls and Results) ---
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        self.control_panel = ControlPanel()
        self.results_panel = ResultsPanel()
        
        left_layout.addWidget(self.control_panel)
        left_layout.addWidget(self.results_panel)
        left_layout.addStretch()
        
        # The scroll area ensures content is accessible on smaller window sizes.
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumWidth(400)
        scroll_area.setWidget(left_widget)

        # --- Right Panel (Plot) ---
        self.plot_panel = PlotPanel()

        splitter.addWidget(scroll_area)
        splitter.addWidget(self.plot_panel)
        
        # Adjust the initial size ratio.
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

    def connect_signals(self):
        """Connects signals from the control panel to the appropriate slots."""
        self.control_panel.calculate_btn.clicked.connect(self.calculate)
        self.control_panel.clear_btn.clicked.connect(self.clear_all)
        self.control_panel.plot_btn.clicked.connect(self.plot_results)

    def calculate(self):
        """Performs the ideal gas law calculation and displays the results."""
        try:
            params = self.control_panel.get_input_values()
            self.results = self.calculator.calculate_ideal_gas_law(params)
            self.results_panel.display_results(self.results)
        except ValueError as e:
            QMessageBox.critical(self, "Input Error", f"Invalid input: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Calculation Error", f"An unexpected error occurred: {e}")

    def clear_all(self):
        """Clears all input fields, results, and the plot."""
        self.control_panel.clear_fields()
        self.results_panel.clear()
        self.plot_panel.clear_plot()
        self.results = {}

    def plot_results(self):
        """Plots the thermodynamic processes based on the user's input."""
        try:
            input_values = self.control_panel.get_input_values()
            self.plot_panel.plot(input_values, self.calculator)
        except ValueError as e:
            QMessageBox.critical(self, "Input Error", f"Invalid input for plotting: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Plotting Error", f"Could not generate plot: {e}")