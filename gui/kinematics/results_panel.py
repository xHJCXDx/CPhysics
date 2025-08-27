from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt

class ResultsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.variable_tooltips = {
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
        self.clear()
        if not results:
            return

        movement_type = results.get('movement_type')
        if movement_type == 'meeting_point':
            self.display_meeting_point_results(results)
        else:
            self.display_standard_results(results)

    def display_standard_results(self, results):
        self.results_table.setRowCount(0)
        
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

        # Input parameters
        input_params = results.get('input_params', {})
        self.results_table.setRowCount(len(input_params) + len(results.get('calculated_values', {})) + len(results.get('equations', [])))
        
        row = 0
        for key, value in input_params.items():
            if value is not None:
                self.results_table.setItem(row, 0, QTableWidgetItem(f"Parámetro: {param_map.get(key, key)}"))
                self.results_table.setItem(row, 1, QTableWidgetItem(str(value)))
                row += 1

        # Calculated values
        calculated_values = results.get('calculated_values', {})
        for key, value in calculated_values.items():
            item_param = QTableWidgetItem(f"Calculado: {param_map.get(key, key)}")
            item_value = QTableWidgetItem(f"{value:.4f}")
            self.results_table.setItem(row, 0, item_param)
            self.results_table.setItem(row, 1, item_value)
            row += 1
            
        # Equations
        if 'equations' in results:
            for eq in results['equations']:
                item_eq = QTableWidgetItem("Ecuación")
                item_formula = QTableWidgetItem(eq)
                
                tooltip = self.get_equation_tooltip(eq)
                item_formula.setToolTip(tooltip)
                
                self.results_table.setItem(row, 0, item_eq)
                self.results_table.setItem(row, 1, item_formula)
                row += 1

    def display_meeting_point_results(self, results):
        self.results_table.setRowCount(0)
        param_map = {
            'x0': 'Posición inicial (m)', 'v0': 'Velocidad inicial (m/s)', 
            'a': 'Aceleración (m/s²)'
        }
        
        input_params = results.get('input_params', {})
        num_rows = sum(len(p) for p in input_params.values()) + len(results.get('calculated_values', {})) + len(results.get('equations', []))
        self.results_table.setRowCount(num_rows)

        row = 0
        for obj_name, params in input_params.items():
            for key, value in params.items():
                self.results_table.setItem(row, 0, QTableWidgetItem(f"Parámetro ({obj_name}): {param_map.get(key, key)}"))
                self.results_table.setItem(row, 1, QTableWidgetItem(str(value)))
                row += 1

        calculated_map = {
            'tiempo_encuentro': 'Tiempo de encuentro (s)',
            'posicion_encuentro': 'Posición de encuentro (m)'
        }
        for key, value in results.get('calculated_values', {}).items():
            self.results_table.setItem(row, 0, QTableWidgetItem(f"Calculado: {calculated_map.get(key, key)}"))
            self.results_table.setItem(row, 1, QTableWidgetItem(f"{value:.4f}"))
            row += 1
            
        if 'equations' in results:
            for eq in results['equations']:
                item_eq = QTableWidgetItem("Ecuación")
                item_formula = QTableWidgetItem(eq)
                
                tooltip = self.get_equation_tooltip(eq)
                item_formula.setToolTip(tooltip)
                
                self.results_table.setItem(row, 0, item_eq)
                self.results_table.setItem(row, 1, item_formula)
                row += 1

    def get_equation_tooltip(self, equation):
        tooltip_parts = []
        # A simple way to find variables in the equation string
        import re
        variables = set(re.findall(r'\b([a-zA-Z_]+[0-9]*)\b', equation))
        for var in variables:
            if var in self.variable_tooltips:
                tooltip_parts.append(f"{var}: {self.variable_tooltips[var]}")
        return "\n".join(tooltip_parts) if tooltip_parts else "Información de variables no disponible"

    def clear(self):
        self.results_table.setRowCount(0)
