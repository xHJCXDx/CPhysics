"""
Módulo de cálculos de cinemática
Contiene las funciones para resolver problemas de movimiento rectilíneo
"""

import numpy as np
import math

class KinematicsCalculator:
    def __init__(self):
        pass
    
    def calculate_mru(self, params):
        """
        Calcular parámetros para Movimiento Rectilíneo Uniforme
        
        Ecuaciones:
        x = x0 + v0 * t
        v = v0 (constante)
        """
        # Parámetros de entrada
        x0 = params.get('x0', 0)
        v0 = params.get('v0')
        t = params.get('t')
        x = params.get('x')
        
        input_params = {}
        calculated_values = {}
        equations = ["x = x₀ + v₀ × t", "v = v₀ (constante)"]
        
        # Determinar qué calcular basado en los parámetros dados
        if v0 is not None and t is not None:
            # Calcular posición final
            if x0 is None:
                x0 = 0
            x_final = x0 + v0 * t
            
            input_params = {'x0': x0, 'v0': v0, 't': t}
            calculated_values = {'x': x_final, 'v': v0}
            
        elif x is not None and t is not None and x0 is not None:
            # Calcular velocidad
            v0_calc = (x - x0) / t if t != 0 else 0
            
            input_params = {'x0': x0, 'x': x, 't': t}
            calculated_values = {'v0': v0_calc, 'v': v0_calc}
            
        elif x is not None and v0 is not None and x0 is not None:
            # Calcular tiempo
            t_calc = (x - x0) / v0 if v0 != 0 else 0
            
            input_params = {'x0': x0, 'v0': v0, 'x': x}
            calculated_values = {'t': t_calc, 'v': v0}
            
        else:
            raise ValueError("Faltan parámetros para resolver el problema de MRU")
        
        return {
            'input_params': input_params,
            'calculated_values': calculated_values,
            'equations': equations,
            'movement_type': 'mru'
        }
    
    def calculate_mrua(self, params):
        """
        Calcular parámetros para Movimiento Rectilíneo Uniformemente Acelerado
        
        Ecuaciones:
        x = x0 + v0*t + (1/2)*a*t²
        v = v0 + a*t
        v² = v0² + 2*a*(x-x0)
        """
        x0 = params.get('x0', 0)
        v0 = params.get('v0')
        a = params.get('a')
        t = params.get('t')
        x = params.get('x')
        v = params.get('v')
        
        input_params = {}
        calculated_values = {}
        equations = [
            "x = x₀ + v₀×t + ½×a×t²",
            "v = v₀ + a×t",
            "v² = v₀² + 2×a×(x-x₀)"
        ]
        
        # Casos más comunes de resolución
        if v0 is not None and a is not None and t is not None:
            # Caso 1: Conocemos v0, a, t
            if x0 is None:
                x0 = 0
            
            x_final = x0 + v0 * t + 0.5 * a * t**2
            v_final = v0 + a * t
            
            input_params = {'x0': x0, 'v0': v0, 'a': a, 't': t}
            calculated_values = {'x': x_final, 'v': v_final}
            
        elif v0 is not None and a is not None and x is not None and x0 is not None:
            # Caso 2: Conocemos v0, a, x, x0 -> calcular t y v
            # Usando: x = x0 + v0*t + (1/2)*a*t²
            # Reordenando: (1/2)*a*t² + v0*t + (x0-x) = 0
            
            A = 0.5 * a if a != 0 else 0
            B = v0
            C = x0 - x
            
            if a == 0:
                # Movimiento uniforme
                t_calc = (x - x0) / v0 if v0 != 0 else 0
            else:
                # Ecuación cuadrática
                discriminant = B**2 - 4*A*C
                if discriminant < 0:
                    raise ValueError("No hay solución real para los parámetros dados")
                
                t1 = (-B + math.sqrt(discriminant)) / (2*A)
                t2 = (-B - math.sqrt(discriminant)) / (2*A)
                
                # Elegir la solución positiva
                t_calc = t1 if t1 >= 0 else t2
                if t_calc < 0:
                    raise ValueError("No se encontró una solución de tiempo válida")
            
            v_final = v0 + a * t_calc
            
            input_params = {'x0': x0, 'v0': v0, 'a': a, 'x': x}
            calculated_values = {'t': t_calc, 'v': v_final}
            
        elif v0 is not None and v is not None and a is not None:
            # Caso 3: Conocemos v0, v, a -> calcular t y x
            t_calc = (v - v0) / a if a != 0 else 0
            
            if x0 is None:
                x0 = 0
            
            x_final = x0 + v0 * t_calc + 0.5 * a * t_calc**2
            
            input_params = {'x0': x0, 'v0': v0, 'a': a, 'v': v}
            calculated_values = {'t': t_calc, 'x': x_final}
            
        elif v0 is not None and a is not None and v is not None and x0 is not None:
            # Caso 4: Usando v² = v0² + 2*a*(x-x0)
            delta_x = (v**2 - v0**2) / (2 * a) if a != 0 else 0
            x_final = x0 + delta_x
            
            t_calc = (v - v0) / a if a != 0 else 0
            
            input_params = {'x0': x0, 'v0': v0, 'a': a, 'v': v}
            calculated_values = {'t': t_calc, 'x': x_final}
            
        else:
            raise ValueError("Faltan parámetros para resolver el problema de MRUA")
        
        return {
            'input_params': input_params,
            'calculated_values': calculated_values,
            'equations': equations,
            'movement_type': 'mrua'
        }
    
    def generate_plot_data(self, results, num_points=100):
        """
        Generar datos para graficar basado en los resultados del cálculo
        """
        # Obtener parámetros del resultado
        input_params = results['input_params']
        calculated_values = results['calculated_values']
        movement_type = results['movement_type']
        
        # Combinar parámetros
        all_params = {**input_params, **calculated_values}
        
        x0 = all_params.get('x0', 0)
        v0 = all_params.get('v0', 0)
        a = all_params.get('a', 0) if movement_type == 'mrua' else 0
        
        # Determinar rango de tiempo para la gráfica
        t_max = all_params.get('t', 10)
        if t_max <= 0:
            t_max = 10  # Valor por defecto
        
        # Crear array de tiempo
        time = np.linspace(0, t_max, num_points)
        
        # Calcular posición y velocidad para cada punto
        if movement_type == 'mru':
            position = x0 + v0 * time
            velocity = np.full_like(time, v0)
        else:  # mrua
            position = x0 + v0 * time + 0.5 * a * time**2
            velocity = v0 + a * time
        
        return {
            'time': time,
            'position': position,
            'velocity': velocity
        }