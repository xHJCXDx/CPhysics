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
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.figure.patch.set_facecolor('#34495e')
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

    def plot_results(self, results, calculator):
        """Plot Coulomb's Law: Force vs Distance using seaborn."""
        if not results:
            QMessageBox.warning(self, "Advertencia", "Primero debe realizar un cálculo")
            return

        try:
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

            sns.lineplot(x=r_values, y=F_values, ax=ax, color='#3498db', linewidth=2.5, label='Fuerza vs Distancia')
            
            if r_calc is not None and F_calc is not None:
                ax.plot(r_calc, F_calc, 'o', color='#e74c3c', markersize=8, label=f'Punto calculado (r={r_calc:.2f}m, F={F_calc:.2e}N)')

            ax.set_xlabel('Distancia (r) [m]', fontsize=12, color='#ecf0f1')
            ax.set_ylabel('Fuerza (F) [N]', fontsize=12, color='#ecf0f1')
            ax.set_title('Ley de Coulomb: Fuerza vs Distancia', fontsize=14, fontweight='bold', color='#ecf0f1')
            ax.legend()
            self.figure.tight_layout(pad=3.0)

            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar gráfico:\n{str(e)}")

    def clear_plot(self):
        self.figure.clear()
        self.figure.add_subplot(1, 1, 1)
        self.canvas.draw()