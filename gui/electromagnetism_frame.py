"""
Electromagnetism Frame for the CPhysics application.

This module defines the main UI for the electromagnetism section,
allowing users to perform calculations related to Coulomb's Law and
visualize electric fields.
"""

from PySide6.QtWidgets import (QWidget, QHBoxLayout, QSplitter, QMessageBox, 
                                QScrollArea, QVBoxLayout)
from PySide6.QtCore import Qt

from modules.electromagnetism import ElectromagnetismCalculator
from utils.validators import InputValidator
from gui.electromagnetism.control_panel import ControlPanel
from gui.electromagnetism.results_panel import ResultsPanel
from gui.electromagnetism.plot_panel import PlotPanel

class ElectromagnetismFrame(QWidget):
    """
    Main widget for the Electromagnetism module.

    Integrates the control panel for user input, the results panel
    for displaying calculation outputs, and the plot panel for visualizing
    the electric field.
    """
    def __init__(self, parent=None):
        """Initializes the ElectromagnetismFrame and its components."""
        super().__init__(parent)
        
        self.calculator = ElectromagnetismCalculator()
        self.validator = InputValidator()
        self.results = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        """Sets up the graphical user interface for the electromagnetism frame."""
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # --- Left Panel (Controls & Results) ---
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)

        self.control_panel = ControlPanel()
        self.results_panel = ResultsPanel()

        left_layout.addWidget(self.control_panel)
        left_layout.addWidget(self.results_panel)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumWidth(400)
        scroll_area.setWidget(left_container)

        # --- Right Panel (Plot) ---
        self.plot_panel = PlotPanel()
        
        splitter.addWidget(scroll_area)
        splitter.addWidget(self.plot_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        # --- Signal Connections ---
        self.control_panel.calculate_btn.clicked.connect(self.calculate)
        self.control_panel.clear_btn.clicked.connect(self.clear_all)
        self.control_panel.plot_btn.clicked.connect(self.plot_results)

    def calculate(self):
        """Retrieves input, performs the calculation, and displays the results."""
        try:
            params = self.control_panel.get_input_values(self.validator)
            self.results = self.calculator.calculate_coulomb_force(params)
            self.results_panel.display_results(self.results, self.control_panel.input_fields)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error in calculation: {str(e)}")

    def clear_all(self):
        """Clears all input fields, results, and the plot."""
        self.control_panel.clear_fields()
        self.results_panel.clear()
        self.plot_panel.clear_plot()
        self.results = {}

    def plot_results(self):
        """Plots the electric field based on the last calculation results."""
        if not self.results:
            QMessageBox.warning(self, "Warning", "You must perform a calculation first.")
            return
        self.plot_panel.plot_results(self.results, self.calculator)