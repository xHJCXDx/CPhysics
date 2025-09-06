"""
Panel for plotting relationships in the electromagnetism module.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import seaborn as sns
import numpy as np

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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        title = QLabel("Electromagnetism Relationships Plot")
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
        self.canvas.axes.set_title("Electromagnetism Plot", color='#ecf0f1')
        self.canvas.axes.grid(True, color='#4a627a', linestyle='--', linewidth=0.5)
        self.canvas.draw()

    def plot_results(self, results, calculator):
        """Plot Coulomb's Law: Force vs Distance using seaborn."""
        if not results:
            QMessageBox.warning(self, "Advertencia", "Primero debe realizar un cálculo")
            return

        try:
            self.canvas.axes.clear()
            
            input_params = results.get('input_params', {})
            calculated_values = results.get('calculated_values', {})
            all_values = {**input_params, **calculated_values}

            q1 = all_values.get('q1')
            q2 = all_values.get('q2')
            F_calc = all_values.get('F')
            r_calc = all_values.get('r')

            if q1 is None or q2 is None:
                QMessageBox.warning(self, "Advertencia", "Se necesitan los valores de q1 y q2 para graficar la relación F vs r.")
                return
            
            r_min_plot = 0.1
            r_max_plot = 10.0
            if r_calc is not None:
                r_min_plot = max(0.01, r_calc * 0.1)
                r_max_plot = r_calc * 2.0

            r_values = np.linspace(r_min_plot, r_max_plot, 100)
            F_values = (calculator.K * abs(q1 * q2)) / (r_values**2)

            sns.lineplot(x=r_values, y=F_values, ax=self.canvas.axes, color='#3498db', linewidth=2.5, label='Fuerza vs Distancia')
            
            if r_calc is not None and F_calc is not None:
                self.canvas.axes.plot(r_calc, F_calc, 'o', color='#e74c3c', markersize=8, label=f'Punto calculado (r={r_calc:.2f}m, F={F_calc:.2e}N)')

            self.canvas.axes.set_xlabel('Distancia (r) [m]', fontsize=12, color='#ecf0f1')
            self.canvas.axes.set_ylabel('Fuerza (F) [N]', fontsize=12, color='#ecf0f1')
            self.canvas.axes.set_title('Ley de Coulomb: Fuerza vs Distancia', fontsize=14, fontweight='bold', color='#ecf0f1')
            self.canvas.axes.grid(True, color='#4a627a', linestyle='--', linewidth=0.5)
            
            legend = self.canvas.axes.legend(fontsize=11)
            legend.get_frame().set_facecolor('#34495e')
            legend.get_frame().set_edgecolor('#4a627a')
            for text in legend.get_texts():
                text.set_color('#ecf0f1')

            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar gráfico:\n{str(e)}")

    def clear_plot(self):
        self.initialize_plot()
