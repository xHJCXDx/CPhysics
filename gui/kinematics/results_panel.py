from PySide6.QtWidgets import QTableWidgetItem
from gui.base_results_panel import BaseResultsPanel

class ResultsPanel(BaseResultsPanel):
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

        input_params = results.get('input_params', {})
        calculated_values = results.get('calculated_values', {})
        equations = results.get('equations', [])
        
        num_rows = len(input_params) + len(calculated_values) + len(equations)
        self.results_table.setRowCount(num_rows)
        
        row = 0
        for key, value in input_params.items():
            if value is not None:
                self.add_row(row, f"Parámetro: {param_map.get(key, key)}", str(value))
                row += 1

        for key, value in calculated_values.items():
            self.add_row(row, f"Calculado: {param_map.get(key, key)}", f"{value:.4f}")
            row += 1
            
        for eq in equations:
            tooltip = self.get_equation_tooltip(eq)
            self.add_row(row, "Ecuación", eq, tooltip)
            row += 1

    def display_meeting_point_results(self, results):
        param_map = {
            'x0': 'Posición inicial (m)', 'v0': 'Velocidad inicial (m/s)', 
            'a': 'Aceleración (m/s²)'
        }
        
        input_params = results.get('input_params', {})
        calculated_values = results.get('calculated_values', {})
        equations = results.get('equations', [])

        num_rows = sum(len(p) for p in input_params.values()) + len(calculated_values) + len(equations)
        self.results_table.setRowCount(num_rows)

        row = 0
        for obj_name, params in input_params.items():
            for key, value in params.items():
                self.add_row(row, f"Parámetro ({obj_name}): {param_map.get(key, key)}", str(value))
                row += 1

        calculated_map = {
            'tiempo_encuentro': 'Tiempo de encuentro (s)',
            'posicion_encuentro': 'Posición de encuentro (m)'
        }
        for key, value in calculated_values.items():
            self.add_row(row, f"Calculado: {calculated_map.get(key, key)}", f"{value:.4f}")
            row += 1
            
        for eq in equations:
            tooltip = self.get_equation_tooltip(eq)
            self.add_row(row, "Ecuación", eq, tooltip)
            row += 1

    def get_variable_tooltips(self):
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