"""
Waves Frame for the CPhysics application.

This module defines the main UI for the waves section,
integrating the control, results, and plotting panels.
"""

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QSplitter, QMessageBox, QVBoxLayout, QScrollArea
)
from PySide6.QtCore import Qt

from modules.waves import WavesCalculator
from gui.waves.control_panel import ControlPanel
from gui.waves.results_panel import ResultsPanel
from gui.waves.plot_panel import PlotPanel

class WavesFrame(QWidget):
    """
    Main widget for the Waves module.

    Orchestrates the interaction between user input (ControlPanel),
    calculation logic (WavesCalculator), and display of results
    (ResultsPanel, PlotPanel).
    """
    def __init__(self, parent=None):
        """Initializes the WavesFrame and sets up the UI."""
        super().__init__(parent)
        self.calculator = WavesCalculator()
        self.results = {}
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        """Sets up the graphical user interface for the waves frame."""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # --- Left Panel (Controls and Results) ---
        left_panel_container = QWidget()
        left_layout = QVBoxLayout(left_panel_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(15)

        self.control_panel = ControlPanel()
        self.results_panel = ResultsPanel()

        left_layout.addWidget(self.control_panel)
        left_layout.addWidget(self.results_panel)
        left_layout.addStretch()

        # Wrap the left panel in a scroll area for responsiveness.
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(left_panel_container)
        scroll_area.setMinimumWidth(400)

        splitter.addWidget(scroll_area)

        # --- Right Panel (Plot) ---
        self.plot_panel = PlotPanel()
        splitter.addWidget(self.plot_panel)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

    def connect_signals(self):
        """Connects signals from the control panel to the appropriate slots."""
        self.control_panel.calc_button.clicked.connect(self.calculate_and_display)
        self.control_panel.plot_button.clicked.connect(self.plot)
        self.control_panel.clear_button.clicked.connect(self.clear_all)

    def calculate_and_display(self):
        """ 
        Performs wave properties calculation, updates the results panel,
        and fills empty input fields with newly calculated values.
        """
        try:
            params = self.control_panel.get_input_values()
            self.results = self.calculator.calculate_wave_properties(params)
            self.results_panel.display_results(self.results)
            self.update_inputs_with_results()
        except ValueError as e:
            QMessageBox.warning(self, "Input Error", f"Invalid input: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Calculation Error", f"An unexpected error occurred: {e}")

    def update_inputs_with_results(self):
        """Fills empty input fields with values from the calculation results."""
        if 'calculated_values' in self.results:
            for key, value in self.results['calculated_values'].items():
                if key in self.control_panel.inputs and not self.control_panel.inputs[key].text():
                    self.control_panel.inputs[key].setText(f"{value:.4f}")

    def plot(self):
        """Initiates the plotting of the wave profile."""
        # Ensure that there are results to plot.
        if not self.results or 'all_values' not in self.results:
            # Attempt to calculate first if no results are present.
            self.calculate_and_display()
            # If still no results, abort plotting.
            if not self.results or 'all_values' not in self.results:
                QMessageBox.warning(self, "Cannot Plot", "Calculation must be performed successfully before plotting.")
                return

        try:
            self.plot_panel.plot_wave_profile(self.results)
        except ValueError as e:
            QMessageBox.warning(self, "Insufficient Data", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Plotting Error", f"An error occurred while plotting: {e}")

    def clear_all(self):
        """Clears all input fields, results, and the plot."""
        self.control_panel.clear()
        self.results_panel.clear()
        self.plot_panel.clear_plot()
        self.results = {}