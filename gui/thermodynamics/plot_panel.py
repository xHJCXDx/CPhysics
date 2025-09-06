import numpy as np
import seaborn as sns
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

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
    """Panel for plotting thermodynamics relationships."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        title = QLabel("Thermodynamics Relationships Plot")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.canvas = MplCanvas(self, width=8, height=6, dpi=100)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.initialize_plot()

    def initialize_plot(self):
        """Sets the initial state of the plot."""
        self.canvas.axes.clear()
        self.canvas.axes.set_title("Thermodynamics Plot", color='#ecf0f1')
        self.canvas.axes.grid(True, color='#4a627a', linestyle='--', linewidth=0.5)
        self.canvas.draw()

    def plot(self, input_values, calculator):
        """Plot P vs T for fixed V and n using seaborn."""
        self.canvas.axes.clear()

        V = input_values.get('V')
        n = input_values.get('n')

        try:
            V = float(V) if V else 1.0
            n = float(n) if n else 1.0
        except (ValueError, TypeError):
            V = 1.0
            n = 1.0

        T = np.linspace(200, 600, 100)
        P = (n * calculator.R * T) / V

        sns.lineplot(x=T, y=P, ax=self.canvas.axes, color='#e74c3c', linewidth=2.5, label='P vs T (V y n fijos)')
        self.canvas.axes.set_xlabel("Temperatura (K)", fontsize=12, color='#ecf0f1')
        self.canvas.axes.set_ylabel("Presión (atm)", fontsize=12, color='#ecf0f1')
        self.canvas.axes.set_title("Relación P vs T (Ley de Gases Ideales)", fontsize=14, fontweight='bold', color='#ecf0f1')
        self.canvas.axes.grid(True, color='#4a627a', linestyle='--', linewidth=0.5)
        
        legend = self.canvas.axes.legend(fontsize=11)
        legend.get_frame().set_facecolor('#34495e')
        legend.get_frame().set_edgecolor('#4a627a')
        for text in legend.get_texts():
            text.set_color('#ecf0f1')
            
        self.canvas.draw()

    def clear_plot(self):
        self.initialize_plot()