
import numpy as np
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGroupBox, QLabel, QLineEdit, QPushButton, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class ControlPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.input_fields = {}
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Termodinámica - Ley de Gases Ideales")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        params_group = self.create_parameters_section()
        layout.addWidget(params_group)

        buttons_layout = self.create_action_buttons()
        layout.addLayout(buttons_layout)

        layout.addStretch()

    def create_parameters_section(self):
        group = QGroupBox("Parámetros (deje uno en blanco para calcular)")
        
        layout = QGridLayout(group)
        layout.setSpacing(8)

        params_info = [
            ('P', 'Presión (atm):'),
            ('V', 'Volumen (L):'),
            ('n', 'Moles (mol):'),
            ('T', 'Temperatura (K):'),
        ]
        for i, (var_name, label_text) in enumerate(params_info):
            label = QLabel(label_text)
            line_edit = QLineEdit()
            line_edit.setPlaceholderText("Valor conocido")
            
            self.input_fields[var_name] = line_edit
            layout.addWidget(label, i, 0)
            layout.addWidget(line_edit, i, 1)
        return group

    def create_action_buttons(self):
        layout = QHBoxLayout()
        layout.setSpacing(10)
        self.calculate_btn = QPushButton("Calcular")
        self.clear_btn = QPushButton("Limpiar")
        self.plot_btn = QPushButton("Graficar")
        
        
        layout.addWidget(self.calculate_btn)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.plot_btn)
        layout.addStretch()
        return layout

    def get_input_values(self):
        params = {}
        for var_name, field in self.input_fields.items():
            text = field.text().strip()
            params[var_name] = float(text) if text else None
        return params

    def clear_fields(self):
        for field in self.input_fields.values():
            field.clear()
