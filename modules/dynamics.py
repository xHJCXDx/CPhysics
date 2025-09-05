"""
Dynamics calculations module.

Provides the DynamicsCalculator class to solve problems related to
Newton's Second Law, work, energy, impulse, and momentum.
"""

import numpy as np

class DynamicsCalculator:
    """Performs dynamics calculations."""

    def __init__(self):
        """Initializes the calculator with the gravitational constant."""
        self.g = 9.81  # Acceleration due to gravity (m/s^2)

    def calculate_newton_second_law(self, params, mu=None, angle=None):
        """
        Calculates a parameter for Newton's Second Law (F=ma).

        This method can account for friction and inclined planes.
        The force 'f' is considered the applied force parallel to the plane of motion.

        Args:
            params (dict): A dictionary containing two of the three parameters:
                           'f' (force), 'm' (mass), 'a' (acceleration).
            mu (float, optional): The coefficient of kinetic friction. Defaults to None.
            angle (float, optional): The angle of inclination in degrees. Defaults to None.

        Returns:
            dict: A dictionary containing the calculated value, input parameters,
                  and relevant equations.
        """
        f = params.get('f')
        m = params.get('m')
        a = params.get('a')

        if sum(p is not None for p in [f, m, a]) != 2:
            raise ValueError("Exactly two of the three parameters (force, mass, acceleration) are required.")

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
                equations.append("N = m × g × cos(θ)")

        if use_friction and normal_force is not None:
            friction_force = mu * normal_force
            equations.append("F_friction = μ × N")

        # --- Calculation Logic ---
        if f is None:  # Calculate Applied Force
            if m <= 0:
                raise ValueError("Mass must be a positive value.")
            f_net = m * a
            equations.append("F_net = m × a")
            
            gravity_component = m * self.g * np.sin(theta) if use_incline else 0
            if use_incline:
                equations.append("F_gravity_parallel = m × g × sin(θ)")

            f_applied = f_net + gravity_component + (friction_force if friction_force is not None else 0)
            equations.append("F_applied = F_net + F_gravity_parallel + F_friction")

            if not np.isfinite(f_applied):
                raise ValueError("The resulting force is infinite.")
            calculated_values = {'f': f_applied}

        elif m is None:  # Calculate Mass
            denominator = a + self.g * np.sin(theta) + (mu * self.g * np.cos(theta) if use_friction else 0)
            if denominator == 0:
                raise ValueError("Division by zero: acceleration and resistive forces cancel out.")
            
            m_calc = f / denominator
            equations.append("m = F_applied / (a + g·sin(θ) + μ·g·cos(θ))")

            if not np.isfinite(m_calc):
                raise ValueError("The resulting mass is infinite.")
            if m_calc <= 0:
                raise ValueError("Calculated mass must be positive.")
            calculated_values = {'m': m_calc}
            
            # Recalculate forces with the new mass for the report.
            normal_force = m_calc * self.g * np.cos(theta)
            if use_friction:
                friction_force = mu * normal_force

        elif a is None:  # Calculate Acceleration
            if m <= 0:
                raise ValueError("Mass must be a positive, non-zero value.")
            
            gravity_component = m * self.g * np.sin(theta) if use_incline else 0
            if use_incline:
                equations.append("F_gravity_parallel = m × g × sin(θ)")

            f_net = f - gravity_component - (friction_force if friction_force is not None else 0)
            equations.append("F_net = F_applied - F_gravity_parallel - F_friction")

            a_calc = f_net / m
            equations.append("a = F_net / m")
            if not np.isfinite(a_calc):
                raise ValueError("The resulting acceleration is infinite.")
            calculated_values = {'a': a_calc}

        # --- Package Results ---
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
        """Calculates work done by a constant force."""
        if force is None or distance is None:
            raise ValueError("Force and distance are required.")
        if not all(isinstance(i, (int, float)) for i in [force, distance, angle]):
            raise TypeError("All values must be numeric.")
        
        theta = np.deg2rad(angle)
        work = force * distance * np.cos(theta)
        
        return {
            'work': work,
            'equation': "W = F × d × cos(θ)"
        }

    def calculate_kinetic_energy(self, mass, velocity):
        """Calculates kinetic energy."""
        if mass is None or velocity is None:
            raise ValueError("Mass and velocity are required.")
        if not all(isinstance(i, (int, float)) for i in [mass, velocity]):
            raise TypeError("All values must be numeric.")
        if mass <= 0:
            raise ValueError("Mass must be a positive value.")
            
        kinetic_energy = 0.5 * mass * velocity**2
        
        return {
            'kinetic_energy': kinetic_energy,
            'equation': "KE = 0.5 × m × v²"
        }

    def calculate_potential_energy(self, mass, height):
        """Calculates gravitational potential energy."""
        if mass is None or height is None:
            raise ValueError("Mass and height are required.")
        if not all(isinstance(i, (int, float)) for i in [mass, height]):
            raise TypeError("All values must be numeric.")
        if mass <= 0:
            raise ValueError("Mass must be a positive value.")

        potential_energy = mass * self.g * height
        
        return {
            'potential_energy': potential_energy,
            'equation': "PE = m × g × h"
        }

    def calculate_impulse(self, force, time, impulse):
        """Calculates impulse, force, or time given the other two."""
        params = {'force': force, 'time': time, 'impulse': impulse}
        provided_params = [k for k, v in params.items() if v is not None]

        if len(provided_params) != 2:
            raise ValueError("Exactly two of the three parameters (force, time, impulse) are required.")

        if 'impulse' not in provided_params:
            result = force * time
            return {'impulse': result, 'equation': "I = F × t"}
        elif 'force' not in provided_params:
            if time == 0:
                raise ValueError("Time cannot be zero.")
            result = impulse / time
            return {'force': result, 'equation': "F = I / t"}
        elif 'time' not in provided_params:
            if force == 0:
                raise ValueError("Force cannot be zero.")
            result = impulse / force
            return {'time': result, 'equation': "t = I / F"}

    def calculate_linear_momentum(self, mass, velocity, momentum):
        """Calculates momentum, mass, or velocity given the other two."""
        params = {'mass': mass, 'velocity': velocity, 'momentum': momentum}
        provided_params = [k for k, v in params.items() if v is not None]

        if len(provided_params) != 2:
            raise ValueError("Exactly two of the three parameters (mass, velocity, momentum) are required.")

        if 'momentum' not in provided_params:
            result = mass * velocity
            return {'momentum': result, 'equation': "p = m × v"}
        elif 'mass' not in provided_params:
            if velocity == 0:
                raise ValueError("Velocity cannot be zero.")
            result = momentum / velocity
            return {'mass': result, 'equation': "m = p / v"}
        elif 'velocity' not in provided_params:
            if mass == 0:
                raise ValueError("Mass cannot be zero.")
            result = momentum / mass
            return {'velocity': result, 'equation': "v = p / m"}

    def generate_custom_plot_data(self, x_var, y_var, constant_value, mu=None, angle=None, num_points=100):
        """
        Generates data for a custom plot based on Newton's Second Law.

        The base equation is: F_applied = m*a + m*g*sin(θ) + μ*m*g*cos(θ)
        """
        all_vars = {"f", "m", "a"}
        constant_var = list(all_vars - {x_var, y_var})[0]

        mu = mu if mu is not None else 0
        theta = np.deg2rad(angle) if angle is not None else 0

        var_map = {
            "f": ("Applied Force (N)", constant_value),
            "m": ("Mass (kg)", constant_value),
            "a": ("Acceleration (m/s²)", constant_value)
        }
        
        params = {constant_var: constant_value}
        f, m, a = params.get('f'), params.get('m'), params.get('a')

        # Define ranges for X-axis data.
        if x_var == 'f':
            x_data = np.linspace(0, 2 * (m * a if m and a else 10), num_points) if f is None else np.linspace(0, 2 * f, num_points)
        elif x_var == 'm':
            x_data = np.linspace(0.1, 2 * (f / a if f and a else 10), num_points) if m is None else np.linspace(0.1, 2 * m, num_points)
        elif x_var == 'a':
            x_data = np.linspace(-10, 2 * (f / m if f and m else 10), num_points) if a is None else np.linspace(a - 10, a + 10, num_points)

        # Calculate Y-axis data based on F = m*a + F_resistance.
        def F_resistance(mass):
            return mass * self.g * np.sin(theta) + mu * mass * self.g * np.cos(theta)

        if y_var == 'f':
            if x_var == 'm':  # y: F, x: M, const: A
                y_data = x_data * a + F_resistance(x_data)
            elif x_var == 'a':  # y: F, x: A, const: M
                y_data = m * x_data + F_resistance(m)
        
        elif y_var == 'm':
            if x_var == 'f':  # y: M, x: F, const: A
                denominator = a + self.g * np.sin(theta) + mu * self.g * np.cos(theta)
                if denominator == 0:
                    raise ValueError("Division by zero when calculating mass.")
                y_data = x_data / denominator
            elif x_var == 'a':  # y: M, x: A, const: F
                denominator = x_data + self.g * np.sin(theta) + mu * self.g * np.cos(theta)
                y_data = np.divide(f, denominator, where=denominator != 0)

        elif y_var == 'a':
            if x_var == 'f':  # y: A, x: F, const: M
                y_data = (x_data - F_resistance(m)) / m if m > 0 else np.zeros(num_points)
            elif x_var == 'm':  # y: A, x: M, const: F
                y_data = (f - F_resistance(x_data)) / x_data if np.all(x_data > 0) else np.zeros(num_points)

        if not np.all(np.isfinite(x_data)) or not np.all(np.isfinite(y_data)):
            raise ValueError("Generated data for the graph contains infinite values.")

        # Create labels and title for the plot.
        x_label = var_map[x_var][0].replace(" (constant)", "")
        y_label = var_map[y_var][0].replace(" (constant)", "")
        const_label, const_val = var_map[constant_var]
        title = f'{y_label.split(" (")[0]} vs. {x_label.split(" (")[0]}\n({const_label.split(" (")[0]} = {const_val:.2f})'
        if angle is not None and angle > 0:
            title += f' (θ={angle}°)'
        if mu is not None and mu > 0:
            title += f' (μ={mu})'

        return {
            'x_data': x_data, 'y_data': y_data,
            'x_label': x_label, 'y_label': y_label,
            'title': title
        }