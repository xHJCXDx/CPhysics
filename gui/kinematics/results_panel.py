from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QTextEdit
from PySide6.QtGui import QFont

class ResultsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        group = QGroupBox("Resultados")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold; font-size: 14px; padding-top: 10px; margin-top: 5px; color: #ecf0f1; 
                border: 1px solid #4a627a; border-radius: 5px;
            }
            QGroupBox::title {
                color: #ecf0f1; subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px;
            }
        """)
        
        group_layout = QVBoxLayout(group)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(200)
        self.results_text.setStyleSheet("""
            QTextEdit { 
                background-color: #2c3e50; border: 1px solid #4a627a; border-radius: 4px; 
                padding: 8px; font-family: 'Consolas', 'Monaco', monospace; font-size: 12px; color: #ecf0f1; 
            }
        """)
        
        group_layout.addWidget(self.results_text)
        layout.addWidget(group)

    def display_results(self, results):
        if not results:
            self.results_text.clear()
            return

        movement_type = results.get('movement_type')
        text = "<b style='font-size:13px;'>RESULTADOS DEL CÁLCULO</b><br>"
        text += "=" * 50 + "<br><br>"

        if movement_type == 'meeting_point':
            self.display_meeting_point_results(results, text)
        else:
            self.display_standard_results(results, text)

    def display_standard_results(self, results, text):
        text += "<b>Parámetros utilizados:</b><br>"
        text += "-" * 25 + "<br>"
        param_map = {
            'x0': 'Posición inicial (m)', 'y0': 'Altura inicial (m)', 'v0': 'Velocidad inicial (m/s)', 
            'a': 'Aceleración (m/s²)', 't': 'Tiempo (s)', 
            'x': 'Posición final (m)', 'v': 'Velocidad final (m/s)',
            'angle': 'Ángulo de lanzamiento (°)',
            'time_of_flight': 'Tiempo de vuelo (s)',
            'max_height': 'Altura máxima (m)',
            'range': 'Alcance (m)',
            'v0x': 'Velocidad inicial en x (m/s)',
            'v0y': 'Velocidad inicial en y (m/s)'
        }
        for key, value in results.get('input_params', {}).items():
            if value is not None:
                text += f"&nbsp;&nbsp;• {param_map.get(key, key)}: {value}<br>"
        
        text += "<br><b>Resultados calculados:</b><br>"
        text += "-" * 25 + "<br>"
        for key, value in results.get('calculated_values', {}).items():
            text += f"&nbsp;&nbsp;• <span style='color:#3498db;'>{param_map.get(key, key)}</span>: {value:.4f}<br>"
        
        if 'equations' in results:
            text += "<br><b style='color:#9b59b6;'>Ecuaciones utilizadas:</b><br>"
            text += "-" * 25 + "<br>"
            for eq in results['equations']:
                text += f"&nbsp;&nbsp;• {eq}<br>"
        
        self.results_text.setHtml(text)

    def display_meeting_point_results(self, results, text):
        text += "<b>Parámetros utilizados:</b><br>"
        text += "-" * 25 + "<br>"
        param_map = {
            'x0': 'Posición inicial (m)', 'v0': 'Velocidad inicial (m/s)', 
            'a': 'Aceleración (m/s²)'
        }
        for obj_name, params in results.get('input_params', {}).items():
            text += f"<b>{obj_name}:</b><br>"
            for key, value in params.items():
                text += f"&nbsp;&nbsp;• {param_map.get(key, key)}: {value}<br>"
        
        text += "<br><b>Resultados calculados:</b><br>"
        text += "-" * 25 + "<br>"
        calculated_map = {
            'tiempo_encuentro': 'Tiempo de encuentro (s)',
            'posicion_encuentro': 'Posición de encuentro (m)'
        }
        for key, value in results.get('calculated_values', {}).items():
            text += f"&nbsp;&nbsp;• <span style='color:#3498db;'>{calculated_map.get(key, key)}</span>: {value:.4f}<br>"

        if 'equations' in results:
            text += "<br><b style='color:#9b59b6;'>Ecuaciones utilizadas:</b><br>"
            text += "-" * 25 + "<br>"
            for eq in results['equations']:
                text += f"&nbsp;&nbsp;• {eq}<br>"

        self.results_text.setHtml(text)

    def clear(self):
        self.results_text.clear()