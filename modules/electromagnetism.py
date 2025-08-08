"""
Módulo de cálculos de electromagnetismo
Contiene las funciones para resolver problemas de la Ley de Coulomb y campos eléctricos.
"""

import numpy as np

class ElectromagnetismCalculator:
    # Constante de Coulomb (N·m²/C²)
    K = 8.9875e9

    def __init__(self):
        pass

    def calculate_coulomb_force(self, params):
        """
        Calcula la fuerza entre dos cargas puntuales usando la Ley de Coulomb.
        F = K * |q1 * q2| / r^2

        Parámetros esperados:
        q1 (float): Carga de la primera partícula en Coulombs (C).
        q2 (float): Carga de la segunda partícula en Coulombs (C).
        r (float): Distancia entre las cargas en metros (m).
        """
        q1 = params.get('q1')
        q2 = params.get('q2')
        r = params.get('r')
        F = params.get('F')

        provided_params_count = sum(p is not None for p in [q1, q2, r, F])

        if provided_params_count != 3:
            raise ValueError("Debe proporcionar exactamente tres de los cuatro parámetros (q1, q2, r, F).")

        input_params = {}
        calculated_values = {}
        equations = [f"F = K × |q₁ × q₂| / r²  (con K = {self.K:.4e} N·m²/C²)"]

        # Validaciones
        if r is not None and r <= 0:
            raise ValueError("La distancia (r) debe ser un valor positivo.")
        if F is not None and F < 0:
            raise ValueError("La fuerza (F) no puede ser negativa en magnitud.")

        if F is None:
            # Calcular Fuerza (F)
            if r is None or r == 0:
                raise ValueError("La distancia (r) no puede ser nula para calcular la fuerza.")
            F_calc = (self.K * abs(q1 * q2)) / (r ** 2)
            input_params = {'q1': q1, 'q2': q2, 'r': r}
            calculated_values = {'F': F_calc}
        elif r is None:
            # Calcular Distancia (r)
            if F is None or F == 0:
                raise ValueError("La fuerza (F) no puede ser nula para calcular la distancia.")
            r_calc = np.sqrt((self.K * abs(q1 * q2)) / F)
            input_params = {'q1': q1, 'q2': q2, 'F': F}
            calculated_values = {'r': r_calc}
        elif q1 is None:
            # Calcular Carga 1 (q1)
            if r is None or r == 0:
                raise ValueError("La distancia (r) no puede ser nula para calcular la carga.")
            if q2 is None or q2 == 0:
                raise ValueError("La carga 2 (q2) no puede ser nula para calcular la carga 1.")
            q1_calc = (F * (r ** 2)) / (self.K * q2)
            input_params = {'q2': q2, 'r': r, 'F': F}
            calculated_values = {'q1': q1_calc}
        elif q2 is None:
            # Calcular Carga 2 (q2)
            if r is None or r == 0:
                raise ValueError("La distancia (r) no puede ser nula para calcular la carga.")
            if q1 is None or q1 == 0:
                raise ValueError("La carga 1 (q1) no puede ser nula para calcular la carga 2.")
            q2_calc = (F * (r ** 2)) / (self.K * q1)
            input_params = {'q1': q1, 'r': r, 'F': F}
            calculated_values = {'q2': q2_calc}

        return {
            'input_params': input_params,
            'calculated_values': calculated_values,
            'equations': equations
        }