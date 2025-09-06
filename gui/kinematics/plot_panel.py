from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import seaborn as sns

class MplCanvas(FigureCanvas):
    """Custom Matplotlib canvas widget to integrate with PySide6."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """Initializes the Matplotlib canvas."""
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MplCanvas, self).__init__(self.fig)
        self.setParent(parent)
        
        # Apply a dark theme to the plot.
        self.fig.patch.set_facecolor('#34495e')

class PlotPanel(QWidget):
    """Panel for plotting kinematics results."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.canvas = MplCanvas(self, width=10, height=8, dpi=100)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        title = QLabel("Kinematics Plots")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.initialize_plot()

    def initialize_plot(self):
        """Sets the initial state of the plot."""
        self.canvas.fig.clear()
        ax = self.canvas.fig.add_subplot(111)
        ax.set_facecolor('#2c3e50')
        ax.tick_params(axis='x', colors='#ecf0f1')
        ax.tick_params(axis='y', colors='#ecf0f1')
        for spine in ax.spines.values():
            spine.set_edgecolor('#ecf0f1')
        ax.set_title("Kinematics Plot", color='#ecf0f1')
        ax.grid(True, color='#4a627a', linestyle='--', linewidth=0.5)
        self.canvas.draw()

    def plot_results(self, calculator, results):
        """Plot kinematics results using seaborn."""
        self.canvas.fig.clear()
        
        plot_data = calculator.generate_plot_data(results)
        movement_type = plot_data.get('movement_type')

        if movement_type == 'parabolic':
            ax = self.canvas.fig.add_subplot(1, 1, 1)
            ax.set_facecolor('#2c3e50')
            ax.tick_params(axis='x', colors='#ecf0f1')
            ax.tick_params(axis='y', colors='#ecf0f1')
            for spine in ax.spines.values():
                spine.set_edgecolor('#ecf0f1')
            sns.lineplot(x=plot_data['position_x'], y=plot_data['position_y'], ax=ax, color='#3498db', linewidth=2.5, label='Trayectoria')
            ax.set_xlabel('Distancia (m)', fontsize=12, color='#ecf0f1')
            ax.set_ylabel('Altura (m)', fontsize=12, color='#ecf0f1')
            ax.set_title('Trayectoria del Proyectil', fontsize=14, fontweight='bold', color='#ecf0f1')
            ax.legend()
            ax.set_aspect('equal', adjustable='box')
            ax.grid(True, color='#4a627a', linestyle='--', linewidth=0.5)
            legend = ax.legend(fontsize=11)
            legend.get_frame().set_facecolor('#34495e')
            legend.get_frame().set_edgecolor('#4a627a')
            for text in legend.get_texts():
                text.set_color('#ecf0f1')

        else:
            ax1 = self.canvas.fig.add_subplot(2, 1, 1)
            ax2 = self.canvas.fig.add_subplot(2, 1, 2)
            
            for ax in [ax1, ax2]:
                ax.set_facecolor('#2c3e50')
                ax.tick_params(axis='x', colors='#ecf0f1')
                ax.tick_params(axis='y', colors='#ecf0f1')
                for spine in ax.spines.values():
                    spine.set_edgecolor('#ecf0f1')
                ax.grid(True, color='#4a627a', linestyle='--', linewidth=0.5)

            sns.lineplot(x=plot_data['time'], y=plot_data['position'], ax=ax1, color='#3498db', linewidth=2.5, label='Posición')
            ax1.set_xlabel('Tiempo (s)', fontsize=12, color='#ecf0f1')
            ax1.set_ylabel('Posición (m)', fontsize=12, color='#ecf0f1')
            ax1.set_title('Posición vs Tiempo', fontsize=14, fontweight='bold', color='#ecf0f1')
            
            legend1 = ax1.legend(fontsize=11)
            legend1.get_frame().set_facecolor('#34495e')
            legend1.get_frame().set_edgecolor('#4a627a')
            for text in legend1.get_texts():
                text.set_color('#ecf0f1')
            
            sns.lineplot(x=plot_data['time'], y=plot_data['velocity'], ax=ax2, color='#e74c3c', linewidth=2.5, label='Velocidad')
            ax2.set_xlabel('Tiempo (s)', fontsize=12, color='#ecf0f1')
            ax2.set_ylabel('Velocidad (m/s)', fontsize=12, color='#ecf0f1')
            ax2.set_title('Velocidad vs Tiempo', fontsize=14, fontweight='bold', color='#ecf0f1')

            legend2 = ax2.legend(fontsize=11)
            legend2.get_frame().set_facecolor('#34495e')
            legend2.get_frame().set_edgecolor('#4a627a')
            for text in legend2.get_texts():
                text.set_color('#ecf0f1')
        
        self.canvas.fig.tight_layout(pad=3.0)
        self.canvas.draw()

    def clear_plot(self):
        self.initialize_plot()