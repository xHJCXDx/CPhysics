"""
Paquete de módulos de cálculo para CPHYSICS
Contiene las funciones de cálculo para diferentes áreas de la física
"""

from .kinematics import KinematicsCalculator
from .dynamics import DynamicsCalculator

__all__ = ['KinematicsCalculator', 'DynamicsCalculator']