from gui.base_results_panel import BaseResultsPanel

class ResultsPanel(BaseResultsPanel):
    def display_results(self, results):
        self.clear()
        if not results:
            return

        param_map = {
            'amplitude': 'Amplitude (m)', 'frequency': 'Frequency (Hz)', 'wavelength': 'Wavelength (m)',
            'wave_number': 'Wave Number (rad/m)', 'angular_frequency': 'Angular Frequency (rad/s)',
            'period': 'Period (s)', 'velocity': 'Velocity (m/s)', 'phase': 'Phase (rad)'
        }

        calculated_values = results.get('calculated_values', {})
        equations = results.get('equations', [])
        
        num_rows = len(calculated_values) + len(equations) + 1 # +1 for the wave equation
        self.results_table.setRowCount(num_rows)
        
        row = 0
        for key, value in calculated_values.items():
            self.add_row(row, f"Calculated: {param_map.get(key, key)}", f"{value:.4f}")
            row += 1
            
        for eq in equations:
            tooltip = self.get_equation_tooltip(eq)
            self.add_row(row, "Equation", eq, tooltip)
            row += 1

        # Wave equation
        vals = results.get('all_values', {})
        A = vals.get('amplitude')
        k = vals.get('wave_number')
        omega = vals.get('angular_frequency')
        phi = vals.get('phase', 0)

        if all(v is not None for v in [A, k, omega]):
            phi_str = f" + {phi:.2f}" if phi != 0 else ""
            wave_eq = f"y(x,t) = {A:.2f} cos({k:.2f}x - {omega:.2f}t{phi_str})"
            tooltip = self.get_equation_tooltip(wave_eq)
            self.add_row(row, "Ecuación de la Onda", wave_eq, tooltip)

    def get_variable_tooltips(self):
        return {
            'y': 'Desplazamiento vertical (m)', 'x': 'Posición horizontal (m)', 't': 'Tiempo (s)',
            'A': 'Amplitud (m)', 'k': 'Número de onda (rad/m)', 'ω': 'Frecuencia angular (rad/s)',
            'φ': 'Fase (rad)', 'f': 'Frecuencia (Hz)', 'λ': 'Longitud de onda (m)',
            'T': 'Período (s)', 'v': 'Velocidad (m/s)'
        }