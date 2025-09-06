from PySide6.QtWidgets import QTableWidgetItem
from gui.base_results_panel import BaseResultsPanel

class ResultsPanel(BaseResultsPanel):
    """Panel for displaying kinematics calculation results."""
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
            'x0': 'Initial position (m)', 'y0': 'Initial height (m)', 'v0': 'Initial velocity (m/s)', 
            'a': 'Acceleration (m/s²)', 't': 'Time (s)', 
            'x': 'Final position (m)', 'v': 'Final velocity (m/s)',
            'angle': 'Launch angle (°)',
            'time_of_flight': 'Time of flight (s)',
            'max_height': 'Maximum height (m)',
            'range': 'Range (m)',
            'v0x': 'Initial velocity in x (m/s)',
            'v0y': 'Initial velocity in y (m/s)'
        }

        input_params = results.get('input_params', {})
        calculated_values = results.get('calculated_values', {})
        equations = results.get('equations', [])

        num_rows = len(input_params) + len(calculated_values) + len(equations)
        self.results_table.setRowCount(num_rows)

        row = 0
        for key, value in input_params.items():
            if value is not None:
                self.add_row(row, f"Parameter: {param_map.get(key, key)}", str(value))
                row += 1

        for key, value in calculated_values.items():
            self.add_row(row, f"Calculated: {param_map.get(key, key)}", f"{value:.4f}")
            row += 1

        for eq in equations:
            tooltip = self.get_equation_tooltip(eq)
            self.add_row(row, "Equation", eq, tooltip)
            row += 1

    def display_meeting_point_results(self, results):
        param_map = {
            'x0': 'Initial position (m)', 'v0': 'Initial velocity (m/s)', 
            'a': 'Acceleration (m/s²)'
        }
        input_params = results.get('input_params', {})
        calculated_values = results.get('calculated_values', {})
        equations = results.get('equations', [])

        num_rows = sum(len(p) for p in input_params.values()) + len(calculated_values) + len(equations)
        self.results_table.setRowCount(num_rows)

        row = 0
        for obj_name, params in input_params.items():
            for key, value in params.items():
                self.add_row(row, f"Parameter ({obj_name}): {param_map.get(key, key)}", str(value))
                row += 1

        calculated_map = {
            'tiempo_encuentro': 'Meeting time (s)',
            'posicion_encuentro': 'Meeting position (m)'
        }
        for key, value in calculated_values.items():
            self.add_row(row, f"Calculated: {calculated_map.get(key, key)}", f"{value:.4f}")
            row += 1

        for eq in equations:
            tooltip = self.get_equation_tooltip(eq)
            self.add_row(row, "Equation", eq, tooltip)
            row += 1

    def get_variable_tooltips(self):
        return {
            'x': 'Final position (m)', 'x0': 'Initial position (m)',
            'y': 'Final height (m)', 'y0': 'Initial height (m)',
            'v': 'Final velocity (m/s)', 'v0': 'Initial velocity (m/s)',
            'a': 'Acceleration (m/s²)', 't': 'Time (s)',
            'g': 'Gravity acceleration (9.8 m/s²)',
            'v0x': 'Initial velocity in x (m/s)',
            'v0y': 'Initial velocity in y (m/s)',
            'vx': 'Velocity in x (m/s)', 'vy': 'Velocity in y (m/s)',
            'θ': 'Launch angle (°)',
            't_vuelo': 'Time of flight (s)',
            'y_max': 'Maximum height (m)',
            'R': 'Horizontal range (m)'
        }