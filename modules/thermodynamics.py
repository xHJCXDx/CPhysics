"""
Thermodynamics calculations module for Ideal Gas Law.
"""

class ThermodynamicsCalculator:
    """Class for Ideal Gas Law calculations."""

    # Ideal gas constant in (L·atm)/(mol·K)
    R = 0.0821

    def __init__(self):
        pass

    def calculate_ideal_gas_law(self, params):
        """
        Calculate one parameter for the Ideal Gas Law (PV = nRT).
        params: dict with three known values among 'P', 'V', 'n', 'T'.
        Returns: dict with calculated value and used equation.
        """
        P = params.get('P')
        V = params.get('V')
        n = params.get('n')
        T = params.get('T')

        if sum(p is not None for p in [P, V, n, T]) != 3:
            raise ValueError("Exactly three of the four parameters (P, V, n, T) are required.")

        input_params = {}
        calculated_values = {}
        equations = [f"PV = nRT  (R = {self.R} L·atm/mol·K)"]

        # Input validation
        if T is not None and T <= 0:
            raise ValueError("Temperature (T) must be a positive value in Kelvin.")
        if V is not None and V <= 0:
            raise ValueError("Volume (V) must be a positive value.")
        if n is not None and n <= 0:
            raise ValueError("Number of moles (n) must be a positive value.")
        if P is not None and P <= 0:
            raise ValueError("Pressure (P) must be a positive value.")

        if P is None:
            # Calculate Pressure (P)
            P_calc = (n * self.R * T) / V
            input_params = {'V': V, 'n': n, 'T': T}
            calculated_values = {'P': P_calc}
        elif V is None:
            # Calculate Volume (V)
            V_calc = (n * self.R * T) / P
            input_params = {'P': P, 'n': n, 'T': T}
            calculated_values = {'V': V_calc}
        elif n is None:
            # Calculate Moles (n)
            n_calc = (P * V) / (self.R * T)
            input_params = {'P': P, 'V': V, 'T': T}
            calculated_values = {'n': n_calc}
        elif T is None:
            # Calculate Temperature (T)
            T_calc = (P * V) / (n * self.R)
            input_params = {'P': P, 'V': V, 'n': n}
            calculated_values = {'T': T_calc}

        return {
            'input_params': input_params,
            'calculated_values': calculated_values,
            'equations': equations
        }
