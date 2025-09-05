"""
Module for the Kinematics Frame of the CPhysics application.

This module defines the main user interface for the kinematics section,
integrating control, results, plotting, and diagram panels.
"""

from PySide6.QtWidgets import (QWidget, QHBoxLayout, QSplitter, QMessageBox, 
                               QScrollArea, QTabWidget)
from PySide6.QtCore import Qt

from modules.kinematics import KinematicsCalculator
from utils.validators import InputValidator
from gui.kinematics.control_panel import ControlPanel
from gui.kinematics.results_panel import ResultsPanel
from gui.kinematics.plot_panel import PlotPanel
from gui.kinematics.diagram_panel import DiagramPanel

class KinematicsFrame(QWidget):
    """
    The main widget for the Kinematics module.

    This class orchestrates the interaction between the user input (ControlPanel),
    the calculation logic (KinematicsCalculator), and the display of results
    (ResultsPanel, PlotPanel, DiagramPanel).
    """
    def __init__(self, parent=None):
        """
        Initializes the KinematicsFrame, its components, and sets up the UI.
        """
        super().__init__(parent)
        
        self.calculator = KinematicsCalculator()
        self.validator = InputValidator()
        self.results = {}
        
        self.setup_ui()
        # Set the initial visibility of controls based on the default movement type.
        self.control_panel.on_movement_type_changed()

    def setup_ui(self):
        """
        Sets up the graphical user interface for the kinematics frame.
        """
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Use a splitter to allow resizing of the control and plot sections.
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        self.control_panel = ControlPanel()
        self.results_panel = ResultsPanel()
        self.plot_panel = PlotPanel()
        self.diagram_panel = DiagramPanel()

        # Group plot and diagram panels into a tabbed view.
        self.plot_tabs = QTabWidget()
        self.plot_tabs.addTab(self.plot_panel, "Motion Graphs")
        self.plot_tabs.addTab(self.diagram_panel, "Vector Diagram")

        # Embed the results panel within the main kinematics control tab.
        kinematics_tab = self.control_panel.tab_widget.widget(0)
        control_panel_layout = kinematics_tab.findChild(QScrollArea).widget().layout()
        control_panel_layout.addWidget(self.results_panel)

        # Embed a separate results panel within the meeting point control tab.
        meeting_tab = self.control_panel.tab_widget.widget(1)
        meeting_panel_layout = meeting_tab.findChild(QScrollArea).widget().layout()
        self.results_panel_meeting = ResultsPanel()
        meeting_panel_layout.addWidget(self.results_panel_meeting)

        splitter.addWidget(self.control_panel)
        splitter.addWidget(self.plot_tabs)
        
        # Set initial size ratio for the splitter sections.
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        # Connect signals from the control panel to the appropriate handler methods.
        self.control_panel.calculate_requested.connect(self.calculate)
        self.control_panel.clear_requested.connect(self.clear_all)
        self.control_panel.plot_requested.connect(self.plot_results)
        self.control_panel.calculate_meeting_requested.connect(self.calculate_meeting)
        self.control_panel.values_changed.connect(self.update_diagram)

    def calculate(self):
        """
        Performs kinematics calculations based on the selected motion type.
        """
        try:
            params = self.control_panel.get_input_values(self.validator)
            
            if self.control_panel.mru_radio.isChecked():
                self.results = self.calculator.calculate_mru(params)
            elif self.control_panel.mrua_radio.isChecked():
                self.results = self.calculator.calculate_mrua(params)
            else:
                self.results = self.calculator.calculate_parabolic_motion(params)
            
            self.results_panel.display_results(self.results)
            
        except ValueError as e:
            QMessageBox.critical(self, "Input Error", f"Invalid input: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Calculation Error", f"An unexpected error occurred: {e}")

    def calculate_meeting(self, params):
        """
        Performs the meeting point calculation.

        Args:
            params (dict): The input parameters for the two objects.
        """
        try:
            self.results = self.calculator.calculate_meeting_point(params)
            self.results_panel_meeting.display_results(self.results)
            self.update_diagram(meeting_data=self.results)
        except ValueError as e:
            QMessageBox.critical(self, "Input Error", f"Invalid input: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Calculation Error", f"An unexpected error occurred during meeting point calculation: {e}")

    def plot_results(self):
        """
        Plots the results of the last successful calculation.
        """
        if not self.results:
            QMessageBox.warning(self, "Warning", "A calculation must be performed before plotting.")
            return
        
        try:
            self.plot_panel.plot_results(self.calculator, self.results)
        except Exception as e:
            QMessageBox.critical(self, "Plotting Error", f"An error occurred while generating the plot: {e}")

    def clear_all(self):
        """
        Clears all input fields, results, and plots in the active tab.
        """
        # Differentiate clearing based on the currently selected tab.
        if self.control_panel.tab_widget.currentIndex() == 0:
            self.control_panel.clear_fields()
            self.results_panel.clear()
        else:
            self.control_panel.meeting_panel.clear_fields()
            self.results_panel_meeting.clear()
            
        self.results = {}
        self.plot_panel.clear_plot()
        self.diagram_panel.clear_diagram()

    def update_diagram(self, values=None, meeting_data=None):
        """
        Updates the vector diagram based on new values or calculation results.

        Args:
            values (dict, optional): A dictionary with velocity and acceleration.
            meeting_data (dict, optional): Results from a meeting point calculation.
        """
        try:
            if meeting_data:
                self.diagram_panel.update_diagram(meeting_data=meeting_data)
            elif values:
                velocity = values.get('velocity')
                acceleration = values.get('acceleration')
                
                vx = float(velocity[0]) if velocity and velocity[0] else 0
                vy = float(velocity[1]) if velocity and velocity[1] else 0
                
                ax = float(acceleration[0]) if acceleration and acceleration[0] else 0
                ay = float(acceleration[1]) if acceleration and acceleration[1] else 0

                self.diagram_panel.update_diagram(velocity=(vx, vy), acceleration=(ax, ay))
        except (ValueError, TypeError):
            # This may occur if input fields are cleared or contain invalid data.
            # Clearing the diagram ensures a clean state.
            self.diagram_panel.clear_diagram()
