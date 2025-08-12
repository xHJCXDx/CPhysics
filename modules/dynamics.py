import numpy as np

class DynamicsCalculator:
    def __init__(self):
        self.g = 9.81 # Acceleration due to gravity

    def calculate_newton_second_law(self, params, mu=None, angle=None):
        """
        Calcular parámetros para la Segunda Ley de Newton (F = m * a),
        con fricción y plano inclinado opcionales.
        F se considera la fuerza aplicada paralela al plano.
        """
        f = params.get('f')
        m = params.get('m')
        a = params.get('a')

        provided_params_count = sum(p is not None for p in [f, m, a])
        if provided_params_count != 2:
            raise ValueError("Debe proporcionar exactamente dos de los tres parámetros (fuerza, masa, aceleración).")

        input_params = {'f': f, 'm': m, 'a': a}
        calculated_values = {}
        equations = []
        friction_force = None
        normal_force = None

        use_friction = mu is not None and mu > 0
        use_incline = angle is not None and 0 <= angle <= 90

        theta = np.deg2rad(angle) if use_incline else 0

        if m is not None:
            normal_force = m * self.g * np.cos(theta)
            if use_incline:
                equations.append("F_normal = m × g × cos(θ)")

        if use_friction and normal_force is not None:
            friction_force = mu * normal_force
            equations.append("F_fricción = μ × F_normal")

        # --- Calculation Logic ---
        if f is None: # Calculate Applied Force
            if m <= 0: raise ValueError("La masa debe ser un valor positivo.")
            f_net = m * a
            equations.append("F_neta = m × a")
            
            gravity_component = m * self.g * np.sin(theta) if use_incline else 0
            if use_incline: equations.append("F_gravedad_paralela = m × g × sin(θ)")

            f_applied = f_net + gravity_component + (friction_force if friction_force is not None else 0)
            equations.append("F_aplicada = F_neta + F_gravedad_paralela + F_fricción")

            if not np.isfinite(f_applied): raise ValueError("El resultado de la fuerza es infinito.")
            calculated_values = {'f': f_applied}

        elif m is None: # Calculate Mass
            # f_app = m*a + m*g*sin(theta) + mu*m*g*cos(theta)
            # f_app = m * (a + g*sin(theta) + mu*g*cos(theta))
            denominator = a + self.g * np.sin(theta) + (mu * self.g * np.cos(theta) if use_friction else 0)
            if denominator == 0: raise ValueError("División por cero: El denominador (aceleración + componentes de gravedad/fricción) no puede ser cero.")
            
            m_calc = f / denominator
            equations.append("m = F_aplicada / (a + g·sin(θ) + μ·g·cos(θ))")

            if not np.isfinite(m_calc): raise ValueError("El resultado de la masa es infinito.")
            if m_calc <= 0: raise ValueError("La masa calculada debe ser positiva.")
            calculated_values = {'m': m_calc}
            # Recalculate forces with the new mass
            normal_force = m_calc * self.g * np.cos(theta)
            if use_friction: friction_force = mu * normal_force

        elif a is None: # Calculate Acceleration
            if m <= 0: raise ValueError("La masa debe ser un valor positivo y no nulo.")
            
            gravity_component = m * self.g * np.sin(theta) if use_incline else 0
            if use_incline: equations.append("F_gravedad_paralela = m × g × sin(θ)")

            f_net = f - gravity_component - (friction_force if friction_force is not None else 0)
            equations.append("F_neta = F_aplicada - F_gravedad_paralela - F_fricción")

            a_calc = f_net / m
            equations.append("a = F_neta / m")
            if not np.isfinite(a_calc): raise ValueError("El resultado de la aceleración es infinito.")
            calculated_values = {'a': a_calc}

        # --- Final Results Packaging ---
        final_results = {
            'input_params': {k: v for k, v in input_params.items() if v is not None},
            'calculated_values': calculated_values,
            'equations': equations
        }
        if normal_force is not None:
            final_results['normal_force'] = normal_force
        if friction_force is not None:
            final_results['friction_force'] = friction_force
        if use_friction:
            final_results['input_params']['mu'] = mu 
        if use_incline:
            final_results['input_params']['angle'] = angle
        
        return final_results

    def calculate_work(self, force, distance, angle=0):
        if force is None or distance is None:
            raise ValueError("La fuerza y la distancia son requeridas.")
        if not all(isinstance(i, (int, float)) for i in [force, distance, angle]):
            raise TypeError("Los valores deben ser numéricos.")
        
        theta = np.deg2rad(angle)
        work = force * distance * np.cos(theta)
        
        return {
            'work': work,
            'equation': "W = F × d × cos(θ)"
        }

    def calculate_kinetic_energy(self, mass, velocity):
        if mass is None or velocity is None:
            raise ValueError("La masa y la velocidad son requeridas.")
        if not all(isinstance(i, (int, float)) for i in [mass, velocity]):
            raise TypeError("Los valores deben ser numéricos.")
        if mass <= 0:
            raise ValueError("La masa debe ser un valor positivo.")
            
        kinetic_energy = 0.5 * mass * velocity**2
        
        return {
            'kinetic_energy': kinetic_energy,
            'equation': "KE = 0.5 × m × v²"
        }

    def calculate_potential_energy(self, mass, height):
        if mass is None or height is None:
            raise ValueError("La masa y la altura son requeridas.")
        if not all(isinstance(i, (int, float)) for i in [mass, height]):
            raise TypeError("Los valores deben ser numéricos.")
        if mass <= 0:
            raise ValueError("La masa debe ser un valor positivo.")

        potential_energy = mass * self.g * height
        
        return {
            'potential_energy': potential_energy,
            'equation': "PE = m × g × h"
        }

    def calculate_impulse(self, force, time, impulse):
        params = {'force': force, 'time': time, 'impulse': impulse}
        provided_params = [k for k, v in params.items() if v is not None]

        if len(provided_params) != 2:
            raise ValueError("Debe proporcionar exactamente dos de los tres parámetros (fuerza, tiempo, impulso).")

        if 'impulse' not in provided_params:
            result = force * time
            return {'impulse': result, 'equation': "I = F × t"}
        elif 'force' not in provided_params:
            if time == 0: raise ValueError("El tiempo no puede ser cero.")
            result = impulse / time
            return {'force': result, 'equation': "F = I / t"}
        elif 'time' not in provided_params:
            if force == 0: raise ValueError("La fuerza no puede ser cero.")
            result = impulse / force
            return {'time': result, 'equation': "t = I / F"}

    def calculate_linear_momentum(self, mass, velocity, momentum):
        params = {'mass': mass, 'velocity': velocity, 'momentum': momentum}
        provided_params = [k for k, v in params.items() if v is not None]

        if len(provided_params) != 2:
            raise ValueError("Debe proporcionar exactamente dos de los tres parámetros (masa, velocidad, momento).")

        if 'momentum' not in provided_params:
            result = mass * velocity
            return {'momentum': result, 'equation': "p = m × v"}
        elif 'mass' not in provided_params:
            if velocity == 0: raise ValueError("La velocidad no puede ser cero.")
            result = momentum / velocity
            return {'mass': result, 'equation': "m = p / v"}
        elif 'velocity' not in provided_params:
            if mass == 0: raise ValueError("La masa no puede ser cero.")
            result = momentum / mass
            return {'velocity': result, 'equation': "v = p / m"}

    def generate_plot_data(self, results, num_points=100):
        input_params = results['input_params']
        calculated_values = results['calculated_values']
        all_params = {**input_params, **calculated_values}

        f = all_params.get('f')
        m = all_params.get('m')
        a = all_params.get('a')
        mu = all_params.get('mu', 0)
        angle = all_params.get('angle', 0)
        theta = np.deg2rad(angle)

        calculated_var = list(calculated_values.keys())[0]

        # F_app = m*a + m*g*sin(theta) + mu*m*g*cos(theta)
        # F_app = m * (a + g*sin(theta) + mu*g*cos(theta))
        # F_app = a*m + (g*sin(theta) + mu*g*cos(theta))*m

        if calculated_var == 'a':
            # Plot F_app vs m (a is constant)
            x_label, y_label = 'Masa (kg)', 'Fuerza Aplicada (N)'
            title = f'Fuerza vs. Masa (a = {a:.2f} m/s²)'
            if angle > 0: title += f' (θ = {angle}°)'
            if mu > 0: title += f' (μ = {mu})'
            
            m_max = m * 2 if m > 0 else 10
            m_min = 0.1
            if m_max <= m_min: m_max = m_min + 10
            
            x_data = np.linspace(m_min, m_max, num_points) # mass values
            y_data = x_data * (a + self.g * np.sin(theta) + mu * self.g * np.cos(theta))
        else: 
            # Plot F_app vs a (m is constant)
            x_label, y_label = 'Aceleración (m/s²)', 'Fuerza Aplicada (N)'
            title = f'Fuerza vs. Aceleración (Masa = {m:.2f} kg)'
            if angle > 0: title += f' (θ = {angle}°)'
            if mu > 0: title += f' (μ = {mu})'

            a_max = a * 2 if a != 0 else 10
            a_min = -abs(a_max) - (self.g * np.sin(theta) + mu * self.g * np.cos(theta))
            if a_max <= a_min: a_max = a_min + 10

            x_data = np.linspace(a_min, a_max, num_points) # acceleration values
            y_data = m * x_data + m * self.g * np.sin(theta) + mu * m * self.g * np.cos(theta)

        if not np.all(np.isfinite(x_data)) or not np.all(np.isfinite(y_data)):
            raise ValueError("Los datos generados para el gráfico contienen valores infinitos.")

        return {
            'x_data': x_data, 'y_data': y_data,
            'x_label': x_label, 'y_label': y_label,
            'title': title
        }