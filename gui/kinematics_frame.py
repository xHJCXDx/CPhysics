"""
Interfaz gráfica para el módulo de cinemática
Permite calcular y visualizar problemas de movimiento
"""

from PySide6.QtWidgets import (QWidget, QHBoxLayout, QSplitter, QMessageBox, QScrollArea, QTabWidget)
from PySide6.QtCore import Qt

from modules.kinematics import KinematicsCalculator
from utils.validators import InputValidator

from gui.kinematics.control_panel import ControlPanel
from gui.kinematics.results_panel import ResultsPanel
from gui.kinematics.plot_panel import PlotPanel

class KinematicsFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.calculator = KinematicsCalculator()
        self.validator = InputValidator()
        self.results = {}
        
        self.setup_ui()
        self.control_panel.on_movement_type_changed()

    # Configuración de la interfaz gráfica
    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        self.control_panel = ControlPanel()
        self.results_panel = ResultsPanel()
        self.plot_panel = PlotPanel()

        # Add results panel to control panel's layout
        kinematics_tab = self.control_panel.tab_widget.widget(0)
        control_panel_layout = kinematics_tab.findChild(QScrollArea).widget().layout()
        control_panel_layout.addWidget(self.results_panel)

        splitter.addWidget(self.control_panel)
        splitter.addWidget(self.plot_panel)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        self.control_panel.calculate_requested.connect(self.calculate)
        self.control_panel.clear_requested.connect(self.clear_all)
        self.control_panel.plot_requested.connect(self.plot_results)
        self.control_panel.calculate_meeting_requested.connect(self.calculate_meeting)

    def calculate(self):
        try:
            params = self.control_panel.get_input_values(self.validator)
            
            if self.control_panel.mru_radio.isChecked():
                self.results = self.calculator.calculate_mru(params)
            elif self.control_panel.mrua_radio.isChecked():
                self.results = self.calculator.calculate_mrua(params)
            else:
                self.results = self.calculator.calculate_parabolic_motion(params)
            
            self.results_panel.display_results(self.results)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en el cálculo:\n{str(e)}")

    def calculate_meeting(self, params):
        try:
            self.results = self.calculator.calculate_meeting_point(params)
            self.results_panel.display_results(self.results)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en el cálculo de encuentro:\n{str(e)}")

    def plot_results(self):
        if not self.results:
            QMessageBox.warning(self, "Advertencia", "Primero debe realizar un cálculo")
            return
        
        try:
            self.plot_panel.plot_results(self.calculator, self.results)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar gráfico:\n{str(e)}")

    def clear_all(self):
        if self.control_panel.tab_widget.currentIndex() == 0:
            self.control_panel.clear_fields()
        else:
            self.control_panel.meeting_panel.clear_fields()
        self.results = {}
        self.results_panel.clear()
        self.plot_panel.clear_plot()
