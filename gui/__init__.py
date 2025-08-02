"""
Paquete GUI para CPHYSICS
Contiene todas las interfaces gráficas de la aplicación basadas en PySide6
"""

from .base_window import MainWindow
from .kinematics_frame import KinematicsFrame

__all__ = ['MainWindow', 'KinematicsFrame']