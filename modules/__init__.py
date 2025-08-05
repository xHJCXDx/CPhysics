"""
Paquete de Módulos para CPHYSICS
Contiene la lógica de cálculo para los diferentes dominios de la física.
"""

from .kinematics import KinematicsCalculator
from .dynamics import DynamicsCalculator
from .thermodynamics import ThermodynamicsCalculator
from .waves import WavesCalculator

__all__ = [
    'KinematicsCalculator', 'DynamicsCalculator', 
    'ThermodynamicsCalculator', 'WavesCalculator'
]