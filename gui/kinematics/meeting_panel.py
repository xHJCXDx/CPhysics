from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont

class MeetingPanel(QWidget):
    calculate_requested = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.object1_fields = {}
        self.object2_fields = {}
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Cálculo de Encuentros")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: #ecf0f1; padding: 10px 0px; border: none;")
        layout.addWidget(title)

        object1_group = self.create_object_group("Objeto 1", self.object1_fields)
        layout.addWidget(object1_group)

        object2_group = self.create_object_group("Objeto 2", self.object2_fields)
        layout.addWidget(object2_group)

        self.calculate_btn = QPushButton("Calcular Encuentro")
        self.calculate_btn.setStyleSheet("""
            QPushButton { 
                background-color: #8e44ad; border: none; color: white; padding: 8px 16px; 
                font-size: 12px; font-weight: bold; border-radius: 4px; min-width: 80px; 
            }
            QPushButton:hover { background-color: #9b59b6; }
            QPushButton:pressed { background-color: #7d3c98; }
        """)
        self.calculate_btn.clicked.connect(self.on_calculate)
        layout.addWidget(self.calculate_btn)

        layout.addStretch()

    def create_object_group(self, title, fields_dict):
        group = QGroupBox(title)
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold; font-size: 12px; padding-top: 10px; margin-top: 5px;
                color: #ecf0f1; border: 1px solid #4a627a; border-radius: 5px;
            }
            QGroupBox::title {
                color: #ecf0f1; subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px;
            }
            QGroupBox QLabel {
                color: #ecf0f1; font-size: 12px;
            }
        """)
        
        layout = QGridLayout(group)
        layout.setSpacing(8)

        params_info = [
            ('x0', 'Posición inicial (m):'),
            ('v0', 'Velocidad inicial (m/s):'),
            ('a', 'Aceleración (m/s²):')
        ]

        for i, (var_name, label_text) in enumerate(params_info):
            label = QLabel(label_text)
            line_edit = QLineEdit()
            line_edit.setStyleSheet("""
                QLineEdit {
                    background-color: #2c3e50;
                    color: #ecf0f1;
                    border: 1px solid #4a627a;
                    border-radius: 4px;
                    padding: 6px;
                }
                QLineEdit:focus {
                    border: 1px solid #8e44ad;
                }
            """)
            
            fields_dict[var_name] = line_edit
            layout.addWidget(label, i, 0)
            layout.addWidget(line_edit, i, 1)
            
        return group

    def on_calculate(self):
        try:
            params = {
                'obj1': self.get_input_values(self.object1_fields),
                'obj2': self.get_input_values(self.object2_fields)
            }
            self.calculate_requested.emit(params)
        except ValueError as e:
            QMessageBox.critical(self, "Error de validación", str(e))

    def get_input_values(self, fields):
        obj_params = {}
        for var_name, field in fields.items():
            text = field.text().strip()
            if not text:
                raise ValueError(f"El campo '{var_name}' no puede estar vacío.")
            try:
                obj_params[var_name] = float(text)
            except ValueError:
                raise ValueError(f"Valor inválido para {var_name}: {text}")
        return obj_params

    def clear_fields(self):
        for field in self.object1_fields.values():
            field.clear()
        for field in self.object2_fields.values():
            field.clear()
