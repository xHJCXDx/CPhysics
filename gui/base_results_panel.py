from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
import re

class BaseResultsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.variable_tooltips = self.get_variable_tooltips()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        group = QGroupBox("Resultados")
        group_layout = QVBoxLayout(group)
        
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Parámetro", "Valor"])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        group_layout.addWidget(self.results_table)
        layout.addWidget(group)

    def display_results(self, results):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def get_variable_tooltips(self):
        # This method can be overridden by subclasses to provide specific tooltips
        return {
            'x': 'Posición final (m)', 'x0': 'Posición inicial (m)',
            'y': 'Altura final (m)', 'y0': 'Altura inicial (m)',
            'v': 'Velocidad final (m/s)', 'v0': 'Velocidad inicial (m/s)',
            'a': 'Aceleración (m/s²)', 't': 'Tiempo (s)',
            'g': 'Aceleración debida a la gravedad (9.8 m/s²)',
            'v0x': 'Velocidad inicial en x (m/s)',
            'v0y': 'Velocidad inicial en y (m/s)',
            'vx': 'Velocidad en x (m/s)', 'vy': 'Velocidad en y (m/s)',
            'θ': 'Ángulo de lanzamiento (°)',
            't_vuelo': 'Tiempo de vuelo (s)',
            'y_max': 'Altura máxima (m)',
            'R': 'Alcance horizontal (m)'
        }

    def get_equation_tooltip(self, equation):
        tooltip_parts = []
        variables = set(re.findall(r'\b([a-zA-Z_]+[0-9]*)\b', equation))
        for var in variables:
            if var in self.variable_tooltips:
                tooltip_parts.append(f"{var}: {self.variable_tooltips[var]}")
        return "\n".join(tooltip_parts) if tooltip_parts else "Información de variables no disponible"

    def clear(self):
        self.results_table.setRowCount(0)

    def add_row(self, row, param, value, tooltip=None):
        item_param = QTableWidgetItem(param)
        item_value = QTableWidgetItem(value)
        if tooltip:
            item_value.setToolTip(tooltip)
        self.results_table.setItem(row, 0, item_param)
        self.results_table.setItem(row, 1, item_value)
