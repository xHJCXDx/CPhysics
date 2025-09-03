"""
Electromagnetism calculations module
Contains functions to solve problems of Coulomb's Law and electric fields.
"""

import numpy as np

class ElectromagnetismCalculator:
    # Coulomb's constant (N·m²/C²)
    K = 8.9875e9

    def __init__(self):
        pass

    def calculate_coulomb_force(self, params):
        """
        Calculates the force between two point charges using Coulomb's Law.
        F = K * |q1 * q2| / r^2

        Expected parameters:
        q1 (float): Charge of the first particle in Coulombs (C).
        q2 (float): Charge of the second particle in Coulombs (C).
        r (float): Distance between the charges in meters (m).
        """
        q1 = params.get('q1')
        q2 = params.get('q2')
        r = params.get('r')
        F = params.get('F')

        provided_params_count = sum(p is not None for p in [q1, q2, r, F])

        if provided_params_count != 3:
            raise ValueError("You must provide exactly three of the four parameters (q1, q2, r, F).")

        input_params = {}
        calculated_values = {}
        equations = [f"F = K × |q₁ × q₂| / r²  (with K = {self.K:.4e} N·m²/C²)"]

        # Validations
        if r is not None and r <= 0:
            raise ValueError("The distance (r) must be a positive value.")
        if F is not None and F < 0:
            raise ValueError("The force (F) cannot be negative in magnitude.")

        if F is None:
            # Calculate Force (F)
            if r is None or r == 0:
                raise ValueError("The distance (r) cannot be zero to calculate the force.")
            F_calc = (self.K * abs(q1 * q2)) / (r ** 2)
            input_params = {'q1': q1, 'q2': q2, 'r': r}
            calculated_values = {'F': F_calc}
        elif r is None:
            # Calculate Distance (r)
            if F is None or F == 0:
                raise ValueError("The force (F) cannot be zero to calculate the distance.")
            r_calc = np.sqrt((self.K * abs(q1 * q2)) / F)
            input_params = {'q1': q1, 'q2': q2, 'F': F}
            calculated_values = {'r': r_calc}
        elif q1 is None:
            # Calculate Charge 1 (q1)
            if r is None or r == 0:
                raise ValueError("The distance (r) cannot be zero to calculate the charge.")
            if q2 is None or q2 == 0:
                raise ValueError("Charge 2 (q2) cannot be zero to calculate charge 1.")
            q1_calc = (F * (r ** 2)) / (self.K * q2)
            input_params = {'q2': q2, 'r': r, 'F': F}
            calculated_values = {'q1': q1_calc}
        elif q2 is None:
            # Calculate Charge 2 (q2)
            if r is None or r == 0:
                raise ValueError("The distance (r) cannot be zero to calculate the charge.")
            if q1 is None or q1 == 0:
                raise ValueError("Charge 1 (q1) cannot be zero to calculate charge 2.")
            q2_calc = (F * (r ** 2)) / (self.K * q1)
            input_params = {'q1': q1, 'r': r, 'F': F}
            calculated_values = {'q2': q2_calc}

        return {
            'input_params': input_params,
            'calculated_values': calculated_values,
            'equations': equations
        }