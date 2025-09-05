"""
Waves calculations module.

Provides the WavesCalculator class to solve problems related to the properties
of traveling waves.
"""

import numpy as np

class WavesCalculator:
    """Performs calculations related to the properties of traveling waves."""

    def calculate_wave_properties(self, params: dict) -> dict:
        """
        Calculates missing wave properties from the given parameters.

        The core relationship used is v = f * λ. Other properties like
        period (T), angular frequency (ω), and wave number (k) are
        derived from the primary properties.

        Args:
            params (dict): A dictionary with known wave properties.
                           Requires at least two of: 'velocity', 'frequency', 'wavelength'.
                           Can also include 'amplitude' and 'phase'.

        Returns:
            dict: A dictionary containing input parameters, calculated values,
                  all combined values, and the equations used.
        """
        p_in = {k: v for k, v in params.items() if v is not None}
        p_calc = {}
        equations = []

        # --- Primary Calculation: v = f * λ ---
        if params.get('velocity') is None and params.get('frequency') is not None and params.get('wavelength') is not None:
            p_calc['velocity'] = params['frequency'] * params['wavelength']
            equations.append("v = f × λ")
        elif params.get('frequency') is None and params.get('velocity') is not None and params.get('wavelength') is not None:
            if params['wavelength'] == 0:
                raise ValueError("Wavelength cannot be zero.")
            p_calc['frequency'] = params['velocity'] / params['wavelength']
            equations.append("f = v / λ")
        elif params.get('wavelength') is None and params.get('velocity') is not None and params.get('frequency') is not None:
            if params['frequency'] == 0:
                raise ValueError("Frequency cannot be zero.")
            p_calc['wavelength'] = params['velocity'] / params['frequency']
            equations.append("λ = v / f")

        # --- Secondary Calculations (derived properties) ---
        all_params = {**params, **p_calc}

        if all_params.get('frequency') is not None:
            p_calc['angular_frequency'] = 2 * np.pi * all_params['frequency']
            equations.append("ω = 2π × f")
            if all_params['frequency'] != 0:
                p_calc['period'] = 1 / all_params['frequency']
                equations.append("T = 1 / f")

        if all_params.get('wavelength') is not None and all_params['wavelength'] != 0:
            p_calc['wave_number'] = 2 * np.pi / all_params['wavelength']
            equations.append("k = 2π / λ")

        if not p_calc:
            raise ValueError("Insufficient data. At least two of the following are required: frequency, wavelength, velocity.")

        return {
            'input_params': p_in,
            'calculated_values': p_calc,
            'all_values': {**all_params, **p_calc},
            'equations': list(dict.fromkeys(equations)),  # Remove duplicate equations
        }
