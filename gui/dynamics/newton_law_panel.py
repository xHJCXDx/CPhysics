from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QGroupBox, 
                                QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout)
from PySide6.QtCore import Signal, Slot

from modules.dynamics import DynamicsCalculator
from utils.validators import InputValidator

class NewtonLawPanel(QWidget):
    calculation_ready = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.calculator = DynamicsCalculator()
        self.validator = InputValidator()
        self.input_fields = {}
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 0, 0, 0)

        params_group = self.create_parameters_section()
        layout.addWidget(params_group)
        
        incline_group = self.create_incline_section()
        layout.addWidget(incline_group)
        
        friction_group = self.create_friction_section()
        layout.addWidget(friction_group)
        
        buttons_layout = self.create_action_buttons()
        layout.addLayout(buttons_layout)

    def create_parameters_section(self):
        group = QGroupBox("Parameters (leave one blank to calculate)")
        
        layout = QGridLayout(group)
        params_info = [('f', 'Applied Force (N):'), ('m', 'Mass (kg):'), ('a', 'Acceleration (m/s²):')]
        for i, (var, label) in enumerate(params_info):
            line_edit = QLineEdit()
            line_edit.setPlaceholderText("Known value")
            
            self.input_fields[var] = line_edit
            layout.addWidget(QLabel(label), i, 0)
            layout.addWidget(line_edit, i, 1)
        return group

    def create_friction_section(self):
        group = QGroupBox("Friction (Optional)")
        group.setCheckable(True)
        group.setChecked(False)
        layout = QGridLayout(group)
        self.mu_input = QLineEdit()
        self.mu_input.setPlaceholderText("ex. 0.2")
        layout.addWidget(QLabel("Friction Coefficient (μ):"), 0, 0)
        layout.addWidget(self.mu_input, 0, 1)
        self.friction_checkbox = group
        group.toggled.connect(self.mu_input.setEnabled)
        self.mu_input.setEnabled(False)
        return group

    def create_incline_section(self):
        group = QGroupBox("Inclined Plane (Optional)")
        group.setCheckable(True)
        group.setChecked(False)
        layout = QGridLayout(group)
        self.angle_input = QLineEdit()
        self.angle_input.setPlaceholderText("ex. 30")
        
        layout.addWidget(QLabel("Plane Angle (θ°):"), 0, 0)
        layout.addWidget(self.angle_input, 0, 1)
        self.incline_checkbox = group
        group.toggled.connect(self.angle_input.setEnabled)
        self.angle_input.setEnabled(False)
        return group

    def create_action_buttons(self):
        layout = QHBoxLayout()
        self.calculate_btn = QPushButton("Calculate Newton's Law")
        self.calculate_btn.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_btn)
        layout.addStretch()
        return layout

    def get_input_values(self):
        params = {var: float(field.text().strip()) if field.text().strip() and self.validator.is_valid_number(field.text().strip()) else None for var, field in self.input_fields.items()}
        mu = float(self.mu_input.text().strip()) if self.friction_checkbox.isChecked() and self.mu_input.text().strip() and self.validator.is_valid_number(self.mu_input.text().strip()) else None
        angle = float(self.angle_input.text().strip()) if self.incline_checkbox.isChecked() and self.angle_input.text().strip() and self.validator.is_valid_number(self.angle_input.text().strip()) else None
        if mu is not None and mu < 0:
            QMessageBox.warning(self, "Invalid Value", "The friction coefficient cannot be negative.")
            mu = None
        if angle is not None and not (0 <= angle <= 90):
            QMessageBox.warning(self, "Invalid Value", "The angle must be between 0 and 90 degrees.")
            angle = None
        return params, mu, angle

    @Slot()
    def calculate(self):
        try:
            params, mu, angle = self.get_input_values()
            results = self.calculator.calculate_newton_second_law(params, mu=mu, angle=angle)
            
            calculated_values = results.get('calculated_values', {})
            if calculated_values:
                calc_var, calc_val = list(calculated_values.items())[0]
                self.input_fields[calc_var].setText(f"{calc_val:.4f}")

            self.calculation_ready.emit(results)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error in calculation:\n{str(e)}")

    @Slot()
    def clear(self):
        for field in self.input_fields.values(): field.clear()
        self.mu_input.clear()
        self.friction_checkbox.setChecked(False)
        self.angle_input.clear()
        self.incline_checkbox.setChecked(False)