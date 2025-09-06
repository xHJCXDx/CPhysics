"""
Momentum Panel for the Dynamics module.

This module defines the UI for calculating impulse and linear momentum.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QGroupBox, 
                                QLabel, QLineEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Signal, Slot

from modules.dynamics import DynamicsCalculator
from utils.validators import InputValidator

class MomentumPanel(QWidget):
    """
    A panel for calculating impulse and linear momentum.

    Emits 'calculation_ready' signal upon successful calculation.
    """
    calculation_ready = Signal(dict)

    def __init__(self, parent=None):
        """Initializes the MomentumPanel."""
        super().__init__(parent)
        self.calculator = DynamicsCalculator()
        self.validator = InputValidator()
        self.input_fields = {}
        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface for the momentum panel."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        momentum_group = self.create_momentum_section()
        layout.addWidget(momentum_group)

    def create_momentum_section(self):
        """Creates the group boxes and input fields for momentum calculations."""
        main_group = QGroupBox("Impulse and Linear Momentum")
        main_layout = QVBoxLayout(main_group)

        # Impulse calculation section
        impulse_group = QGroupBox("Calculate Impulse (I)")
        impulse_layout = QGridLayout(impulse_group)
        impulse_params = {'impulse_force': 'Force (N):', 'impulse_time': 'Time (s):', 'impulse_impulse': 'Impulse (N·s):'}
        for i, (key, label) in enumerate(impulse_params.items()):
            impulse_layout.addWidget(QLabel(label), i, 0)
            line_edit = QLineEdit()
            line_edit.setPlaceholderText("Leave blank to calculate")
            self.input_fields[key] = line_edit
            impulse_layout.addWidget(line_edit, i, 1)
        calc_impulse_btn = QPushButton("Calculate Impulse")
        calc_impulse_btn.clicked.connect(self.calculate_impulse)
        impulse_layout.addWidget(calc_impulse_btn, len(impulse_params), 0, 1, 2)
        main_layout.addWidget(impulse_group)

        # Linear Momentum calculation section
        momentum_group = QGroupBox("Calculate Linear Momentum (p)")
        momentum_layout = QGridLayout(momentum_group)
        momentum_params = {'momentum_mass': 'Mass (kg):', 'momentum_velocity': 'Velocity (m/s):', 'momentum_momentum': 'Momentum (kg·m/s):'}
        for i, (key, label) in enumerate(momentum_params.items()):
            momentum_layout.addWidget(QLabel(label), i, 0)
            line_edit = QLineEdit()
            line_edit.setPlaceholderText("Leave blank to calculate")
            self.input_fields[key] = line_edit
            momentum_layout.addWidget(line_edit, i, 1)
        calc_momentum_btn = QPushButton("Calculate Linear Momentum")
        calc_momentum_btn.clicked.connect(self.calculate_linear_momentum)
        momentum_layout.addWidget(calc_momentum_btn, len(momentum_params), 0, 1, 2)
        main_layout.addWidget(momentum_group)

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
    def calculate_impulse(self):
        """Calculates impulse and emits the result."""
        try:
            force = self.get_input_value('impulse_force')
            time = self.get_input_value('impulse_time')
            impulse = self.get_input_value('impulse_impulse')
            result = self.calculator.calculate_impulse(force, time, impulse)
            result['title'] = "Impulse"
            self.calculation_ready.emit(result)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error in impulse calculation:\n{str(e)}")

    @Slot()
    def calculate_linear_momentum(self):
        """Calculates linear momentum and emits the result."""
        try:
            mass = self.get_input_value('momentum_mass')
            velocity = self.get_input_value('momentum_velocity')
            momentum = self.get_input_value('momentum_momentum')
            result = self.calculator.calculate_linear_momentum(mass, velocity, momentum)
            result['title'] = "Linear Momentum"
            self.calculation_ready.emit(result)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error in linear momentum calculation:\n{str(e)}")

    @Slot()
    def clear(self):
        """Clears all input fields in the panel."""
        for field in self.input_fields.values():
            field.clear()