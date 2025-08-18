from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSplitter, 
                                QScrollArea, QLabel, QPushButton)
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont

from gui.dynamics.newton_law_panel import NewtonLawPanel
from gui.dynamics.energy_panel import EnergyPanel
from gui.dynamics.momentum_panel import MomentumPanel
from gui.dynamics.results_panel import ResultsPanel
from gui.dynamics.plot_panel import PlotPanel

class DynamicsFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Left Panel (Controls)
        self.control_panel = self.create_control_panel()
        splitter.addWidget(self.control_panel)

        # Right Panel (Plot)
        self.plot_panel = PlotPanel()
        splitter.addWidget(self.plot_panel)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

    def create_control_panel(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumWidth(400)
        
        container = QWidget()
        scroll_area.setWidget(container)
        layout = QVBoxLayout(container)

        title = QLabel("Dinámica")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Instantiate Panels
        self.newton_panel = NewtonLawPanel()
        self.energy_panel = EnergyPanel()
        self.momentum_panel = MomentumPanel()
        self.results_panel = ResultsPanel()

        # Clear Button
        self.clear_btn = QPushButton("Limpiar Todo")
        self.clear_btn.setStyleSheet('''QPushButton { background-color: #c0392b; border: none; color: white; padding: 8px 16px; font-size: 12px; font-weight: bold; border-radius: 4px; } QPushButton:hover { background-color: #e74c3c; }''')

        # Add widgets to layout
        layout.addWidget(self.newton_panel)
        layout.addWidget(self.energy_panel)
        layout.addWidget(self.momentum_panel)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.results_panel)
        layout.addStretch()

        return scroll_area

    def connect_signals(self):
        self.newton_panel.calculation_ready.connect(self.results_panel.display_html)
        self.energy_panel.calculation_ready.connect(self.results_panel.display_html)
        self.momentum_panel.calculation_ready.connect(self.results_panel.display_html)
        self.clear_btn.clicked.connect(self.clear_all)
        self.plot_panel.plot_data_requested.connect(self.handle_plot_request)

    @Slot()
    def clear_all(self):
        self.newton_panel.clear()
        self.energy_panel.clear()
        self.momentum_panel.clear()
        self.results_panel.clear()
        self.plot_panel.initialize_plot()

    @Slot(str, str, str)
    def handle_plot_request(self, x_var, y_var, constant_text):
        params, mu, angle = self.newton_panel.get_input_values()
        plot_params = {
            'x_var': x_var,
            'y_var': y_var,
            'constant_value': float(constant_text),
            'mu': mu if self.newton_panel.friction_checkbox.isChecked() else None,
            'angle': angle if self.newton_panel.incline_checkbox.isChecked() else None
        }
        self.plot_panel.plot(plot_params)