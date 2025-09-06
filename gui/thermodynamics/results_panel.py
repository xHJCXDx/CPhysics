from gui.base_results_panel import BaseResultsPanel

class ResultsPanel(BaseResultsPanel):
    """Panel for displaying thermodynamics calculation results."""
    def display_results(self, results):
        self.clear()
        if not results:
            return

        param_map = {
            'P': 'Pressure (atm)', 'V': 'Volume (L)', 'n': 'Moles', 
            'T': 'Temperature (K)'
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

    def get_variable_tooltips(self):
        return {
            'P': 'Pressure (atm)', 'V': 'Volume (L)', 'n': 'Moles',
            'R': 'Ideal gas constant (0.0821 L·atm/(mol·K))', 'T': 'Temperature (K)'
        }

    def clear_results(self):
        self.clear()