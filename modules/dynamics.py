import numpy as np

class DynamicsCalculator:
    def __init__(self):
        self.g = 9.81 # Acceleration due to gravity

    def calculate_newton_second_law(self, params, mu=None):
        """
        Calcular parámetros para la Segunda Ley de Newton (F = m * a),
        con fricción opcional.
        F se considera la fuerza aplicada.
        """
        f = params.get('f') # Applied force
        m = params.get('m')
        a = params.get('a')

        provided_params_count = sum(p is not None for p in [f, m, a])
        if provided_params_count != 2:
            raise ValueError("Debe proporcionar exactamente dos de los tres parámetros (fuerza, masa, aceleración).")

        input_params = {'f': f, 'm': m, 'a': a}
        calculated_values = {}
        equations = []
        friction_force = None

        use_friction = mu is not None and mu > 0

        if f is None: # Calculate Applied Force
            if m <= 0: raise ValueError("La masa debe ser un valor positivo.")
            f_net = m * a
            equations.append("F_neta = m × a")
            f_applied = f_net
            if use_friction:
                friction_force = mu * m * self.g
                f_applied += friction_force
                equations.extend(["F_fricción = μ × m × g", "F_aplicada = F_neta + F_fricción"])
            if not np.isfinite(f_applied): raise ValueError("El resultado de la fuerza es infinito.")
            calculated_values = {'f': f_applied}

        elif m is None: # Calculate Mass
            denominator = a
            if use_friction:
                denominator += mu * self.g
                equations.append("m = F_aplicada / (a + μ × g)")
            else:
                equations.append("m = F_aplicada / a")
            if denominator == 0: raise ValueError("División por cero: (a + μ × g) no puede ser cero.")
            m_calc = f / denominator
            if not np.isfinite(m_calc): raise ValueError("El resultado de la masa es infinito.")
            if m_calc <= 0: raise ValueError("La masa calculada debe ser positiva.")
            calculated_values = {'m': m_calc}

        elif a is None: # Calculate Acceleration
            if m <= 0: raise ValueError("La masa debe ser un valor positivo y no nulo.")
            f_net = f
            if use_friction:
                friction_force = mu * m * self.g
                f_net -= friction_force
                equations.extend(["F_fricción = μ × m × g", "F_neta = F_aplicada - F_fricción"])
            a_calc = f_net / m
            equations.append("a = F_neta / m")
            if not np.isfinite(a_calc): raise ValueError("El resultado de la aceleración es infinito.")
            calculated_values = {'a': a_calc}

        final_results = {
            'input_params': {k: v for k, v in input_params.items() if v is not None},
            'calculated_values': calculated_values,
            'equations': equations
        }
        if friction_force is not None:
            final_results['friction_force'] = friction_force
        if use_friction:
            final_results['input_params']['mu'] = mu
        
        return final_results

    def generate_plot_data(self, results, num_points=100):
        input_params = results['input_params']
        calculated_values = results['calculated_values']
        all_params = {**input_params, **calculated_values}

        f = all_params.get('f')
        m = all_params.get('m')
        a = all_params.get('a')
        mu = all_params.get('mu', 0)

        calculated_var = list(calculated_values.keys())[0]

        if calculated_var == 'a':
            # F_app vs m (a is constant) -> F_app = m * (a + mu*g)
            x_label, y_label = 'Masa (kg)', 'Fuerza Aplicada (N)'
            title = f'Fuerza vs. Masa (a = {a:.2f} m/s²)'
            if mu > 0: title += f' (μ = {mu})'
            
            m_max = m * 2 if m > 0 else 10
            m_min = 0.1
            if m_max < m_min: m_min, m_max = m_max, m_min
            
            x_data = np.linspace(m_min, m_max, num_points) # mass values
            y_data = x_data * (a + mu * self.g) # applied force values
        else: 
            # F_app vs a (m is constant) -> F_app = m*a + mu*m*g
            x_label, y_label = 'Aceleración (m/s²)', 'Fuerza Aplicada (N)'
            title = f'Fuerza vs. Aceleración (Masa = {m:.2f} kg)'
            if mu > 0: title += f' (μ = {mu})'

            a_max = a * 2 if a != 0 else 10
            a_min = -abs(a_max)
            if a_max < a_min: a_min, a_max = a_max, a_min

            x_data = np.linspace(a_min, a_max, num_points) # acceleration values
            y_data = m * x_data + mu * m * self.g # applied force values

        if not np.all(np.isfinite(x_data)) or not np.all(np.isfinite(y_data)):
            raise ValueError("Los datos generados para el gráfico contienen valores infinitos.")

        return {
            'x_data': x_data, 'y_data': y_data,
            'x_label': x_label, 'y_label': y_label,
            'title': title
        }