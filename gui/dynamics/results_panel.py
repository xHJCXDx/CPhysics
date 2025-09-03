from gui.base_results_panel import BaseResultsPanel

class ResultsPanel(BaseResultsPanel):
    def display_results(self, results):
        self.clear()
        if not results:
            return

        title = results.get('title', 'Results')
        self.results_table.setRowCount(0)

        param_map = {
            'f': 'Applied Force (N)', 'm': 'Mass (kg)', 'a': 'Acceleration (m/s²)', 
            'mu': 'Friction Coef. (μ)', 'angle': 'Plane Angle (°)',
            'work_force': 'Force (N)', 'work_distance': 'Distance (m)', 'work_angle': 'Angle (θ°)',
            'ke_mass': 'Mass (kg)', 'ke_velocity': 'Velocity (m/s)',
            'pe_mass': 'Mass (kg)', 'pe_height': 'Height (m)',
            'impulse_force': 'Force (N)', 'impulse_time': 'Time (s)', 'impulse_impulse': 'Impulse (N·s)',
            'momentum_mass': 'Mass (kg)', 'momentum_velocity': 'Velocity (m/s)', 'momentum_momentum': 'Momentum (kg·m/s)',
            'normal_force': 'Normal Force (N)', 'friction_force': 'Friction Force (N)',
            'work': 'Work (J)', 'kinetic_energy': 'Kinetic Energy (J)', 'potential_energy': 'Potential Energy (J)',
            'impulse': 'Impulse (N·s)', 'momentum': 'Linear Momentum (kg·m/s)'
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
                    self.add_row(row, f"Parameter: {param_map.get(key, key)}", str(value))
                    row += 1
            self.add_row(row, f"Calculated: {param_map.get(calculated_key, calculated_key)}", f"{calculated_value:.4f}")
            row += 1
            tooltip = self.get_equation_tooltip(equations[0])
            self.add_row(row, "Equation", equations[0], tooltip)
        else: # For Newton's law
            num_rows = len(input_params) + len(calculated_values) + len(equations)
            if 'normal_force' in results: num_rows += 1
            if 'friction_force' in results: num_rows += 1
            self.results_table.setRowCount(num_rows)
            row = 0
            for key, value in input_params.items():
                if value is not None:
                    self.add_row(row, f"Parameter: {param_map.get(key, key)}", str(value))
                    row += 1
            for key, value in calculated_values.items():
                self.add_row(row, f"Calculated: {param_map.get(key, key)}", f"{value:.4f}")
                row += 1
            if 'normal_force' in results:
                self.add_row(row, "Normal Force (N)", f"{results['normal_force']:.4f}")
                row += 1
            if 'friction_force' in results:
                self.add_row(row, "Friction Force (N)", f"{results['friction_force']:.4f}")
                row += 1
            for eq in equations:
                tooltip = self.get_equation_tooltip(eq)
                self.add_row(row, "Equation", eq, tooltip)
                row += 1

    def get_variable_tooltips(self):
        return {
            'F': 'Force (N)', 'm': 'Mass (kg)', 'a': 'Acceleration (m/s²)',
            'μ': 'Friction coefficient', 'N': 'Normal force (N)',
            'W': 'Work (J)', 'd': 'Distance (m)', 'θ': 'Angle (°)',
            'KE': 'Kinetic energy (J)', 'v': 'Velocity (m/s)',
            'PE': 'Potential energy (J)', 'h': 'Height (m)', 'g': 'Gravity (9.8 m/s²)',
            'I': 'Impulse (N·s)', 't': 'Time (s)',
            'p': 'Linear momentum (kg·m/s)'
        }