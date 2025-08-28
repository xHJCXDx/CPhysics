
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class DiagramPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.setup_ui()
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.grid(True)
        self.figure.patch.set_facecolor('#34495e')
        self.ax.set_facecolor('#2c3e50')
        self.ax.xaxis.label.set_color('#ecf0f1')
        self.ax.yaxis.label.set_color('#ecf0f1')
        self.ax.tick_params(axis='x', colors='#ecf0f1')
        self.ax.tick_params(axis='y', colors='#ecf0f1')


    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("Diagrama de Vectores")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title)
        layout.addWidget(self.canvas)

    def update_diagram(self, velocity, acceleration):
        self.ax.clear()
        self.ax.set_xlim(-15, 15)
        self.ax.set_ylim(-15, 15)
        self.ax.grid(True)

        # Particle
        self.ax.plot(0, 0, 'o', markersize=10, color='white', label='Partícula')

        # Velocity vector
        if velocity is not None:
            vx, vy = velocity
            self.ax.arrow(0, 0, vx, vy, head_width=0.5, head_length=0.7, fc='cyan', ec='cyan', label=f'Velocidad ({vx}, {vy})')

        # Acceleration vector
        if acceleration is not None:
            ax, ay = acceleration
            self.ax.arrow(0, 0, ax, ay, head_width=0.5, head_length=0.7, fc='magenta', ec='magenta', label=f'Aceleración ({ax}, {ay})')

        self.ax.legend()
        self.canvas.draw()

    def clear_diagram(self):
        self.ax.clear()
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.grid(True)
        self.canvas.draw()
