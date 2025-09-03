"""
GUI package for CPHYSICS
Contains all the graphical interfaces of the application based on PySide6
"""

from .base_window import MainWindow
from .kinematics_frame import KinematicsFrame
from .dynamics_frame import DynamicsFrame
from .thermodynamics_frame import ThermodynamicsFrame
from .electromagnetism_frame import ElectromagnetismFrame
from .waves_frame import WavesFrame

__all__ = ['MainWindow', 'KinematicsFrame', 'DynamicsFrame', 'ThermodynamicsFrame', 'WavesFrame', 'ElectromagnetismFrame']
