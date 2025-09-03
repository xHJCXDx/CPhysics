from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                                QGroupBox, QLabel, QLineEdit, QPushButton, QRadioButton,
                                QScrollArea, QTabWidget)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
import numpy as np

from gui.kinematics.meeting_panel import MeetingPanel

class ControlPanel(QWidget):
    calculate_requested = Signal()
    clear_requested = Signal()
    plot_requested = Signal()
    calculate_meeting_requested = Signal(dict)
    values_changed = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.input_fields = {}
        self.param_widgets = {}
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Cinemática")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        self.tab_widget = QTabWidget()
        

        # Tab for standard kinematics
        kinematics_tab = QWidget()
        self.setup_kinematics_tab(kinematics_tab)
        self.tab_widget.addTab(kinematics_tab, "Movimiento")

        # Tab for meeting point calculation
        meeting_tab = QWidget()
        self.setup_meeting_tab(meeting_tab)
        self.tab_widget.addTab(meeting_tab, "Encuentros")

        main_layout.addWidget(self.tab_widget)

    def setup_kinematics_tab(self, tab):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumWidth(400)
        
        container = QWidget()
        scroll_area.setWidget(container)
        
        tab_layout = QVBoxLayout(tab)
        tab_layout.addWidget(scroll_area)
        
        layout = QVBoxLayout(container)
        layout.setSpacing(15)
        
        movement_group = self.create_movement_type_section()
        layout.addWidget(movement_group)
        
        params_group = self.create_parameters_section()
        layout.addWidget(params_group)
        
        buttons_layout = self.create_action_buttons()
        layout.addLayout(buttons_layout)
        
        layout.addStretch()

    def setup_meeting_tab(self, tab):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumWidth(400)

        self.meeting_panel = MeetingPanel()
        scroll_area.setWidget(self.meeting_panel)

        tab_layout = QVBoxLayout(tab)
        tab_layout.addWidget(scroll_area)
        self.meeting_panel.calculate_requested.connect(self.calculate_meeting_requested)

    def create_movement_type_section(self):
        group = QGroupBox("Tipo de Movimiento")
        
        
        layout = QVBoxLayout(group)
        
        self.mru_radio = QRadioButton("Movimiento Rectilíneo Uniforme (MRU)")
        self.mrua_radio = QRadioButton("Movimiento Rectilíneo Uniformemente Acelerado (MRUA)")
        self.parabolic_radio = QRadioButton("Movimiento Parabólico")
        
        

        self.mru_radio.setChecked(True)
        
        self.mru_radio.toggled.connect(self.on_movement_type_changed)
        self.mrua_radio.toggled.connect(self.on_movement_type_changed)
        self.parabolic_radio.toggled.connect(self.on_movement_type_changed)
        
        layout.addWidget(self.mru_radio)
        layout.addWidget(self.mrua_radio)
        layout.addWidget(self.parabolic_radio)
        
        return group

    def create_parameters_section(self):
        group = QGroupBox("Parámetros")
        
        
        self.params_layout = QGridLayout(group)
        self.params_layout.setSpacing(8)
        
        params_info = [
            ('x0', 'Posición inicial (m):', True),
            ('y0', 'Altura inicial (m):', False),
            ('v0', 'Velocidad inicial (m/s):', True),
            ('a', 'Aceleración (m/s²):', False),
            ('t', 'Tiempo (s):', True),
            ('x', 'Posición final (m):', False),
            ('v', 'Velocidad final (m/s):', False),
            ('angle', 'Ángulo de lanzamiento (°):', False)
        ]
        
        for i, (var_name, label_text, is_enabled) in enumerate(params_info):
            label = QLabel(label_text)
            line_edit = QLineEdit()
            line_edit.setEnabled(is_enabled)
            line_edit.textChanged.connect(self._on_values_changed)
            
            
            self.input_fields[var_name] = line_edit
            self.param_widgets[var_name] = (label, line_edit)
            
            self.params_layout.addWidget(label, i, 0)
            self.params_layout.addWidget(line_edit, i, 1)
        
        return group

    def create_action_buttons(self):
        layout = QHBoxLayout()
        layout.setSpacing(10)
        
        self.calculate_btn = QPushButton("Calcular")
        self.clear_btn = QPushButton("Limpiar")
        self.plot_btn = QPushButton("Graficar")
        
        
        
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
        is_mrua = self.mrua_radio.isChecked()
        is_parabolic = self.parabolic_radio.isChecked()

        # Ocultar todos los parámetros primero
        for var_name in self.param_widgets:
            label, line_edit = self.param_widgets[var_name]
            label.setVisible(False)
            line_edit.setVisible(False)

        if is_mru or is_mrua:
            # Mostrar parámetros para MRU/MRUA
            params_to_show = ['x0', 'v0', 'a', 't', 'x', 'v']
            for var_name in params_to_show:
                label, line_edit = self.param_widgets[var_name]
                label.setVisible(True)
                line_edit.setVisible(True)
            
            self.input_fields['a'].setEnabled(is_mrua)
            if is_mru:
                self.input_fields['a'].setText('0')
                
            else:
                self.input_fields['a'].setText('')
                

        # Hide all parameters first
        for var_name in self.param_widgets:
            label, line_edit = self.param_widgets[var_name]
            label.setVisible(False)
            line_edit.setVisible(False)

        if is_mru or is_mrua:
            # Show parameters for MRU/MRUA
            params_to_show = ['x0', 'v0', 'a', 't', 'x', 'v']
            for var_name in params_to_show:
                label, line_edit = self.param_widgets[var_name]
                label.setVisible(True)
                line_edit.setVisible(True)
            
            self.input_fields['a'].setEnabled(is_mrua)
            if is_mru:
                self.input_fields['a'].setText('0')
                
            else:
                self.input_fields['a'].setText('')
                

        elif is_parabolic:
            # Show parameters for Parabolic Movement
            params_to_show = ['v0', 'angle', 'x0', 'y0']
            for var_name in params_to_show:
                label, line_edit = self.param_widgets[var_name]
                label.setVisible(True)
                line_edit.setVisible(True)
                line_edit.setEnabled(True)
        
        self._on_values_changed()

    def get_input_values(self, validator):
        params = {}
        for var_name, field in self.input_fields.items():
            if field.isVisible():
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
        if hasattr(self, 'meeting_panel'):
            self.meeting_panel.clear_fields()

    def _on_values_changed(self):
        try:
            if self.mru_radio.isChecked():
                v0 = float(self.input_fields['v0'].text() or 0)
                velocity = (v0, 0)
                acceleration = (0, 0)
            elif self.mrua_radio.isChecked():
                v0 = float(self.input_fields['v0'].text() or 0)
                a = float(self.input_fields['a'].text() or 0)
                velocity = (v0, 0)
                acceleration = (a, 0)
            elif self.parabolic_radio.isChecked():
                v0 = float(self.input_fields['v0'].text() or 0)
                angle = float(self.input_fields['angle'].text() or 0)
                angle_rad = np.deg2rad(angle)
                vx = v0 * np.cos(angle_rad)
                vy = v0 * np.sin(angle_rad)
                velocity = (vx, vy)
                acceleration = (0, -9.81) # Gravity
            else:
                velocity = (0, 0)
                acceleration = (0, 0)

            self.values_changed.emit({'velocity': velocity, 'acceleration': acceleration})
        except (ValueError, TypeError):
            self.values_changed.emit({'velocity': (0,0), 'acceleration': (0,0)})
