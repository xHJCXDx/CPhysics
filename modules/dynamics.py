"""
Módulo de cálculos de dinámica
Contiene las funciones para resolver problemas basados en las Leyes de Newton
"""

import numpy as np

class DynamicsCalculator:
    def __init__(self):
        pass

    def calculate_newton_second_law(self, params):
        """
        Calcular parámetros para la Segunda Ley de Newton (F = m * a)

        Se deben proporcionar exactamente dos de los tres parámetros:
        f (fuerza), m (masa), a (aceleración)
        """
        f = params.get('f')
        m = params.get('m')
        a = params.get('a')

        # Contar cuántos parámetros se han proporcionado
        provided_params_count = sum(p is not None for p in [f, m, a])

        if provided_params_count != 2:
            raise ValueError("Debe proporcionar exactamente dos de los tres parámetros (fuerza, masa, aceleración).")

        input_params = {}
        calculated_values = {}
        equations = ["F = m × a"]

        if f is None:
            # Calcular Fuerza
            if m <= 0:
                raise ValueError("La masa debe ser un valor positivo.")
            f_calc = m * a
            input_params = {'m': m, 'a': a}
            calculated_values = {'f': f_calc}

        elif m is None:
            # Calcular Masa
            if a == 0:
                raise ValueError("La aceleración no puede ser cero si se desconoce la masa.")
            m_calc = f / a
            if m_calc <= 0:
                raise ValueError("La masa calculada debe ser positiva. Verifique la dirección de la fuerza y la aceleración.")
            input_params = {'f': f, 'a': a}
            calculated_values = {'m': m_calc}

        elif a is None:
            # Calcular Aceleración
            if m <= 0:
                raise ValueError("La masa debe ser un valor positivo y no nulo.")
            a_calc = f / m
            input_params = {'f': f, 'm': m}
            calculated_values = {'a': a_calc}

        return {
            'input_params': input_params,
            'calculated_values': calculated_values,
            'equations': equations
        }

    def generate_plot_data(self, results, num_points=100):
        """
        Generar datos para graficar la relación entre las variables de la Segunda Ley de Newton.
        """
        input_params = results['input_params']
        calculated_values = results['calculated_values']
        all_params = {**input_params, **calculated_values}

        f = all_params.get('f')
        m = all_params.get('m')
        a = all_params.get('a')

        # Identificar qué se calculó para determinar las variables del gráfico
        calculated_var = list(calculated_values.keys())[0]

        if calculated_var == 'f':
            # Graficar F vs a (con m constante)
            a_max = a * 2 if a != 0 else 10
            a_values = np.linspace(0, a_max, num_points)
            f_values = m * a_values
            return {
                'x_data': a_values, 'y_data': f_values,
                'x_label': 'Aceleración (m/s²)', 'y_label': 'Fuerza (N)',
                'title': f'Fuerza vs. Aceleración (Masa = {m:.2f} kg)'
            }
        elif calculated_var == 'm':
            # Graficar F vs a (para la masa calculada)
            a_max = a * 2 if a != 0 else 10
            a_values = np.linspace(0.1, a_max, num_points) # Evitar a=0
            f_values = m * a_values
            return {
                'x_data': a_values, 'y_data': f_values,
                'x_label': 'Aceleración (m/s²)', 'y_label': 'Fuerza (N)',
                'title': f'Fuerza vs. Aceleración (Masa = {m:.2f} kg)'
            }
        elif calculated_var == 'a':
            # Graficar F vs m (con a constante)
            m_max = m * 2 if m != 0 else 10
            m_values = np.linspace(0.1, m_max, num_points) # Evitar m=0
            f_values = m_values * a
            return {
                'x_data': m_values, 'y_data': f_values,
                'x_label': 'Masa (kg)', 'y_label': 'Fuerza (N)',
                'title': f'Fuerza vs. Masa (Aceleración = {a:.2f} m/s²)'
            }
