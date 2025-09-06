"""
Energy Panel for the Dynamics module.

This module defines the UI for calculating work, kinetic energy, and potential energy.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QGroupBox,
                                QLabel, QLineEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Signal, Slot

from modules.dynamics import DynamicsCalculator
from utils.validators import InputValidator

class EnergyPanel(QWidget):
    """
    A panel for calculating work, kinetic energy, and potential energy.

    Emits 'calculation_ready' signal upon successful calculation.
    """
    calculation_ready = Signal(dict)

    def __init__(self, parent=None):
        """Initializes the EnergyPanel."""
        super().__init__(parent)
        self.calculator = DynamicsCalculator()
        self.validator = InputValidator()
        self.input_fields = {}
        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface for the energy panel."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        energy_group = self.create_energy_section()
        layout.addWidget(energy_group)

    def create_energy_section(self):
        """Creates the group boxes and input fields for energy calculations."""
        main_group = QGroupBox("Work and Energy")
        main_layout = QVBoxLayout(main_group)

        # Work calculation section
        work_group = QGroupBox("Calculate Work (W)")
        work_layout = QGridLayout(work_group)
        work_params = {'work_force': 'Force (N):', 'work_distance': 'Distance (m):', 'work_angle': 'Angle (θ°):'}
        for i, (key, label) in enumerate(work_params.items()):
            work_layout.addWidget(QLabel(label), i, 0)
            line_edit = QLineEdit()
            self.input_fields[key] = line_edit
            work_layout.addWidget(line_edit, i, 1)
        calc_work_btn = QPushButton("Calculate Work")
        calc_work_btn.clicked.connect(self.calculate_work)
        work_layout.addWidget(calc_work_btn, len(work_params), 0, 1, 2)
        main_layout.addWidget(work_group)

        # Kinetic Energy calculation section
        ke_group = QGroupBox("Calculate Kinetic Energy (KE)")
        ke_layout = QGridLayout(ke_group)
        ke_params = {'ke_mass': 'Mass (kg):', 'ke_velocity': 'Velocity (m/s):'}
        for i, (key, label) in enumerate(ke_params.items()):
            ke_layout.addWidget(QLabel(label), i, 0)
            line_edit = QLineEdit()
            self.input_fields[key] = line_edit
            ke_layout.addWidget(line_edit, i, 1)
        calc_ke_btn = QPushButton("Calculate Kinetic Energy")
        calc_ke_btn.clicked.connect(self.calculate_kinetic_energy)
        ke_layout.addWidget(calc_ke_btn, len(ke_params), 0, 1, 2)
        main_layout.addWidget(ke_group)

        # Potential Energy calculation section
        pe_group = QGroupBox("Calculate Potential Energy (PE)")
        pe_layout = QGridLayout(pe_group)
        pe_params = {'pe_mass': 'Mass (kg):', 'pe_height': 'Height (m):'}
        for i, (key, label) in enumerate(pe_params.items()):
            pe_layout.addWidget(QLabel(label), i, 0)
            line_edit = QLineEdit()
            self.input_fields[key] = line_edit
            pe_layout.addWidget(line_edit, i, 1)
        calc_pe_btn = QPushButton("Calculate Potential Energy")
        calc_pe_btn.clicked.connect(self.calculate_potential_energy)
        pe_layout.addWidget(calc_pe_btn, len(pe_params), 0, 1, 2)
        main_layout.addWidget(pe_group)

        return main_group

    def get_input_value(self, key):
        """
        Retrieves and validates the numeric value from a QLineEdit.

        Args:
            key (str): The key corresponding to the QLineEdit in self.input_fields.

        Returns:
            float or None: The float value if valid, otherwise None.
        """
        field = self.input_fields.get(key)
        if field and field.text().strip() and self.validator.is_valid_number(field.text().strip()):
            return float(field.text().strip())
        return None

    @Slot()
    def calculate_work(self):
        """Calculates work and emits the result."""
        try:
            force = self.get_input_value('work_force')
            distance = self.get_input_value('work_distance')
            angle = self.get_input_value('work_angle') or 0
            result = self.calculator.calculate_work(force, distance, angle)
            result['title'] = "Work"
            self.calculation_ready.emit(result)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error in work calculation:\n{str(e)}")

    @Slot()
    def calculate_kinetic_energy(self):
        """Calculates kinetic energy and emits the result."""
        try:
            mass = self.get_input_value('ke_mass')
            velocity = self.get_input_value('ke_velocity')
            result = self.calculator.calculate_kinetic_energy(mass, velocity)
            result['title'] = "Kinetic Energy"
            self.calculation_ready.emit(result)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error in kinetic energy calculation:\n{str(e)}")

    @Slot()
    def calculate_potential_energy(self):
        """Calculates potential energy and emits the result."""
        try:
            mass = self.get_input_value('pe_mass')
            height = self.get_input_value('pe_height')
            result = self.calculator.calculate_potential_energy(mass, height)
            result['title'] = "Potential Energy"
            self.calculation_ready.emit(result)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error in potential energy calculation:\n{str(e)}")

    @Slot()
    def clear(self):
        """Clears all input fields in the panel."""
        for field in self.input_fields.values():
            field.clear()