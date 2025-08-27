from gui.base_results_panel import BaseResultsPanel

class ResultsPanel(BaseResultsPanel):
    def display_results(self, results, input_fields=None):
        self.clear()
        if not results:
            return

        calculated_values = results.get('calculated_values', {})
        if calculated_values and input_fields:
            calculated_var, calculated_val = list(calculated_values.items())[0]
            if calculated_var in input_fields:
                input_fields[calculated_var].setText(f"{calculated_val:.4e}")

        param_map = {'q1': 'Carga 1 (C)', 'q2': 'Carga 2 (C)', 'r': 'Distancia (m)', 'F': 'Fuerza (N)'}

        input_params = results.get('input_params', {})
        equations = results.get('equations', [])
        
        num_rows = len(input_params) + len(calculated_values) + len(equations)
        self.results_table.setRowCount(num_rows)
        
        row = 0
        for key, value in input_params.items():
            if value is not None:
                self.add_row(row, f"Parámetro: {param_map.get(key, key)}", f"{value:.4e}")
                row += 1

        for key, value in calculated_values.items():
            self.add_row(row, f"Calculado: {param_map.get(key, key)}", f"{value:.4e}")
            row += 1
            
        for eq in equations:
            tooltip = self.get_equation_tooltip(eq)
            self.add_row(row, "Ecuación", eq, tooltip)
            row += 1

    def get_variable_tooltips(self):
        return {
            'F': 'Fuerza eléctrica (N)', 'k': 'Constante de Coulomb (8.987e9 N·m²/C²)',
            'q1': 'Carga 1 (C)', 'q2': 'Carga 2 (C)', 'r': 'Distancia (m)'
        }

    def clear_results(self):
        self.clear()