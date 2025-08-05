import numpy as np
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSplitter, QTextEdit, QFormLayout, QMessageBox, QGroupBox,
    QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QDoubleValidator

from modules.waves import WavesCalculator
from utils.validators import InputValidator

# Integración de Matplotlib con PySide6 (Qt6)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    """Widget de lienzo de Matplotlib personalizado para PySide6."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        self.setParent(parent)
        
        # Estilo oscuro para el gráfico
        fig.patch.set_facecolor('#34495e')
        self.axes.set_facecolor('#2c3e50')
        self.axes.tick_params(axis='x', colors='#ecf0f1')
        self.axes.tick_params(axis='y', colors='#ecf0f1')
        for spine in self.axes.spines.values():
            spine.set_edgecolor('#ecf0f1')

class WavesFrame(QWidget):
    """
    Un widget para cálculos y visualizaciones de física de ondas.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.calculator = WavesCalculator()
        self.validator = InputValidator()
        self.results = {}
        self.inputs = {}
        self.setup_ui()

    def setup_ui(self):
        """Inicializa y organiza los componentes de la interfaz de usuario."""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        control_panel = self.create_control_panel()
        splitter.addWidget(control_panel)

        plot_panel = self.create_plot_panel()
        splitter.addWidget(plot_panel)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

    def create_control_panel(self):
        """Crea el panel de control izquierdo con entradas y resultados."""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumWidth(400)

        container = QWidget()
        scroll_area.setWidget(container)

        layout = QVBoxLayout(container)
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

        results_group = self.create_results_section()
        layout.addWidget(results_group)

        layout.addStretch()
        return scroll_area

    def create_parameters_section(self):
        """Crea la sección de parámetros de entrada."""
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
        """Crea los botones de acción."""
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

        self.calc_button.clicked.connect(self.calculate_and_display)
        self.plot_button.clicked.connect(self.plot_wave)
        self.clear_button.clicked.connect(self.clear_all)

        layout.addWidget(self.calc_button)
        layout.addWidget(self.plot_button)
        layout.addWidget(self.clear_button)
        layout.addStretch()
        return layout

    def create_results_section(self):
        """Crea la sección de visualización de resultados."""
        group = QGroupBox("Resultados")
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
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setMinimumHeight(200)
        self.results_display.setStyleSheet("""
            QTextEdit { 
                background-color: #2c3e50; border: 1px solid #4a627a; border-radius: 4px; 
                padding: 8px; font-family: 'Consolas', 'Monaco', monospace; font-size: 12px; color: #ecf0f1; 
            }
        """)
        layout.addWidget(self.results_display)
        return group

    def create_plot_panel(self):
        """Crea el panel derecho para el gráfico."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)

        title = QLabel("Gráfico de la Onda")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: #ecf0f1; padding: 5px 0px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        toolbar = NavigationToolbar(self.canvas, container)

        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        return container

    def get_input_values(self):
        """Recupera y convierte los valores de entrada de QLineEdits a flotantes."""
        values = {}
        for name, widget in self.inputs.items():
            text = widget.text().strip().replace(',', '.')
            if text:
                if not self.validator.is_valid_number(text):
                    raise ValueError(f"Valor inválido para {name}: '{text}'")
                values[name] = float(text)
            else:
                values[name] = None
        return values

    def calculate_and_display(self):
        """Calcula propiedades y actualiza el panel de resultados."""
        try:
            params = self.get_input_values()
            self.results = self.calculator.calculate_wave_properties(params)
            self.display_results()
        except ValueError as e:
            QMessageBox.warning(self, "Datos Insuficientes", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error de Cálculo", f"Ocurrió un error: {e}")

    def display_results(self):
        """Muestra los resultados en la interfaz."""
        if not self.results:
            return

        # Rellenar campos de entrada con valores calculados
        for key, value in self.results['calculated_values'].items():
            if key in self.inputs:
                self.inputs[key].setText(f"{value:.4f}")

        # Formatear texto de resultados
        text = "<b>Parámetros Calculados:</b><br>"
        if not self.results['calculated_values']:
            text += "No se pudo calcular ningún valor. Se necesitan más datos.<br>"
        else:
            for key, value in self.results['calculated_values'].items():
                text += f"&nbsp;&nbsp;• {key.replace('_', ' ').capitalize()}: {value:.4f}<br>"

        text += "<br><b>Ecuaciones Utilizadas:</b><br>"
        if not self.results['equations']:
            text += "Ninguna ecuación fue necesaria.<br>"
        else:
            for eq in self.results['equations']:
                text += f"&nbsp;&nbsp;• {eq}<br>"

        # Ecuación de la onda
        vals = self.results.get('all_values', {}) # type: ignore
        A = vals.get('amplitude')
        k = vals.get('wave_number')
        omega = vals.get('angular_frequency')
        phi = vals.get('phase', 0)

        text += "<br><b style='color:#9b59b6;'>Ecuación de la Onda y(x,t):</b><br>"
        if all(v is not None for v in [A, k, omega]):
            phi_str = f" + {phi:.2f}" if phi != 0 else ""
            text += f"&nbsp;&nbsp;• y(x,t) = {A:.2f} cos({k:.2f}x - {omega:.2f}t{phi_str})"
        else:
            text += "Datos insuficientes para generar la ecuación completa."

        self.results_display.setHtml(text)

    def plot_wave(self):
        """Genera un gráfico de la onda en un instante t=0."""
        if not self.results or 'all_values' not in self.results:
            self.calculate_and_display()
            if not self.results or 'all_values' not in self.results:
                QMessageBox.warning(self, "Advertencia", "Primero debe realizar un cálculo.")
                return

        vals = self.results['all_values']
        A = vals.get('amplitude')
        wavelength = vals.get('wavelength')
        k = vals.get('wave_number')
        phi = vals.get('phase', 0)

        if not all(v is not None for v in [A, wavelength, k]):
            QMessageBox.warning(self, "Datos Insuficientes",
                                "Se necesita Amplitud y Longitud de onda para graficar.")
            return

        try:
            self.canvas.axes.clear()

            # Graficar dos longitudes de onda para una buena visualización
            x = np.linspace(0, 2 * wavelength, 500)
            y = A * np.cos(k * x + phi)  # Ecuación y(x, t=0) = A cos(kx + φ)

            self.canvas.axes.plot(x, y, color='#3498db', linewidth=2.5, label=f'Onda en t=0')
            self.canvas.axes.set_xlabel('Posición (x) [m]', fontsize=12, color='#ecf0f1')
            self.canvas.axes.set_ylabel('Amplitud (y) [m]', fontsize=12, color='#ecf0f1')
            self.canvas.axes.set_title('Perfil de la Onda (y vs x)', fontsize=14, fontweight='bold', color='#ecf0f1')
            self.canvas.axes.grid(True, color='#4a627a', linestyle='--', linewidth=0.5)
            self.canvas.axes.axhline(0, color='#7f8c8d', linewidth=0.8)
            
            legend = self.canvas.axes.legend(fontsize=11)
            legend.get_frame().set_facecolor('#34495e')
            legend.get_frame().set_edgecolor('#4a627a')
            for text in legend.get_texts():
                text.set_color('#ecf0f1')

            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error de Gráfico", f"Ocurrió un error al graficar: {e}")

    def clear_all(self):
        """Limpia todos los campos de entrada, resultados y el gráfico."""
        for field in self.inputs.values():
            field.clear()
        self.inputs['phase'].setText("0")

        self.results = {}
        self.results_display.clear()

        self.canvas.axes.clear()
        self.canvas.axes.set_title("Gráfico de la Onda", color='#ecf0f1')
        self.canvas.axes.grid(True, color='#4a627a', linestyle='--', linewidth=0.5)
        self.canvas.draw()