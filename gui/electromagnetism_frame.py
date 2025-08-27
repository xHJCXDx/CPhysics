"""
Interfaz gráfica para el módulo de electromagnetismo
Permite calcular problemas relacionados con la Ley de Coulomb y campos eléctricos.
"""

from PySide6.QtWidgets import (QWidget, QHBoxLayout, QSplitter, QMessageBox, QScrollArea, QVBoxLayout)
from PySide6.QtCore import Qt

from modules.electromagnetism import ElectromagnetismCalculator
from utils.validators import InputValidator
from gui.electromagnetism.control_panel import ControlPanel
from gui.electromagnetism.results_panel import ResultsPanel
from gui.electromagnetism.plot_panel import PlotPanel

class ElectromagnetismFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.calculator = ElectromagnetismCalculator()
        self.validator = InputValidator()
        self.results = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Paneles
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

        self.plot_panel = PlotPanel()
        
        splitter.addWidget(scroll_area)
        splitter.addWidget(self.plot_panel)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        # Conexiones
        self.control_panel.calculate_btn.clicked.connect(self.calculate)
        self.control_panel.clear_btn.clicked.connect(self.clear_all)
        self.control_panel.plot_btn.clicked.connect(self.plot_results)

    def calculate(self):
        try:
            params = self.control_panel.get_input_values(self.validator)
            self.results = self.calculator.calculate_coulomb_force(params)
            self.results_panel.display_results(self.results, self.control_panel.input_fields)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en el cálculo:\n{str(e)}")

    def clear_all(self):
        self.control_panel.clear_fields()
        self.results_panel.clear()
        self.plot_panel.clear_plot()
        self.results = {}

    def plot_results(self):
        if not self.results:
            QMessageBox.warning(self, "Advertencia", "Primero debe realizar un cálculo")
            return
        self.plot_panel.plot_results(self.results, self.calculator)