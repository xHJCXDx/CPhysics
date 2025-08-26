
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QTextEdit
from PySide6.QtCore import Slot

class ResultsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        results_group = self.create_results_section()
        layout.addWidget(results_group)

    def create_results_section(self):
        """Crear sección de resultados"""
        group = QGroupBox("Resultados")
        
        
        layout = QVBoxLayout(group)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(150)
        
        
        layout.addWidget(self.results_text)
        return group

    @Slot(str)
    def display_html(self, html_content):
        """Muestra contenido HTML en el área de texto de resultados."""
        self.results_text.setHtml(html_content)

    @Slot()
    def clear(self):
        """Limpia el área de texto de resultados."""
        self.results_text.clear()
