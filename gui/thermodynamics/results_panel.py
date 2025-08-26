from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QTextEdit

class ResultsPanel(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Resultados", parent)
        self.setup_ui()

    def setup_ui(self):
        
        layout = QVBoxLayout(self)
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(150)
        
        layout.addWidget(self.results_text)

    def display_results(self, results):
        if not results:
            self.results_text.setText("No hay resultados.")
            return
        
        txt = "Parámetros de entrada:\n"
        for k, v in results['input_params'].items():
            txt += f"  {k}: {v}\n"
        txt += "\nResultado calculado:\n"
        for k, v in results['calculated_values'].items():
            txt += f"  {k}: {v}\n"
        txt += "\nEcuaciones usadas:\n"
        for eq in results['equations']:
            txt += f"  {eq}\n"
        self.results_text.setText(txt)

    def clear_results(self):
        self.results_text.clear()
