"""
Módulo de cálculos de cinemática
Contiene las funciones para resolver problemas de movimiento rectilíneo
"""

import numpy as np
import math

EPSILON = 1e-9 # Pequeño valor para evitar división por cero en punto flotante

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
        x0 = params.get('x0') if params.get('x0') is not None else 0
        v0 = params.get('v0')
        t = params.get('t')
        x = params.get('x')
        
        input_params = {}
        calculated_values = {}
        equations = ["x = x₀ + v₀ × t", "v = v₀ (constante)"]
        
        # Determinar qué calcular basado en los parámetros dados
        if v0 is not None and t is not None:
            # Calcular posición final (x)
            x_final = x0 + v0 * t
            
            input_params = {'x0': x0, 'v0': v0, 't': t}
            calculated_values = {'x': x_final, 'v': v0}
            
        elif x is not None and t is not None:
            # Calcular velocidad (v0)
            v0_calc = (x - x0) / t if abs(t) > EPSILON else 0
            
            input_params = {'x0': x0, 'x': x, 't': t}
            calculated_values = {'v0': v0_calc, 'v': v0_calc}
            
        elif x is not None and v0 is not None:
            # Calcular tiempo (t)
            t_calc = (x - x0) / v0 if abs(v0) > EPSILON else 0
            
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
    
    def _calculate_x_v_from_v0_a_t(self, params):
        x0, v0, a, t = params.get('x0', 0), params['v0'], params['a'], params['t']
        x_final = x0 + v0 * t + 0.5 * a * t**2
        v_final = v0 + a * t
        return {'x': x_final, 'v': v_final}, {'x0': x0, 'v0': v0, 'a': a, 't': t}

    def _calculate_t_v_from_v0_a_x(self, params):
        x0, v0, a, x = params.get('x0', 0), params['v0'], params['a'], params['x']
        A, B, C = 0.5 * a, v0, x0 - x
        if abs(a) < EPSILON:
            t_calc = (x - x0) / v0 if abs(v0) > EPSILON else 0
        else:
            discriminant = B**2 - 4 * A * C
            if discriminant < 0:
                raise ValueError("No hay solución real para el tiempo (discriminante negativo)")
            t1, t2 = (-B + np.sqrt(discriminant)) / (2 * A), (-B - np.sqrt(discriminant)) / (2 * A)
            t_calc = t1 if t1 >= 0 else t2
            if t_calc < 0:
                raise ValueError("No se encontró una solución de tiempo válida")
        v_final = v0 + a * t_calc
        return {'t': t_calc, 'v': v_final}, {'x0': x0, 'v0': v0, 'a': a, 'x': x}

    def _calculate_t_x_from_v0_v_a(self, params):
        x0, v0, v, a = params.get('x0', 0), params['v0'], params['v'], params['a']
        t_calc = (v - v0) / a if abs(a) > EPSILON else 0
        x_final = x0 + v0 * t_calc + 0.5 * a * t_calc**2
        return {'t': t_calc, 'x': x_final}, {'x0': x0, 'v0': v0, 'a': a, 'v': v}

    def _calculate_x_t_from_v0_a_v(self, params):
        x0, v0, a, v = params.get('x0', 0), params['v0'], params['a'], params['v']
        delta_x = (v**2 - v0**2) / (2 * a) if abs(a) > EPSILON else 0
        x_final = x0 + delta_x
        t_calc = (v - v0) / a if abs(a) > EPSILON else 0
        return {'t': t_calc, 'x': x_final}, {'x0': x0, 'v0': v0, 'a': a, 'v': v}

    def calculate_mrua(self, params):
        """
        Calcular parámetros para Movimiento Rectilíneo Uniformemente Acelerado
        """
        strategies = [
            ({'v0', 'a', 't'}, self._calculate_x_v_from_v0_a_t),
            ({'v0', 'a', 'x'}, self._calculate_t_v_from_v0_a_x),
            ({'v0', 'v', 'a'}, self._calculate_t_x_from_v0_v_a),
        ]

        provided_params = {k for k, v in params.items() if v is not None}
        
        for required, func in strategies:
            if required.issubset(provided_params):
                calculated_values, input_params = func(params)
                return {
                    'input_params': input_params,
                    'calculated_values': calculated_values,
                    'equations': [
                        "x = x₀ + v₀×t + ½×a×t²",
                        "v = v₀ + a×t",
                        "v² = v₀² + 2×a×(x-x₀)"
                    ],
                    'movement_type': 'mrua'
                }
        
        # Special case for the last one as it has the same signature
        if {'v0', 'a', 'v'}.issubset(provided_params):
             calculated_values, input_params = self._calculate_x_t_from_v0_a_v(params)
             return {
                    'input_params': input_params,
                    'calculated_values': calculated_values,
                    'equations': [
                        "x = x₀ + v₀×t + ½×a×t²",
                        "v = v₀ + a×t",
                        "v² = v₀² + 2×a×(x-x₀)"
                    ],
                    'movement_type': 'mrua'
                }

        raise ValueError("Faltan parámetros para resolver el problema de MRUA")
    
    def calculate_parabolic_motion(self, params):
        """
        Calcular parámetros para Movimiento Parabólico (Tiro de Proyectil)
        
        Ecuaciones:
        y = y0 + v0y*t - (1/2)*g*t²
        x = x0 + v0x*t
        vy = v0y - g*t
        vx = v0x
        """
        v0 = params.get('v0')
        angle_deg = params.get('angle')
        x0 = params.get('x0', 0)
        y0 = params.get('y0', 0)
        g = 9.81 # Aceleración gravitacional

        if v0 is None or angle_deg is None:
            raise ValueError("La velocidad inicial y el ángulo son requeridos")

        angle_rad = math.radians(angle_deg)
        v0x = v0 * math.cos(angle_rad)
        v0y = v0 * math.sin(angle_rad)

        # Tiempo para alcanzar la altura máxima (vy = 0)
        t_max_height = v0y / g if g > EPSILON else 0
        
        # Tiempo de vuelo total (retorno a y=y0)
        # y0 = y0 + v0y*t - 0.5*g*t^2 => 0 = t * (v0y - 0.5*g*t)
        time_of_flight = (2 * v0y) / g if g > EPSILON else 0
        
        # Altura máxima (y en t_max_height)
        max_height = y0 + v0y * t_max_height - 0.5 * g * t_max_height**2
        
        # Alcance (x en time_of_flight)
        reach = x0 + v0x * time_of_flight

        input_params = {'v0': v0, 'angle': angle_deg, 'x0': x0, 'y0': y0}
        calculated_values = {
            'time_of_flight': time_of_flight,
            'max_height': max_height,
            'range': reach,
            'v0x': v0x,
            'v0y': v0y
        }
        equations = [
            "t_vuelo = (2 * v₀ * sin(θ)) / g",
            "h_max = y₀ + (v₀² * sin²(θ)) / (2 * g)",
            "R = x₀ + (v₀² * sin(2θ)) / g"
        ]

        return {
            'input_params': input_params,
            'calculated_values': calculated_values,
            'equations': equations,
            'movement_type': 'parabolic'
        }

    def calculate_meeting_point(self, params):
        """
        Calcular el punto de encuentro de dos objetos en MRUA.
        
        Resuelve la ecuación:
        x0_1 + v0_1*t + 0.5*a1*t^2 = x0_2 + v0_2*t + 0.5*a2*t^2
        
        (0.5*a1 - 0.5*a2)*t^2 + (v0_1 - v0_2)*t + (x0_1 - x0_2) = 0
        """
        obj1 = params['obj1']
        obj2 = params['obj2']

        x0_1, v0_1, a_1 = obj1.get('x0', 0), obj1.get('v0', 0), obj1.get('a', 0)
        x0_2, v0_2, a_2 = obj2.get('x0', 0), obj2.get('v0', 0), obj2.get('a', 0)

        # Coeficientes de la ecuación cuadrática At^2 + Bt + C = 0
        A = 0.5 * (a_1 - a_2)
        B = v0_1 - v0_2
        C = x0_1 - x0_2

        if abs(A) < EPSILON:
            # Ecuación lineal (movimiento con aceleración igual o similar)
            if abs(B) < EPSILON:
                if abs(C) < EPSILON:
                    # Los objetos están en la misma posición y se mueven juntos
                    raise ValueError("Los objetos tienen la misma posición y velocidad inicial (movimiento relativo cero)")
                else:
                    # Paralelos, nunca se encuentran
                    raise ValueError("Los objetos nunca se encuentran (velocidades iguales, posiciones diferentes)")
            
            t = -C / B
            if t < 0:
                raise ValueError("El encuentro ocurriría en un tiempo negativo (en el pasado)")
        else:
            # Ecuación cuadrática
            discriminant = B**2 - 4*A*C
            if discriminant < 0:
                raise ValueError("No hay solución real para el tiempo (los objetos no se encuentran)")
            
            sqrt_discriminant = np.sqrt(discriminant)
            t1 = (-B + sqrt_discriminant) / (2*A)
            t2 = (-B - sqrt_discriminant) / (2*A)
            
            # Filtrar tiempos negativos
            valid_times = [t for t in [t1, t2] if t >= 0]
            
            if not valid_times:
                raise ValueError("El encuentro ocurriría en un tiempo negativo")
            
            t = min(valid_times)

        # Calcular posición de encuentro
        position = x0_1 + v0_1 * t + 0.5 * a_1 * t**2

        input_params = {
            'Objeto 1': {'x0': x0_1, 'v0': v0_1, 'a': a_1},
            'Objeto 2': {'x0': x0_2, 'v0': v0_2, 'a': a_2}
        }
        calculated_values = {
            'tiempo_encuentro': t,
            'posicion_encuentro': position
        }
        equations = ["x₁ = x₀₁ + v₀₁t + ½a₁t²", "x₂ = x₀₂ + v₀₂t + ½a₂t²"]

        return {
            'input_params': input_params,
            'calculated_values': calculated_values,
            'equations': equations,
            'movement_type': 'meeting_point'
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
        
        if movement_type == 'parabolic':
            v0 = all_params.get('v0', 0)
            angle_deg = all_params.get('angle', 0)
            x0 = all_params.get('x0', 0)
            y0 = all_params.get('y0', 0)
            time_of_flight = all_params.get('time_of_flight', 10)
            g = 9.81

            angle_rad = math.radians(angle_deg)
            v0x = v0 * math.cos(angle_rad)
            v0y = v0 * math.sin(angle_rad)
            
            t = np.linspace(0, time_of_flight, num_points)
            x = x0 + v0x * t
            y = y0 + v0y * t - 0.5 * g * t**2
            
            return {
                'time': t,
                'position_x': x,
                'position_y': y,
                'movement_type': 'parabolic'
            }

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
            'velocity': velocity,
            'movement_type': movement_type
        }