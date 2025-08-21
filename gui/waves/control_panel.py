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
        title.setStyleSheet("color: #ecf0f1; padding: 10px 0px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        params_group = self.create_parameters_section()
        layout.addWidget(params_group)

        buttons_layout = self.create_action_buttons()
        layout.addLayout(buttons_layout)

        layout.addStretch()

    def create_parameters_section(self):
        group = QGroupBox("Parámetros de la Onda")
        group.setStyleSheet("""
            QGroupBox { 
                font-weight: bold; font-size: 14px; padding-top: 10px; margin-top: 5px; 
                color: #ecf0f1; border: 1px solid #4a627a; border-radius: 5px;
            }
            QGroupBox::title { 
                color: #ecf0f1; subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px;
            }
            QGroupBox QLabel {
                color: #ecf0f1; font-size: 12px;
            }
        """)
        
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
            line_edit.setStyleSheet("""
                QLineEdit {
                    background-color: #2c3e50;
                    color: #ecf0f1;
                    border: 1px solid #4a627a;
                    border-radius: 4px;
                    padding: 5px;
                }
                QLineEdit:focus {
                    border: 1px solid #8e44ad;
                }""")

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

        button_style = """
            QPushButton { 
                background-color: #8e44ad; border: none; color: white; padding: 8px 16px; 
                font-size: 12px; font-weight: bold; border-radius: 4px; min-width: 80px; 
            }
            QPushButton:hover { background-color: #9b59b6; }
            QPushButton:pressed { background-color: #7d3c98; }
        """
        for btn in [self.calc_button, self.plot_button, self.clear_button]:
            btn.setStyleSheet(button_style)

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
