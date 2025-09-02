"""
Control panel for the electromagnetism module.
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
        """Set up the user interface"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        
                # Module title
        title = QLabel("Electromagnetism - Coulomb's Law")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Parameters section
        params_group = self.create_parameters_section()
        main_layout.addWidget(params_group)
        
        # Action buttons
        buttons_layout = self.create_action_buttons()
        main_layout.addLayout(buttons_layout)
        
        main_layout.addStretch()

    def create_parameters_section(self):
        """Create parameters section"""
        group = QGroupBox("Parameters (leave one blank to calculate)")
        
        
        layout = QGridLayout(group)
        layout.setSpacing(8)
        
        params_info = [
            ('q1', 'Charge 1 (C):'),
            ('q2', 'Charge 2 (C):'),
            ('r', 'Distance (m):'),
            ('F', 'Force (N):'),
        ]
        
        for i, (var_name, label_text) in enumerate(params_info):
            label = QLabel(label_text)
            line_edit = QLineEdit()
            line_edit.setPlaceholderText("Known value")
            
            self.input_fields[var_name] = line_edit
            layout.addWidget(label, i, 0)
            layout.addWidget(line_edit, i, 1)
        
        return group

    def create_action_buttons(self):
        """Create action buttons"""
        layout = QHBoxLayout()
        layout.setSpacing(10)
        
        self.calculate_btn = QPushButton("Calculate")
        self.clear_btn = QPushButton("Clear")
        self.plot_btn = QPushButton("Plot")
        
        
        
        layout.addWidget(self.calculate_btn)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.plot_btn)
        layout.addStretch()
        
        return layout

    def get_input_values(self, validator):
        """Get input values from the form"""
        params = {}
        for var_name, field in self.input_fields.items():
            text = field.text().strip()
            params[var_name] = float(text) if text and validator.is_valid_number(text) else None
        return params

    def clear_fields(self):
        """Clear all input fields"""
        for field in self.input_fields.values():
            field.clear()