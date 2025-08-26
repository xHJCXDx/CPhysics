"""
Panel de control para el módulo de electromagnetismo.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                                QGroupBox, QLabel, QLineEdit, QPushButton, QScrollArea)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class ControlPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.input_fields = {}
        self.setup_ui()

    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        
        # Título del módulo
        title = QLabel("Electromagnetismo - Ley de Coulomb")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Sección de parámetros
        params_group = self.create_parameters_section()
        main_layout.addWidget(params_group)
        
        # Botones de acción
        buttons_layout = self.create_action_buttons()
        main_layout.addLayout(buttons_layout)
        
        main_layout.addStretch()

    def create_parameters_section(self):
        """Crear sección de parámetros"""
        group = QGroupBox("Parámetros (deje uno en blanco para calcular)")
        
        
        layout = QGridLayout(group)
        layout.setSpacing(8)
        
        params_info = [
            ('q1', 'Carga 1 (C):'),
            ('q2', 'Carga 2 (C):'),
            ('r', 'Distancia (m):'),
            ('F', 'Fuerza (N):'),
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
        """Crear botones de acción"""
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

    def get_input_values(self, validator):
        """Obtener valores de entrada del formulario"""
        params = {}
        for var_name, field in self.input_fields.items():
            text = field.text().strip()
            params[var_name] = float(text) if text and validator.is_valid_number(text) else None
        return params

    def clear_fields(self):
        """Limpiar todos los campos de entrada"""
        for field in self.input_fields.values():
            field.clear()
