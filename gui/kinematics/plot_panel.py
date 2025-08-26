from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import seaborn as sns

class PlotPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(10, 8), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        title = QLabel("Gráficos")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.figure.patch.set_facecolor('#34495e')
        
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

    def plot_results(self, calculator, results):
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
        
        plot_data = calculator.generate_plot_data(results)
        movement_type = plot_data.get('movement_type')

        if movement_type == 'parabolic':
            ax = self.figure.add_subplot(1, 1, 1)
            sns.lineplot(x=plot_data['position_x'], y=plot_data['position_y'], ax=ax, color='#3498db', linewidth=2.5, label='Trayectoria')
            ax.set_xlabel('Distancia (m)', fontsize=12, color='#ecf0f1')
            ax.set_ylabel('Altura (m)', fontsize=12, color='#ecf0f1')
            ax.set_title('Trayectoria del Proyectil', fontsize=14, fontweight='bold', color='#ecf0f1')
            ax.legend()
            ax.set_aspect('equal', adjustable='box')

        else:
            ax1 = self.figure.add_subplot(2, 1, 1)
            ax2 = self.figure.add_subplot(2, 1, 2)
            
            sns.lineplot(x=plot_data['time'], y=plot_data['position'], ax=ax1, color='#3498db', linewidth=2.5, label='Posición')
            ax1.set_xlabel('Tiempo (s)', fontsize=12, color='#ecf0f1')
            ax1.set_ylabel('Posición (m)', fontsize=12, color='#ecf0f1')
            ax1.set_title('Posición vs Tiempo', fontsize=14, fontweight='bold', color='#ecf0f1')
            ax1.legend()
            
            sns.lineplot(x=plot_data['time'], y=plot_data['velocity'], ax=ax2, color='#e74c3c', linewidth=2.5, label='Velocidad')
            ax2.set_xlabel('Tiempo (s)', fontsize=12, color='#ecf0f1')
            ax2.set_ylabel('Velocidad (m/s)', fontsize=12, color='#ecf0f1')
            ax2.set_title('Velocidad vs Tiempo', fontsize=14, fontweight='bold', color='#ecf0f1')
            ax2.legend()
        
        self.figure.tight_layout(pad=3.0)
        self.canvas.draw()

    def clear_plot(self):
        self.figure.clear()
        if hasattr(self, 'ax1') and hasattr(self, 'ax2'):
            self.ax1.clear()
            self.ax2.clear()
        else:
            ax = self.figure.add_subplot(1, 1, 1)
            ax.clear()
        self.canvas.draw()