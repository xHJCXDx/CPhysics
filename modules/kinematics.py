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
    
    def calculate_mrua(self, params):
        """
        Calcular parámetros para Movimiento Rectilíneo Uniformemente Acelerado
        
        Ecuaciones:
        x = x0 + v0*t + (1/2)*a*t²
        v = v0 + a*t
        v² = v0² + 2*a*(x-x0)
        """
        x0 = params.get('x0') if params.get('x0') is not None else 0
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
            # Caso 1: Conocemos v0, a, t -> calcular x, v
            x_final = x0 + v0 * t + 0.5 * a * t**2
            v_final = v0 + a * t
            
            input_params = {'x0': x0, 'v0': v0, 'a': a, 't': t}
            calculated_values = {'x': x_final, 'v': v_final}
            
        elif v0 is not None and a is not None and x is not None and x0 is not None:
            # Caso 2: Conocemos v0, a, x, x0 -> calcular t, v
            # Usando: x = x0 + v0*t + (1/2)*a*t²
            # Reordenando: (1/2)*a*t² + v0*t + (x0-x) = 0
            
            A = 0.5 * a
            B = v0
            C = x0 - x
            
            if abs(a) < EPSILON:
                # Movimiento uniforme
                t_calc = (x - x0) / v0 if abs(v0) > EPSILON else 0
            else:
                # Ecuación cuadrática
                discriminant = B**2 - 4*A*C
                if discriminant < 0:
                    raise ValueError("No hay solución real para el tiempo (discriminante negativo)")
                
                t1 = (-B + np.sqrt(discriminant)) / (2*A)
                t2 = (-B - np.sqrt(discriminant)) / (2*A)
                
                # Elegir la solución de tiempo positiva más pequeña (o la única positiva)
                t_calc = t1 if t1 >= 0 else t2
                if t_calc < 0:
                    raise ValueError("No se encontró una solución de tiempo válida")
            
            v_final = v0 + a * t_calc
            
            input_params = {'x0': x0, 'v0': v0, 'a': a, 'x': x}
            calculated_values = {'t': t_calc, 'v': v_final}
            
        elif v0 is not None and v is not None and a is not None:
            # Caso 3: Conocemos v0, v, a -> calcular t, x
            t_calc = (v - v0) / a if abs(a) > EPSILON else 0
            x_final = x0 + v0 * t_calc + 0.5 * a * t_calc**2
            
            input_params = {'x0': x0, 'v0': v0, 'a': a, 'v': v}
            calculated_values = {'t': t_calc, 'x': x_final}
            
        elif v0 is not None and a is not None and v is not None and x0 is not None:
            # Caso 4: Usando v² = v0² + 2*a*(x-x0) -> calcular x, t
            delta_x = (v**2 - v0**2) / (2 * a) if abs(a) > EPSILON else 0
            x_final = x0 + delta_x
            
            t_calc = (v - v0) / a if abs(a) > EPSILON else 0
            
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