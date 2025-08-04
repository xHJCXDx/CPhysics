"""
Módulo de cálculos de dinámica
Contiene las funciones para resolver problemas basados en las Leyes de Newton
"""

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
