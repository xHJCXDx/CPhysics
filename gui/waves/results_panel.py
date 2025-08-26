from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QTextEdit

class ResultsPanel(QWidget):
    """Panel para mostrar los resultados de los cálculos."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        group = QGroupBox("Resultados")
        
        group_layout = QVBoxLayout(group)
        
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setMinimumHeight(200)
        
        group_layout.addWidget(self.results_display)
        layout.addWidget(group)

    def display_results(self, results):
        if not results:
            return

        text = "<b>Parámetros Calculados:</b><br>"
        if not results['calculated_values']:
            text += "No se pudo calcular ningún valor. Se necesitan más datos.<br>"
        else:
            for key, value in results['calculated_values'].items():
                text += f"&nbsp;&nbsp;• {key.replace('_', ' ').capitalize()}: {value:.4f}<br>"

        text += "<br><b>Ecuaciones Utilizadas:</b><br>"
        if not results['equations']:
            text += "Ninguna ecuación fue necesaria.<br>"
        else:
            for eq in results['equations']:
                text += f"&nbsp;&nbsp;• {eq}<br>"

        vals = results.get('all_values', {}) # type: ignore
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

    def clear(self):
        self.results_display.clear()
