from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QGroupBox,
                                QLabel, QLineEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Signal, Slot

from modules.dynamics import DynamicsCalculator
from utils.validators import InputValidator

class EnergyPanel(QWidget):
    calculation_ready = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.calculator = DynamicsCalculator()
        self.validator = InputValidator()
        self.input_fields = {}
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        energy_group = self.create_energy_section()
        layout.addWidget(energy_group)

    def create_energy_section(self):
        main_group = QGroupBox("Trabajo y Energía")
        
        main_layout = QVBoxLayout(main_group)

        # Work
        work_group = QGroupBox("Calcular Trabajo (W)")
        work_layout = QGridLayout(work_group)
        work_params = {'work_force': 'Fuerza (N):', 'work_distance': 'Distancia (m):', 'work_angle': 'Ángulo (θ°):'}
        for i, (key, label) in enumerate(work_params.items()):
            work_layout.addWidget(QLabel(label), i, 0)
            line_edit = QLineEdit()
            self.input_fields[key] = line_edit
            work_layout.addWidget(line_edit, i, 1)
        calc_work_btn = QPushButton("Calcular Trabajo")
        calc_work_btn.clicked.connect(self.calculate_work)
        work_layout.addWidget(calc_work_btn, len(work_params), 0, 1, 2)
        main_layout.addWidget(work_group)

        # Kinetic Energy
        ke_group = QGroupBox("Calcular Energía Cinética (KE)")
        ke_layout = QGridLayout(ke_group)
        ke_params = {'ke_mass': 'Masa (kg):', 'ke_velocity': 'Velocidad (m/s):'}
        for i, (key, label) in enumerate(ke_params.items()):
            ke_layout.addWidget(QLabel(label), i, 0)
            line_edit = QLineEdit()
            self.input_fields[key] = line_edit
            ke_layout.addWidget(line_edit, i, 1)
        calc_ke_btn = QPushButton("Calcular Energía Cinética")
        calc_ke_btn.clicked.connect(self.calculate_kinetic_energy)
        ke_layout.addWidget(calc_ke_btn, len(ke_params), 0, 1, 2)
        main_layout.addWidget(ke_group)

        # Potential Energy
        pe_group = QGroupBox("Calcular Energía Potencial (PE)")
        pe_layout = QGridLayout(pe_group)
        pe_params = {'pe_mass': 'Masa (kg):', 'pe_height': 'Altura (m):'}
        for i, (key, label) in enumerate(pe_params.items()):
            pe_layout.addWidget(QLabel(label), i, 0)
            line_edit = QLineEdit()
            self.input_fields[key] = line_edit
            pe_layout.addWidget(line_edit, i, 1)
        calc_pe_btn = QPushButton("Calcular Energía Potencial")
        calc_pe_btn.clicked.connect(self.calculate_potential_energy)
        pe_layout.addWidget(calc_pe_btn, len(pe_params), 0, 1, 2)
        main_layout.addWidget(pe_group)

        return main_group

    def get_input_value(self, key):
        field = self.input_fields.get(key)
        if field and field.text().strip() and self.validator.is_valid_number(field.text().strip()):
            return float(field.text().strip())
        return None

    @Slot()
    def calculate_work(self):
        try:
            force = self.get_input_value('work_force')
            distance = self.get_input_value('work_distance')
            angle = self.get_input_value('work_angle') or 0
            result = self.calculator.calculate_work(force, distance, angle)
            result['title'] = "Trabajo"
            self.calculation_ready.emit(result)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en el cálculo de trabajo:\n{str(e)}")

    @Slot()
    def calculate_kinetic_energy(self):
        try:
            mass = self.get_input_value('ke_mass')
            velocity = self.get_input_value('ke_velocity')
            result = self.calculator.calculate_kinetic_energy(mass, velocity)
            result['title'] = "Energía Cinética"
            self.calculation_ready.emit(result)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en el cálculo de energía cinética:\n{str(e)}")

    @Slot()
    def calculate_potential_energy(self):
        try:
            mass = self.get_input_value('pe_mass')
            height = self.get_input_value('pe_height')
            result = self.calculator.calculate_potential_energy(mass, height)
            result['title'] = "Energía Potencial"
            self.calculation_ready.emit(result)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en el cálculo de energía potencial:\n{str(e)}")

    @Slot()
    def clear(self):
        for field in self.input_fields.values():
            field.clear()