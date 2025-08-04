"""
Módulo de cálculos de termodinámica
Contiene las funciones para resolver problemas de la Ley de los Gases Ideales
"""

class ThermodynamicsCalculator:
    # Constante de los gases ideales (L·atm)/(mol·K)
    R = 0.0821

    def __init__(self):
        pass

    def calculate_ideal_gas_law(self, params):
        """
        Calcular parámetros para la Ley de los Gases Ideales (PV = nRT)

        Se deben proporcionar exactamente tres de los cuatro parámetros:
        P (presión), V (volumen), n (moles), T (temperatura)
        """
        P = params.get('P')
        V = params.get('V')
        n = params.get('n')
        T = params.get('T')

        provided_params_count = sum(p is not None for p in [P, V, n, T])

        if provided_params_count != 3:
            raise ValueError("Debe proporcionar exactamente tres de los cuatro parámetros (P, V, n, T).")

        input_params = {}
        calculated_values = {}
        equations = [f"PV = nRT  (con R = {self.R} L·atm/mol·K)"]

        # Validaciones comunes
        if T is not None and T <= 0:
            raise ValueError("La temperatura (T) debe ser un valor positivo en Kelvin.")
        if V is not None and V <= 0:
            raise ValueError("El volumen (V) debe ser un valor positivo.")
        if n is not None and n <= 0:
            raise ValueError("El número de moles (n) debe ser un valor positivo.")

        if P is None:
            # Calcular Presión (P)
            P_calc = (n * self.R * T) / V
            input_params = {'V': V, 'n': n, 'T': T}
            calculated_values = {'P': P_calc}
        elif V is None:
            # Calcular Volumen (V)
            V_calc = (n * self.R * T) / P
            input_params = {'P': P, 'n': n, 'T': T}
            calculated_values = {'V': V_calc}
        elif n is None:
            # Calcular Moles (n)
            n_calc = (P * V) / (self.R * T)
            input_params = {'P': P, 'V': V, 'T': T}
            calculated_values = {'n': n_calc}
        elif T is None:
            # Calcular Temperatura (T)
            T_calc = (P * V) / (n * self.R)
            input_params = {'P': P, 'V': V, 'n': n}
            calculated_values = {'T': T_calc}

        return {
            'input_params': input_params,
            'calculated_values': calculated_values,
            'equations': equations
        }