from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                                QGroupBox, QLabel, QLineEdit, QPushButton, QRadioButton,
                                QScrollArea)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

class ControlPanel(QWidget):
    calculate_requested = Signal()
    clear_requested = Signal()
    plot_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.input_fields = {}
        self.setup_ui()

    def setup_ui(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumWidth(400)
        
        container = QWidget()
        scroll_area.setWidget(container)
        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        
        layout = QVBoxLayout(container)
        layout.setSpacing(15)
        
        title = QLabel("Cinemática - Movimiento Rectilíneo")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #ecf0f1; padding: 10px 0px; border: none;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        movement_group = self.create_movement_type_section()
        layout.addWidget(movement_group)
        
        params_group = self.create_parameters_section()
        layout.addWidget(params_group)
        
        buttons_layout = self.create_action_buttons()
        layout.addLayout(buttons_layout)
        
        layout.addStretch()

    def create_movement_type_section(self):
        group = QGroupBox("Tipo de Movimiento")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold; font-size: 14px; padding-top: 10px; margin-top: 5px;
                color: #ecf0f1; border: 1px solid #4a627a; border-radius: 5px;
            }
            QGroupBox::title {
                color: #ecf0f1; subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout(group)
        
        self.mru_radio = QRadioButton("Movimiento Rectilíneo Uniforme (MRU)")
        self.mrua_radio = QRadioButton("Movimiento Rectilíneo Uniformemente Acelerado (MRUA)")
        
        radio_style = "QRadioButton { color: #ecf0f1; font-size: 12px; } QRadioButton::indicator { width: 15px; height: 15px; }"
        for radio in [self.mru_radio, self.mrua_radio]:
            radio.setStyleSheet(radio_style)

        self.mru_radio.setChecked(True)
        
        self.mru_radio.toggled.connect(self.on_movement_type_changed)
        self.mrua_radio.toggled.connect(self.on_movement_type_changed)
        
        layout.addWidget(self.mru_radio)
        layout.addWidget(self.mrua_radio)
        
        return group

    def create_parameters_section(self):
        group = QGroupBox("Parámetros")
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
        
        layout = QGridLayout(group)
        layout.setSpacing(8)
        
        params_info = [
            ('x0', 'Posición inicial (m):', True),
            ('v0', 'Velocidad inicial (m/s):', True),
            ('a', 'Aceleración (m/s²):', False),
            ('t', 'Tiempo (s):', True),
            ('x', 'Posición final (m):', False),
            ('v', 'Velocidad final (m/s):', False)
        ]
        
        for i, (var_name, label_text, is_enabled) in enumerate(params_info):
            label = QLabel(label_text)
            line_edit = QLineEdit()
            line_edit.setEnabled(is_enabled)
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
        
        button_style = """
            QPushButton { 
                background-color: #8e44ad; border: none; color: white; padding: 8px 16px; 
                font-size: 12px; font-weight: bold; border-radius: 4px; min-width: 80px; 
            }
            QPushButton:hover { background-color: #9b59b6; }
            QPushButton:pressed { background-color: #7d3c98; }
        """
        
        for btn in [self.calculate_btn, self.clear_btn, self.plot_btn]:
            btn.setStyleSheet(button_style)
        
        self.calculate_btn.clicked.connect(self.calculate_requested)
        self.clear_btn.clicked.connect(self.clear_requested)
        self.plot_btn.clicked.connect(self.plot_requested)
        
        layout.addWidget(self.calculate_btn)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.plot_btn)
        layout.addStretch()
        
        return layout

    def on_movement_type_changed(self):
        is_mru = self.mru_radio.isChecked()
        self.input_fields['a'].setEnabled(not is_mru)
        
        if is_mru:
            self.input_fields['a'].setText('0')
            self.input_fields['a'].setStyleSheet("background-color: #2c3e50; color: #7f8c8d; border: 1px solid #4a627a; border-radius: 4px; padding: 6px;")
        else:
            self.input_fields['a'].setText('')
            self.input_fields['a'].setStyleSheet("""
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

    def get_input_values(self, validator):
        params = {}
        for var_name, field in self.input_fields.items():
            text = field.text().strip()
            if text:
                if not validator.is_valid_number(text):
                    raise ValueError(f"Valor inválido para {var_name}: {text}")
                params[var_name] = float(text)
            else:
                params[var_name] = None
        return params

    def clear_fields(self):
        for field in self.input_fields.values():
            if field.isEnabled():
                field.clear()
        self.on_movement_type_changed()