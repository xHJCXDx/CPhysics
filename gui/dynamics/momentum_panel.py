from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QGroupBox, 
                                QLabel, QLineEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Signal, Slot

from modules.dynamics import DynamicsCalculator
from utils.validators import InputValidator

class MomentumPanel(QWidget):
    calculation_ready = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.calculator = DynamicsCalculator()
        self.validator = InputValidator()
        self.input_fields = {}
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        momentum_group = self.create_momentum_section()
        layout.addWidget(momentum_group)

    def create_momentum_section(self):
        main_group = QGroupBox("Impulso y Momento Lineal")
        
        main_layout = QVBoxLayout(main_group)

        # Impulse
        impulse_group = QGroupBox("Calcular Impulso (I)")
        impulse_layout = QGridLayout(impulse_group)
        impulse_params = {'impulse_force': 'Fuerza (N):', 'impulse_time': 'Tiempo (s):', 'impulse_impulse': 'Impulso (N·s):'}
        for i, (key, label) in enumerate(impulse_params.items()):
            impulse_layout.addWidget(QLabel(label), i, 0)
            line_edit = QLineEdit()
            line_edit.setPlaceholderText("Dejar en blanco para calcular")
            self.input_fields[key] = line_edit
            impulse_layout.addWidget(line_edit, i, 1)
        calc_impulse_btn = QPushButton("Calcular Impulso")
        calc_impulse_btn.clicked.connect(self.calculate_impulse)
        impulse_layout.addWidget(calc_impulse_btn, len(impulse_params), 0, 1, 2)
        main_layout.addWidget(impulse_group)

        # Linear Momentum
        momentum_group = QGroupBox("Calcular Momento Lineal (p)")
        momentum_layout = QGridLayout(momentum_group)
        momentum_params = {'momentum_mass': 'Masa (kg):', 'momentum_velocity': 'Velocidad (m/s):', 'momentum_momentum': 'Momento (kg·m/s):'}
        for i, (key, label) in enumerate(momentum_params.items()):
            momentum_layout.addWidget(QLabel(label), i, 0)
            line_edit = QLineEdit()
            line_edit.setPlaceholderText("Dejar en blanco para calcular")
            self.input_fields[key] = line_edit
            momentum_layout.addWidget(line_edit, i, 1)
        calc_momentum_btn = QPushButton("Calcular Momento Lineal")
        calc_momentum_btn.clicked.connect(self.calculate_linear_momentum)
        momentum_layout.addWidget(calc_momentum_btn, len(momentum_params), 0, 1, 2)
        main_layout.addWidget(momentum_group)

        return main_group

    def get_input_value(self, key):
        field = self.input_fields.get(key)
        if field and field.text().strip() and self.validator.is_valid_number(field.text().strip()):
            return float(field.text().strip())
        return None

    @Slot()
    def calculate_impulse(self):
        try:
            force = self.get_input_value('impulse_force')
            time = self.get_input_value('impulse_time')
            impulse = self.get_input_value('impulse_impulse')
            result = self.calculator.calculate_impulse(force, time, impulse)
            if 'impulse' in result:
                self.input_fields['impulse_impulse'].setText(f"{result['impulse']:.4f}")
                html = self.format_result_to_html("Impulso", result['impulse'], result['equation'], {'Fuerza': force, 'Tiempo': time, 'Impulso': None})
            elif 'force' in result:
                self.input_fields['impulse_force'].setText(f"{result['force']:.4f}")
                html = self.format_result_to_html("Fuerza (Impulso)", result['force'], result['equation'], {'Fuerza': None, 'Tiempo': time, 'Impulso': impulse})
            elif 'time' in result:
                self.input_fields['impulse_time'].setText(f"{result['time']:.4f}")
                html = self.format_result_to_html("Tiempo (Impulso)", result['time'], result['equation'], {'Fuerza': force, 'Tiempo': None, 'Impulso': impulse})
            self.calculation_ready.emit(html)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en el cálculo de impulso:\n{str(e)}")

    @Slot()
    def calculate_linear_momentum(self):
        try:
            mass = self.get_input_value('momentum_mass')
            velocity = self.get_input_value('momentum_velocity')
            momentum = self.get_input_value('momentum_momentum')
            result = self.calculator.calculate_linear_momentum(mass, velocity, momentum)
            if 'momentum' in result:
                self.input_fields['momentum_momentum'].setText(f"{result['momentum']:.4f}")
                html = self.format_result_to_html("Momento Lineal", result['momentum'], result['equation'], {'Masa': mass, 'Velocidad': velocity, 'Momento': None})
            elif 'mass' in result:
                self.input_fields['momentum_mass'].setText(f"{result['mass']:.4f}")
                html = self.format_result_to_html("Masa (Momento)", result['mass'], result['equation'], {'Masa': None, 'Velocidad': velocity, 'Momento': momentum})
            elif 'velocity' in result:
                self.input_fields['momentum_velocity'].setText(f"{result['velocity']:.4f}")
                html = self.format_result_to_html("Velocidad (Momento)", result['velocity'], result['equation'], {'Masa': mass, 'Velocidad': None, 'Momento': momentum})
            self.calculation_ready.emit(html)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en el cálculo de momento lineal:\n{str(e)}")

    def format_result_to_html(self, title, value, equation, params):
        parts = [f"<b style='font-size:13px;'>RESULTADO - {title.upper()}</b><br>", "=" * 50 + "<br><br>"]
        parts.append("<b>Parámetros:</b><br>")
        for name, val in params.items():
            if val is not None: parts.append(f"&nbsp;&nbsp;• {name}: {val}<br>")
        parts.append(f"<br><b>Ecuación:</b><br>&nbsp;&nbsp;• {equation}<br>")
        unit_map = {"Impulso": "N·s", "Momento": "kg·m/s", "Fuerza": "N", "Tiempo": "s", "Masa": "kg", "Velocidad": "m/s"}
        unit = next((u for k, u in unit_map.items() if k in title), "")
        parts.append(f"<br><b>Resultado:</b><br>&nbsp;&nbsp;• <span style='color:#2ecc71;'>{title}</span>: {value:.4f} {unit}<br>")
        return "".join(parts)

    @Slot()
    def clear(self):
        for field in self.input_fields.values():
            field.clear()
