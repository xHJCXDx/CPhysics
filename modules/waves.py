import numpy as np

class WavesCalculator:
    """
    Realiza cálculos relacionados con las propiedades de las ondas viajeras.
    """
    def calculate_wave_properties(self, params: dict) -> dict:
        """
        Calcula las propiedades de onda faltantes a partir de los parámetros dados.

        Args:
            params (dict): Un diccionario con las propiedades conocidas de la onda.
                            Puede contener 'amplitude', 'frequency', 'wavelength', 'velocity', 'phase'.

        Returns:
            dict: Un diccionario con los parámetros de entrada, los valores calculados,
                    los valores combinados y las ecuaciones utilizadas.
        """
        p_in = {k: v for k, v in params.items() if v is not None}
        p_calc = {}
        equations = []

        # Lógica de cálculo principal: v = f * λ
        if params.get('velocity') is None and params.get('frequency') is not None and params.get('wavelength') is not None:
            p_calc['velocity'] = params['frequency'] * params['wavelength']
            equations.append("v = f × λ")
        elif params.get('frequency') is None and params.get('velocity') is not None and params.get('wavelength') is not None:
            if params['wavelength'] == 0:
                raise ValueError("La longitud de onda no puede ser cero.")
            p_calc['frequency'] = params['velocity'] / params['wavelength']
            equations.append("f = v / λ")
        elif params.get('wavelength') is None and params.get('velocity') is not None and params.get('frequency') is not None:
            if params['frequency'] == 0:
                raise ValueError("La frecuencia no puede ser cero.")
            p_calc['wavelength'] = params['velocity'] / params['frequency']
            equations.append("λ = v / f")

        all_params = {**params, **p_calc}

        if all_params.get('frequency') is not None:
            p_calc['angular_frequency'] = 2 * np.pi * all_params['frequency']
            if all_params['frequency'] != 0:
                p_calc['period'] = 1 / all_params['frequency']
                equations.append("T = 1 / f")
            equations.append("ω = 2π × f")

        if all_params.get('wavelength') is not None and all_params['wavelength'] != 0:
            p_calc['wave_number'] = 2 * np.pi / all_params['wavelength']
            equations.append("k = 2π / λ")

        if not p_calc:
            raise ValueError("Datos insuficientes. Se requieren al menos dos de: frecuencia, longitud de onda, velocidad.")

        return {
            'input_params': p_in,
            'calculated_values': p_calc,
            'all_values': {**all_params, **p_calc},
            'equations': list(dict.fromkeys(equations)),
        }