
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSplitter, QMessageBox, QScrollArea, QVBoxLayout
from PySide6.QtCore import Qt

from modules.thermodynamics import ThermodynamicsCalculator
from gui.thermodynamics.control_panel import ControlPanel
from gui.thermodynamics.results_panel import ResultsPanel
from gui.thermodynamics.plot_panel import PlotPanel

class ThermodynamicsFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.calculator = ThermodynamicsCalculator()
        self.results = {}
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Left panel (controls and results)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0,0,0,0)
        self.control_panel = ControlPanel()
        self.results_panel = ResultsPanel()
        left_layout.addWidget(self.control_panel)
        left_layout.addWidget(self.results_panel)
        left_layout.addStretch()
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumWidth(400)
        scroll_area.setWidget(left_widget)

        # Right panel (plot)
        self.plot_panel = PlotPanel()

        splitter.addWidget(scroll_area)
        splitter.addWidget(self.plot_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

    def connect_signals(self):
        self.control_panel.calculate_btn.clicked.connect(self.calculate)
        self.control_panel.clear_btn.clicked.connect(self.clear_all)
        self.control_panel.plot_btn.clicked.connect(self.plot_results)

    def calculate(self):
        try:
            params = self.control_panel.get_input_values()
            self.results = self.calculator.calculate_ideal_gas_law(params)
            self.results_panel.display_results(self.results)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def clear_all(self):
        self.control_panel.clear_fields()
        self.results_panel.clear_results()
        self.results = {}

    def plot_results(self):
        try:
            input_values = self.control_panel.get_input_values()
            self.plot_panel.plot(input_values, self.calculator)
        except Exception as e:
            QMessageBox.critical(self, "Error de Graficación", f"No se pudo generar el gráfico: {e}")
