from gui.base_results_panel import BaseResultsPanel

class ResultsPanel(BaseResultsPanel):
    def display_results(self, results):
        self.clear()
        if not results:
            return

        title = results.get('title', 'Resultados')
        self.results_table.setRowCount(0)

        param_map = {
            'f': 'Fuerza Aplicada (N)', 'm': 'Masa (kg)', 'a': 'Aceleración (m/s²)', 
            'mu': 'Coef. Fricción (μ)', 'angle': 'Ángulo del Plano (°)',
            'work_force': 'Fuerza (N)', 'work_distance': 'Distancia (m)', 'work_angle': 'Ángulo (θ°)',
            'ke_mass': 'Masa (kg)', 'ke_velocity': 'Velocidad (m/s)',
            'pe_mass': 'Masa (kg)', 'pe_height': 'Altura (m)',
            'impulse_force': 'Fuerza (N)', 'impulse_time': 'Tiempo (s)', 'impulse_impulse': 'Impulso (N·s)',
            'momentum_mass': 'Masa (kg)', 'momentum_velocity': 'Velocidad (m/s)', 'momentum_momentum': 'Momento (kg·m/s)',
            'normal_force': 'Fuerza Normal (N)', 'friction_force': 'Fuerza de Fricción (N)',
            'work': 'Trabajo (J)', 'kinetic_energy': 'Energía Cinética (J)', 'potential_energy': 'Energía Potencial (J)',
            'impulse': 'Impulso (N·s)', 'momentum': 'Momento Lineal (kg·m/s)'
        }

        input_params = results.get('input_params', {})
        calculated_values = results.get('calculated_values', {})
        equations = results.get('equations', [])
        
        # Special case for energy and momentum panels that have a simpler structure
        if 'work' in results or 'kinetic_energy' in results or 'potential_energy' in results or 'impulse' in results or 'momentum' in results:
            calculated_key = list(calculated_values.keys())[0]
            calculated_value = calculated_values[calculated_key]
            num_rows = len(input_params) + 2
            self.results_table.setRowCount(num_rows)
            row = 0
            for key, value in input_params.items():
                if value is not None:
                    self.add_row(row, f"Parámetro: {param_map.get(key, key)}", str(value))
                    row += 1
            self.add_row(row, f"Calculado: {param_map.get(calculated_key, calculated_key)}", f"{calculated_value:.4f}")
            row += 1
            tooltip = self.get_equation_tooltip(equations[0])
            self.add_row(row, "Ecuación", equations[0], tooltip)
        else: # For Newton's law
            num_rows = len(input_params) + len(calculated_values) + len(equations)
            if 'normal_force' in results: num_rows += 1
            if 'friction_force' in results: num_rows += 1
            self.results_table.setRowCount(num_rows)
            row = 0
            for key, value in input_params.items():
                if value is not None:
                    self.add_row(row, f"Parámetro: {param_map.get(key, key)}", str(value))
                    row += 1
            for key, value in calculated_values.items():
                self.add_row(row, f"Calculado: {param_map.get(key, key)}", f"{value:.4f}")
                row += 1
            if 'normal_force' in results:
                self.add_row(row, "Fuerza Normal (N)", f"{results['normal_force']:.4f}")
                row += 1
            if 'friction_force' in results:
                self.add_row(row, "Fuerza de Fricción (N)", f"{results['friction_force']:.4f}")
                row += 1
            for eq in equations:
                tooltip = self.get_equation_tooltip(eq)
                self.add_row(row, "Ecuación", eq, tooltip)
                row += 1

    def get_variable_tooltips(self):
        return {
            'F': 'Fuerza (N)', 'm': 'Masa (kg)', 'a': 'Aceleración (m/s²)',
            'μ': 'Coeficiente de fricción', 'N': 'Fuerza normal (N)',
            'W': 'Trabajo (J)', 'd': 'Distancia (m)', 'θ': 'Ángulo (°)',
            'KE': 'Energía cinética (J)', 'v': 'Velocidad (m/s)',
            'PE': 'Energía potencial (J)', 'h': 'Altura (m)', 'g': 'Gravedad (9.8 m/s²)',
            'I': 'Impulso (N·s)', 't': 'Tiempo (s)',
            'p': 'Momento lineal (kg·m/s)'
        }