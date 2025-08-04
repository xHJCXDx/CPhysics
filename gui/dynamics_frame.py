"""
Interfaz gráfica para el módulo de dinámica
Permite calcular problemas de la Segunda Ley de Newton
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                                QGroupBox, QLabel, QLineEdit, QPushButton,
                                QTextEdit, QScrollArea, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from modules.dynamics import DynamicsCalculator
from utils.validators import InputValidator

class DynamicsFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Inicializar calculadora y validador
        self.calculator = DynamicsCalculator()
        self.validator = InputValidator()
        
        # Variables para almacenar resultados
        self.results = {}
        self.input_fields = {}
        
        # Configurar la interfaz
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Panel de controles
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel)
    
    def create_control_panel(self):
        """Crear panel de controles y resultados"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        container = QWidget()
        scroll_area.setWidget(container)
        
        layout = QVBoxLayout(container)
        layout.setSpacing(15)
        
        # Título del módulo
        title = QLabel("Dinámica - Segunda Ley de Newton")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; padding: 10px 0px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Sección de parámetros
        params_group = self.create_parameters_section()
        layout.addWidget(params_group)
        
        # Botones de acción
        buttons_layout = self.create_action_buttons()
        layout.addLayout(buttons_layout)
        
        # Sección de resultados
        results_group = self.create_results_section()
        layout.addWidget(results_group)
        
        layout.addStretch()
        
        return scroll_area
    
    def create_parameters_section(self):
        """Crear sección de parámetros"""
        group = QGroupBox("Parámetros (deje uno en blanco para calcular)")
        group.setStyleSheet("""
            QGroupBox { font-weight: bold; font-size: 14px; padding-top: 10px; margin-top: 5px; }
            QGroupBox::title { color: #34495e; subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px; }
        """)
        
        layout = QGridLayout(group)
        layout.setSpacing(8)
        
        params_info = [
            ('f', 'Fuerza (N):'),
            ('m', 'Masa (kg):'),
            ('a', 'Aceleración (m/s²):'),
        ]
        
        for i, (var_name, label_text) in enumerate(params_info):
            label = QLabel(label_text)
            line_edit = QLineEdit()
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
        
        button_style = """
            QPushButton { background-color: #3498db; border: none; color: white; padding: 8px 16px; font-size: 12px; font-weight: bold; border-radius: 4px; min-width: 80px; }
            QPushButton:hover { background-color: #2980b9; }
            QPushButton:pressed { background-color: #21618c; }
        """
        
        for btn in [self.calculate_btn, self.clear_btn]:
            btn.setStyleSheet(button_style)
        
        self.calculate_btn.clicked.connect(self.calculate)
        self.clear_btn.clicked.connect(self.clear_all)
        
        layout.addWidget(self.calculate_btn)
        layout.addWidget(self.clear_btn)
        layout.addStretch()
        
        return layout
    
    def create_results_section(self):
        """Crear sección de resultados"""
        group = QGroupBox("Resultados")
        group.setStyleSheet("""
            QGroupBox { font-weight: bold; font-size: 14px; padding-top: 10px; margin-top: 5px; }
            QGroupBox::title { color: #34495e; subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px; }
        """)
        
        layout = QVBoxLayout(group)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(150)
        self.results_text.setStyleSheet("""
            QTextEdit { background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 4px; padding: 8px; font-family: 'Consolas', 'Monaco', monospace; font-size: 11px; color: #2c3e50; }
        """)
        
        layout.addWidget(self.results_text)
        return group
        
    def get_input_values(self):
        """Obtener valores de entrada del formulario"""
        params = {}
        for var_name, field in self.input_fields.items():
            text = field.text().strip()
            params[var_name] = float(text) if text and self.validator.is_valid_number(text) else None
        return params

    def calculate(self):
        """Realizar cálculos de la Segunda Ley de Newton"""
        try:
            params = self.get_input_values()
            self.results = self.calculator.calculate_newton_second_law(params)
            self.display_results()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en el cálculo:\n{str(e)}")

    def display_results(self):
        """Mostrar resultados en el área de texto y en el campo de entrada correspondiente"""
        if not self.results: return

        # Rellenar el campo de entrada calculado
        calculated_values = self.results.get('calculated_values', {})
        if calculated_values:
            calculated_var, calculated_val = list(calculated_values.items())[0]
            self.input_fields[calculated_var].setText(f"{calculated_val:.4f}")

        # Formatear el texto de resultados de manera detallada
        text = "RESULTADOS DEL CÁLCULO\n"
        text += "=" * 50 + "\n\n"

        # Mostrar parámetros utilizados
        text += "Parámetros utilizados:\n"
        text += "-" * 25 + "\n"
        param_map = {'f': 'Fuerza (N)', 'm': 'Masa (kg)', 'a': 'Aceleración (m/s²)'}
        for key, value in self.results.get('input_params', {}).items():
            if value is not None:
                text += f"  {param_map.get(key, key)}: {value}\n"

        text += "\nResultado calculado:\n"
        text += "-" * 25 + "\n"
        for key, value in calculated_values.items():
            text += f"  {param_map.get(key, key)}: {value:.4f}\n"

        # Mostrar ecuaciones utilizadas
        text += "\nEcuación utilizada:\n"
        text += "-" * 25 + "\n"
        text += f"  • {self.results['equations'][0]}\n"
        self.results_text.setPlainText(text)

    def clear_all(self):
        """Limpiar todos los campos y resultados"""
        for field in self.input_fields.values():
            field.clear()
        self.results = {}
        self.results_text.clear()