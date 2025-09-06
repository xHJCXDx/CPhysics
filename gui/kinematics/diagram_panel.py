from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class DiagramPanel(QWidget):
    """Panel for displaying vector and meeting diagrams in kinematics."""
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
        title = QLabel("Vector Diagram")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addWidget(self.canvas)

    def update_diagram(self, velocity=None, acceleration=None, meeting_data=None):
        """Update diagram for vectors or meeting point."""
        self.ax.clear()
        self.ax.grid(True)
        if meeting_data:
            self._update_meeting_diagram(meeting_data)
        else:
            self._update_vector_diagram(velocity, acceleration)
        self.ax.legend()
        self.canvas.draw()

    def _update_vector_diagram(self, velocity, acceleration):
        """Draw velocity and acceleration vectors."""
        self.ax.set_xlim(-15, 15)
        self.ax.set_ylim(-15, 15)

        # Particle
        self.ax.plot(0, 0, 'o', markersize=10, color='white', label='Particle')

        # Velocity vector
        if velocity is not None:
            vx, vy = velocity
            self.ax.arrow(0, 0, vx, vy, head_width=0.5, head_length=0.7, fc='cyan', ec='cyan', label=f'Velocity ({vx}, {vy})')

        # Acceleration vector
        if acceleration is not None:
            ax, ay = acceleration
            self.ax.arrow(0, 0, ax, ay, head_width=0.5, head_length=0.7, fc='magenta', ec='magenta', label=f'Acceleration ({ax}, {ay})')

    def _update_meeting_diagram(self, meeting_data):
        """Draw diagram for meeting point between two objects."""
        obj1_params = meeting_data['input_params']['Object 1']
        obj2_params = meeting_data['input_params']['Object 2']
        results = meeting_data['calculated_values']

        x0_1 = obj1_params['x0']
        x0_2 = obj2_params['x0']
        pos_enq = results['meeting_position']

        # Determine the graph limits
        all_x = [x0_1, x0_2, pos_enq]
        x_min, x_max = min(all_x), max(all_x)
        padding = (x_max - x_min) * 0.2 if (x_max - x_min) > 0 else 5
        self.ax.set_xlim(x_min - padding, x_max + padding)
        self.ax.set_ylim(-5, 5)

        # Draw the objects and the meeting point
        self.ax.plot(x0_1, 0, 'o', markersize=10, color='royalblue', label='Object 1 (Start)')
        self.ax.plot(x0_2, 0, 's', markersize=10, color='seagreen', label='Object 2 (Start)')
        self.ax.plot(pos_enq, 0, 'X', markersize=12, color='gold', label=f'Meeting ({pos_enq:.2f} m)')

        # Trajectory lines
        self.ax.plot([x0_1, pos_enq], [0, 0], '--', color='royalblue')
        self.ax.plot([x0_2, pos_enq], [0, 0], '--', color='seagreen')
        
        # Annotations
        self.ax.text(x0_1, 0.5, f'x₀_₁={x0_1}', color='white', ha='center')
        self.ax.text(x0_2, 0.5, f'x₀_₂={x0_2}', color='white', ha='center')
        self.ax.text(pos_enq, -0.5, f't={results["meeting_time"]:.2f}s', color='gold', ha='center')


    def clear_diagram(self):
        """Clear the diagram panel."""
        self.ax.clear()
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.grid(True)
        self.canvas.draw()