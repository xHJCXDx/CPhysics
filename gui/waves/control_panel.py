from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QGroupBox, QFormLayout, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QDoubleValidator

class ControlPanel(QWidget):
    """Panel de control con entradas y botones de acción."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Ondas - Movimiento Ondulatorio")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        params_group = self.create_parameters_section()
        layout.addWidget(params_group)

        buttons_layout = self.create_action_buttons()
        layout.addLayout(buttons_layout)

        layout.addStretch()

    def create_parameters_section(self):
        group = QGroupBox("Parámetros de la Onda")
        
        
        form_layout = QFormLayout(group)
        form_layout.setSpacing(8)
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.inputs = {
            "amplitude": QLineEdit(),
            "frequency": QLineEdit(),
            "wavelength": QLineEdit(),
            "velocity": QLineEdit(),
            "phase": QLineEdit("0"),
        }

        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        for line_edit in self.inputs.values():
            line_edit.setValidator(validator)
            line_edit.setPlaceholderText("Valor conocido")
            

        form_layout.addRow("Amplitud (A) [m]:", self.inputs["amplitude"])
        form_layout.addRow("Frecuencia (f) [Hz]:", self.inputs["frequency"])
        form_layout.addRow("Longitud de onda (λ) [m]:", self.inputs["wavelength"])
        form_layout.addRow("Velocidad (v) [m/s]:", self.inputs["velocity"])
        form_layout.addRow("Fase inicial (φ) [rad]:", self.inputs["phase"])
        
        return group

    def create_action_buttons(self):
        layout = QHBoxLayout()
        layout.setSpacing(10)

        self.calc_button = QPushButton("Calcular")
        self.plot_button = QPushButton("Graficar")
        self.clear_button = QPushButton("Limpiar")

        

        layout.addWidget(self.calc_button)
        layout.addWidget(self.plot_button)
        layout.addWidget(self.clear_button)
        layout.addStretch()
        return layout

    def get_input_values(self):
        values = {}
        for name, widget in self.inputs.items():
            text = widget.text().strip().replace(',', '.')
            if text:
                values[name] = float(text)
            else:
                values[name] = None
        return values

    def clear(self):
        for field in self.inputs.values():
            field.clear()
        self.inputs['phase'].setText("0")
