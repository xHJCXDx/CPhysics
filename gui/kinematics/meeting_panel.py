from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont

class MeetingPanel(QWidget):
    """Panel for input and calculation of meeting point between two objects."""
    calculate_requested = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.object1_fields = {}
        self.object2_fields = {}
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Meeting Point Calculation")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)

        object1_group = self.create_object_group("Object 1", self.object1_fields)
        layout.addWidget(object1_group)

        object2_group = self.create_object_group("Object 2", self.object2_fields)
        layout.addWidget(object2_group)

        self.calculate_btn = QPushButton("Calculate Meeting")
        self.calculate_btn.clicked.connect(self.on_calculate)
        layout.addWidget(self.calculate_btn)
        layout.addStretch()

    def create_object_group(self, title, fields_dict):
        group = QGroupBox(title)
        layout = QGridLayout(group)
        layout.setSpacing(8)

        params_info = [
            ('x0', 'Initial position (m):'),
            ('v0', 'Initial velocity (m/s):'),
            ('a', 'Acceleration (m/s²):')
        ]
        for i, (var_name, label_text) in enumerate(params_info):
            label = QLabel(label_text)
            line_edit = QLineEdit()
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
            QMessageBox.critical(self, "Validation Error", str(e))

    def get_input_values(self, fields):
        obj_params = {}
        for var_name, field in fields.items():
            text = field.text().strip()
            if not text:
                raise ValueError(f"Field '{var_name}' cannot be empty.")
            try:
                obj_params[var_name] = float(text)
            except ValueError:
                raise ValueError(f"Invalid value for {var_name}: {text}")
        return obj_params

    def clear_fields(self):
        for field in self.object1_fields.values():
            field.clear()
        for field in self.object2_fields.values():
            field.clear()
