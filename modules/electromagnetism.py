"""
Electromagnetism calculations module.

Provides the ElectromagnetismCalculator class to solve problems related to
Coulomb's Law and electric fields.
"""

import numpy as np

class ElectromagnetismCalculator:
    """Performs electromagnetism calculations."""

    # Coulomb's constant (N·m²/C²)
    K = 8.9875e9

    def __init__(self):
        pass

    def calculate_coulomb_force(self, params):
        """
        Calculates a parameter for Coulomb's Law.

        F = K * |q1 * q2| / r^2

        Args:
            params (dict): A dictionary containing three of the four parameters:
                           'q1' (charge 1), 'q2' (charge 2), 'r' (distance), 'F' (force).

        Returns:
            dict: A dictionary containing the calculated value, input parameters,
                  and relevant equations.
        """
        q1 = params.get('q1')
        q2 = params.get('q2')
        r = params.get('r')
        F = params.get('F')

        if sum(p is not None for p in [q1, q2, r, F]) != 3:
            raise ValueError("Exactly three of the four parameters (q1, q2, r, F) are required.")

        input_params = {}
        calculated_values = {}
        equations = [f"F = K × |q₁ × q₂| / r²  (K = {self.K:.4e} N·m²/C²)"]

        # Input validation
        if r is not None and r <= 0:
            raise ValueError("Distance (r) must be a positive value.")
        if F is not None and F < 0:
            raise ValueError("Force magnitude (F) cannot be negative.")

        if F is None:
            # Calculate Force (F)
            if r == 0:
                raise ValueError("Distance (r) cannot be zero for force calculation.")
            F_calc = (self.K * abs(q1 * q2)) / (r ** 2)
            input_params = {'q1': q1, 'q2': q2, 'r': r}
            calculated_values = {'F': F_calc}
        elif r is None:
            # Calculate Distance (r)
            if F == 0:
                raise ValueError("Force (F) cannot be zero for distance calculation.")
            r_calc = np.sqrt((self.K * abs(q1 * q2)) / F)
            input_params = {'q1': q1, 'q2': q2, 'F': F}
            calculated_values = {'r': r_calc}
        elif q1 is None:
            # Calculate Charge 1 (q1)
            if r == 0:
                raise ValueError("Distance (r) cannot be zero for charge calculation.")
            if q2 == 0:
                raise ValueError("Charge 2 (q2) cannot be zero for charge 1 calculation.")
            q1_calc = (F * (r ** 2)) / (self.K * q2)
            input_params = {'q2': q2, 'r': r, 'F': F}
            calculated_values = {'q1': q1_calc}
        elif q2 is None:
            # Calculate Charge 2 (q2)
            if r == 0:
                raise ValueError("Distance (r) cannot be zero for charge calculation.")
            if q1 == 0:
                raise ValueError("Charge 1 (q1) cannot be zero for charge 2 calculation.")
            q2_calc = (F * (r ** 2)) / (self.K * q1)
            input_params = {'q1': q1, 'r': r, 'F': F}
            calculated_values = {'q2': q2_calc}

        return {
            'input_params': input_params,
            'calculated_values': calculated_values,
            'equations': equations
        }
