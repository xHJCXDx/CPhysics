"""
Panel de resultados para el módulo de electromagnetismo.
"""

from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QTextEdit

class ResultsPanel(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Resultados", parent)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QGroupBox { 
                font-weight: bold; font-size: 14px; padding-top: 10px; margin-top: 5px; 
                color: #ecf0f1; border: 1px solid #4a627a; border-radius: 5px;
            }
            QGroupBox::title { 
                color: #ecf0f1; subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px; 
            }
        """)
        
        layout = QVBoxLayout(self)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(150)
        self.results_text.setStyleSheet("""
            QTextEdit { 
                background-color: #2c3e50; border: 1px solid #4a627a; border-radius: 4px; 
                padding: 8px; font-family: 'Consolas', 'Monaco', monospace; font-size: 12px; color: #ecf0f1; 
            }
        """)
        
        layout.addWidget(self.results_text)

    def display_results(self, results, input_fields):
        if not results: return

        calculated_values = results.get('calculated_values', {})
        if calculated_values:
            calculated_var, calculated_val = list(calculated_values.items())[0]
            input_fields[calculated_var].setText(f"{calculated_val:.4e}")

        text = "<b style='font-size:13px;'>RESULTADOS DEL CÁLCULO</b><br>"
        text += "=" * 50 + "<br><br>"

        text += "<b>Parámetros utilizados:</b><br>"
        text += "-" * 25 + "<br>"
        param_map = {'q1': 'Carga 1 (C)', 'q2': 'Carga 2 (C)', 'r': 'Distancia (m)', 'F': 'Fuerza (N)'}
        for key, value in results.get('input_params', {}).items():
            if value is not None:
                text += f"&nbsp;&nbsp;• {param_map.get(key, key)}: {value:.4e}<br>"

        text += "<br><b>Resultado calculado:</b><br>"
        text += "-" * 25 + "<br>"
        for key, value in calculated_values.items():
            text += f"&nbsp;&nbsp;• <span style='color:#3498db;'>{param_map.get(key, key)}</span>: {value:.4e}<br>"

        text += "<br><b style='color:#9b59b6;'>Ecuación utilizada:</b><br>"
        text += "-" * 25 + "<br>"
        text += f"&nbsp;&nbsp;• {results['equations'][0]}<br>"
        self.results_text.setHtml(text)

    def clear_results(self):
        self.results_text.clear()
