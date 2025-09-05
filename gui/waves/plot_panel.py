"""
Module for the Plot Panel of the Waves module.

This module defines the panel responsible for plotting the wave form.
"""

import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import seaborn as sns

class MplCanvas(FigureCanvas):
    """Custom Matplotlib canvas widget to integrate with PySide6."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """Initializes the Matplotlib canvas."""
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        self.setParent(parent)
        
        # Apply a dark theme to the plot.
        fig.patch.set_facecolor('#34495e')
        self.axes.set_facecolor('#2c3e50')
        self.axes.tick_params(axis='x', colors='#ecf0f1')
        self.axes.tick_params(axis='y', colors='#ecf0f1')
        for spine in self.axes.spines.values():
            spine.set_edgecolor('#ecf0f1')

class PlotPanel(QWidget):
    """A widget panel to display the wave graph."""
    def __init__(self, parent=None):
        """Initializes the PlotPanel and sets up the UI."""
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Sets up the graphical user interface for the plot panel."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        title = QLabel("Waveform Graph")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        toolbar = NavigationToolbar(self.canvas, self)

        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        self.initialize_plot()

    def initialize_plot(self):
        """Sets the initial state of the plot."""
        self.canvas.axes.clear()
        self.canvas.axes.set_title("Wave Plot", color='#ecf0f1')
        self.canvas.axes.grid(True, color='#4a627a', linestyle='--', linewidth=0.5)
        self.canvas.draw()

    def plot_wave_profile(self, wave_properties):
        """
        Generates and displays a plot of the wave.

        Args:
            wave_properties (dict): A dictionary containing the calculated wave properties.
        """
        self.canvas.axes.clear()

        vals = wave_properties.get('all_values', {})
        A = vals.get('amplitude')
        wavelength = vals.get('wavelength')
        k = vals.get('wave_number')
        phi = vals.get('phase', 0)

        if not all(v is not None for v in [A, wavelength, k]):
            raise ValueError("Amplitude, Wavelength, and Wave Number are required to plot.")

        x = np.linspace(0, 2 * wavelength, 500)
        y = A * np.cos(k * x + phi)

        sns.lineplot(x=x, y=y, ax=self.canvas.axes, color='#3498db', linewidth=2.5, label='Wave at t=0')
        self.canvas.axes.set_xlabel('Position (x) [m]', fontsize=12, color='#ecf0f1')
        self.canvas.axes.set_ylabel('Amplitude (y) [m]', fontsize=12, color='#ecf0f1')
        self.canvas.axes.set_title('Wave Profile (y vs x)', fontsize=14, fontweight='bold', color='#ecf0f1')
        self.canvas.axes.grid(True, color='#4a627a', linestyle='--', linewidth=0.5)
        self.canvas.axes.axhline(0, color='#7f8c8d', linewidth=0.8)
        
        legend = self.canvas.axes.legend(fontsize=11)
        legend.get_frame().set_facecolor('#34495e')
        legend.get_frame().set_edgecolor('#4a627a')
        for text in legend.get_texts():
            text.set_color('#ecf0f1')

        self.canvas.draw()

    def clear_plot(self):
        """Clears the plot and resets it to its initial state."""
        self.initialize_plot()
