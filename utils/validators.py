"""
Utilidades para validación de entradas y conversión de unidades
"""

import re
import math

class InputValidator:
    def __init__(self):
        # Patrón para números (enteros, decimales, negativos, notación científica)
        self.number_pattern = re.compile(r'^[-+]?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?$')
    
    def is_valid_number(self, value):
        """
        Validar si una cadena representa un número válido
        """
        if not isinstance(value, str):
            return False
        
        value = value.strip()
        if not value:
            return False
        
        return bool(self.number_pattern.match(value))
    
    def sanitize_number(self, value):
        """
        Limpiar y convertir una cadena a número
        """
        if not self.is_valid_number(value):
            raise ValueError(f"'{value}' no es un número válido")
        
        return float(value.strip())
    
    def validate_positive(self, value, allow_zero=True):
        """
        Validar que un número sea positivo
        """
        num = self.sanitize_number(value) if isinstance(value, str) else value
        
        if allow_zero:
            return num >= 0
        else:
            return num > 0
    
    def validate_range(self, value, min_val=None, max_val=None):
        """
        Validar que un número esté dentro de un rango
        """
        num = self.sanitize_number(value) if isinstance(value, str) else value
        
        if min_val is not None and num < min_val:
            return False
        
        if max_val is not None and num > max_val:
            return False
        
        return True

class UnitConverter:
    """
    Conversor de unidades para diferentes magnitudes físicas
    """
    
    def __init__(self):
        # Factores de conversión a unidades base (SI)
        self.length_conversions = {
            'm': 1.0,           # metro (base)
            'cm': 0.01,         # centímetro
            'mm': 0.001,        # milímetro
            'km': 1000.0,       # kilómetro
            'in': 0.0254,       # pulgada
            'ft': 0.3048,       # pie
            'yd': 0.9144,       # yarda
            'mi': 1609.344      # milla
        }
        
        self.time_conversions = {
            's': 1.0,           # segundo (base)
            'min': 60.0,        # minuto
            'h': 3600.0,        # hora
            'ms': 0.001,        # milisegundo
            'μs': 1e-6,         # microsegundo
            'ns': 1e-9          # nanosegundo
        }
        
        self.velocity_conversions = {
            'm/s': 1.0,         # metros por segundo (base)
            'km/h': 1/3.6,      # kilómetros por hora
            'mph': 0.44704,     # millas por hora
            'ft/s': 0.3048,     # pies por segundo
            'knot': 0.514444    # nudos
        }
        
        self.acceleration_conversions = {
            'm/s²': 1.0,        # metros por segundo cuadrado (base)
            'km/h²': 1/12960,   # kilómetros por hora cuadrado
            'ft/s²': 0.3048,    # pies por segundo cuadrado
            'g': 9.80665        # aceleración gravitacional estándar
        }
    
    def convert_length(self, value, from_unit, to_unit):
        """Convertir unidades de longitud"""
        if from_unit not in self.length_conversions:
            raise ValueError(f"Unidad de origen '{from_unit}' no reconocida")
        if to_unit not in self.length_conversions:
            raise ValueError(f"Unidad de destino '{to_unit}' no reconocida")
        
        # Convertir a metros primero, luego a la unidad destino
        meters = value * self.length_conversions[from_unit]
        result = meters / self.length_conversions[to_unit]
        return result
    
    def convert_time(self, value, from_unit, to_unit):
        """Convertir unidades de tiempo"""
        if from_unit not in self.time_conversions:
            raise ValueError(f"Unidad de origen '{from_unit}' no reconocida")
        if to_unit not in self.time_conversions:
            raise ValueError(f"Unidad de destino '{to_unit}' no reconocida")
        
        # Convertir a segundos primero, luego a la unidad destino
        seconds = value * self.time_conversions[from_unit]
        result = seconds / self.time_conversions[to_unit]
        return result
    
    def convert_velocity(self, value, from_unit, to_unit):
        """Convertir unidades de velocidad"""
        if from_unit not in self.velocity_conversions:
            raise ValueError(f"Unidad de origen '{from_unit}' no reconocida")
        if to_unit not in self.velocity_conversions:
            raise ValueError(f"Unidad de destino '{to_unit}' no reconocida")
        
        # Convertir a m/s primero, luego a la unidad destino
        ms = value * self.velocity_conversions[from_unit]
        result = ms / self.velocity_conversions[to_unit]
        return result
    
    def convert_acceleration(self, value, from_unit, to_unit):
        """Convertir unidades de aceleración"""
        if from_unit not in self.acceleration_conversions:
            raise ValueError(f"Unidad de origen '{from_unit}' no reconocida")
        if to_unit not in self.acceleration_conversions:
            raise ValueError(f"Unidad de destino '{to_unit}' no reconocida")
        
        # Convertir a m/s² primero, luego a la unidad destino
        ms2 = value * self.acceleration_conversions[from_unit]
        result = ms2 / self.acceleration_conversions[to_unit]
        return result
    
    def get_available_units(self, magnitude_type):
        """Obtener lista de unidades disponibles para un tipo de magnitud"""
        conversions_map = {
            'length': self.length_conversions,
            'time': self.time_conversions,
            'velocity': self.velocity_conversions,
            'acceleration': self.acceleration_conversions
        }
        
        if magnitude_type not in conversions_map:
            raise ValueError(f"Tipo de magnitud '{magnitude_type}' no reconocido")
        
        return list(conversions_map[magnitude_type].keys())

class PhysicsFormatter:
    """
    Formateador para mostrar resultados físicos con la precisión apropiada
    """
    
    def __init__(self):
        pass
    
    def format_number(self, value, precision=3, scientific_threshold=1e6):
        """
        Formatear un número con la precisión apropiada
        """
        if abs(value) >= scientific_threshold or (abs(value) < 1e-3 and value != 0):
            return f"{value:.{precision}e}"
        else:
            return f"{value:.{precision}f}".rstrip('0').rstrip('.')
    
    def format_with_units(self, value, unit, precision=3):
        """
        Formatear un número con sus unidades
        """
        formatted_value = self.format_number(value, precision)
        return f"{formatted_value} {unit}"
    
    def format_equation(self, equation_parts):
        """
        Formatear una ecuación física con valores
        """
        # Implementar formateo de ecuaciones con valores sustituidos
        pass
    
    def format_vector(self, components, labels=None):
        """
        Formatear un vector con sus componentes
        """
        if labels is None:
            labels = ['x', 'y', 'z'][:len(components)]
        
        formatted_components = []
        for i, (comp, label) in enumerate(zip(components, labels)):
            formatted_components.append(f"{label}: {self.format_number(comp)}")
        
        return f"({', '.join(formatted_components)})"