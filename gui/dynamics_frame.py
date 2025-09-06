"""Main frame for the Dynamics module."""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSplitter, 
                                QScrollArea, QLabel, QPushButton, QMessageBox)
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont

from gui.dynamics.newton_law_panel import NewtonLawPanel
from gui.dynamics.energy_panel import EnergyPanel
from gui.dynamics.momentum_panel import MomentumPanel
from gui.dynamics.results_panel import ResultsPanel
from gui.dynamics.plot_panel import PlotPanel

class DynamicsFrame(QWidget):
    """Main widget for the Dynamics module. Integrates input, results, and plot panels."""
    def __init__(self, parent=None):
        """Initialize UI and signal connections."""
        super().__init__(parent)
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        """Set up the graphical user interface."""
        main_layout = QHBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Left panel for user inputs and controls.
        self.control_panel = self.create_control_panel()
        splitter.addWidget(self.control_panel)

        # Right panel for displaying plots.
        self.plot_panel = PlotPanel()
        splitter.addWidget(self.plot_panel)

        # Adjust the initial size ratio of the splitter sections.
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

    def create_control_panel(self):
        """Create left panel with control widgets."""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumWidth(400)
        
        container = QWidget()
        scroll_area.setWidget(container)
        layout = QVBoxLayout(container)

        title = QLabel("Dynamics")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.newton_panel = NewtonLawPanel()
        self.energy_panel = EnergyPanel()
        self.momentum_panel = MomentumPanel()
        self.results_panel = ResultsPanel()
        self.clear_btn = QPushButton("Clear All")
        
        layout.addWidget(self.newton_panel)
        layout.addWidget(self.energy_panel)
        layout.addWidget(self.momentum_panel)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.results_panel)
        layout.addStretch()

        return scroll_area

    def connect_signals(self):
        """Connect signals from child widgets to slots."""
        # Route calculation-ready signals to the results display panel.
        self.newton_panel.calculation_ready.connect(self.results_panel.display_results)
        self.energy_panel.calculation_ready.connect(self.results_panel.display_results)
        self.momentum_panel.calculation_ready.connect(self.results_panel.display_results)
        
        # Connect the master clear button to the clear_all slot.
        self.clear_btn.clicked.connect(self.clear_all)
        
        # Handle plot requests from the plot panel.
        self.plot_panel.plot_data_requested.connect(self.handle_plot_request)

    @Slot()
    def clear_all(self):
        """Clear all input fields and results."""
        self.newton_panel.clear()
        self.energy_panel.clear()
        self.momentum_panel.clear()
        self.results_panel.clear()
        self.plot_panel.initialize_plot()

    @Slot(str, str, str)
    def handle_plot_request(self, x_var, y_var, constant_text):
        """
        Handles the request to plot data from the Newton's Law panel.

        Args:
            x_var (str): The variable for the x-axis.
            y_var (str): The variable for the y-axis.
            constant_text (str): The value of the constant variable as a string.
        """
        try:
            params, mu, angle = self.newton_panel.get_input_values()
            plot_params = {
                'x_var': x_var,
                'y_var': y_var,
                'constant_value': float(constant_text),
                'mu': mu if self.newton_panel.friction_checkbox.isChecked() else None,
                'angle': angle if self.newton_panel.incline_checkbox.isChecked() else None
            }
            self.plot_panel.plot(plot_params)
        except ValueError:
            QMessageBox.critical(self, "Input Error", f"Invalid constant value: '{constant_text}'. Please enter a valid number.")
        except Exception as e:
            QMessageBox.critical(self, "Plotting Error", f"An unexpected error occurred while preparing the plot: {e}")