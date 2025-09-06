
import numpy as np
import seaborn as sns
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

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

        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.figure.patch.set_facecolor('#34495e')
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

    def plot(self, input_values, calculator):
        """Plot P vs T for fixed V and n using seaborn."""
        self.figure.clear()
        sns.set_theme(style="darkgrid", rc={
            "axes.facecolor": "#2c3e50", 
            "figure.facecolor": "#34495e",
            "text.color": "#ecf0f1",
            "axes.labelcolor": "#ecf0f1",
            "xtick.color": "#ecf0f1",
            "ytick.color": "#ecf0f1",
            "grid.color": "#4a627a",
        })
        ax = self.figure.add_subplot(1, 1, 1)

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

        sns.lineplot(x=T, y=P, ax=ax, color='#e74c3c', linewidth=2.5, label='P vs T (V y n fijos)')
        ax.set_xlabel("Temperatura (K)", fontsize=12, color='#ecf0f1')
        ax.set_ylabel("Presión (atm)", fontsize=12, color='#ecf0f1')
        ax.set_title("Relación P vs T (Ley de Gases Ideales)", fontsize=14, fontweight='bold', color='#ecf0f1')
        ax.legend()
        self.figure.tight_layout(pad=3.0)
        self.canvas.draw()
