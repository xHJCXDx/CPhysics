"""
Interfaz gráfica para el módulo de cinemática
Permite calcular y visualizar problemas de movimiento
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from modules.kinematics import KinematicsCalculator
from utils.validators import InputValidator

class KinematicsFrame:
    def __init__(self, parent):
        self.parent = parent
        self.calculator = KinematicsCalculator()
        self.validator = InputValidator()
        
        # Variables para almacenar resultados
        self.results = {}
        
        # Crear la interfaz
        self.create_widgets()
    
    def create_widgets(self):
        """Crear todos los widgets de la interfaz de cinemática"""
        # Frame principal con scroll
        canvas = tk.Canvas(self.parent)
        scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scroll components
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Título del módulo
        title = ttk.Label(scrollable_frame, 
                            text="Cinemática - Movimiento Rectilíneo",
                            style='Subtitle.TLabel')
        title.pack(pady=(0, 20))
        
        # Frame principal dividido en dos columnas
        main_container = ttk.Frame(scrollable_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Columna izquierda: Controles
        left_frame = ttk.Frame(main_container)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Columna derecha: Gráfico
        right_frame = ttk.Frame(main_container)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Crear controles en la columna izquierda
        self.create_input_controls(left_frame)
        
        # Crear gráfico en la columna derecha
        self.create_plot_area(right_frame)
    
    def create_input_controls(self, parent):
        """Crear controles de entrada de datos"""
        # Sección de tipo de movimiento
        movement_section = ttk.LabelFrame(parent, text="Tipo de Movimiento", padding=10)
        movement_section.pack(fill=tk.X, pady=(0, 15))
        
        self.movement_type = tk.StringVar(value="uniform")
        ttk.Radiobutton(movement_section, text="Movimiento Rectilíneo Uniforme (MRU)", 
                        variable=self.movement_type, value="uniform",
                        command=self.on_movement_type_change).pack(anchor=tk.W)
        ttk.Radiobutton(movement_section, text="Movimiento Rectilíneo Uniformemente Acelerado (MRUA)", 
                        variable=self.movement_type, value="accelerated",
                        command=self.on_movement_type_change).pack(anchor=tk.W)
        
        # Sección de parámetros
        params_section = ttk.LabelFrame(parent, text="Parámetros", padding=10)
        params_section.pack(fill=tk.X, pady=(0, 15))
        
        # Variables de entrada
        self.vars = {
            'x0': tk.StringVar(),
            'v0': tk.StringVar(),
            'a': tk.StringVar(),
            't': tk.StringVar(),
            'x': tk.StringVar(),
            'v': tk.StringVar()
        }
        
        # Labels y entradas
        self.entries = {}
        params_info = [
            ('x0', 'Posición inicial (m):', True),
            ('v0', 'Velocidad inicial (m/s):', True),
            ('a', 'Aceleración (m/s²):', False),
            ('t', 'Tiempo (s):', True),
            ('x', 'Posición final (m):', False),
            ('v', 'Velocidad final (m/s):', False)
        ]
        
        for var_name, label_text, is_enabled in params_info:
            frame = ttk.Frame(params_section)
            frame.pack(fill=tk.X, pady=2)
            
            label = ttk.Label(frame, text=label_text, width=20)
            label.pack(side=tk.LEFT)
            
            entry = ttk.Entry(frame, textvariable=self.vars[var_name], width=15)
            entry.pack(side=tk.LEFT, padx=(5, 0))
            
            self.entries[var_name] = entry
            
            if not is_enabled:
                entry.configure(state='disabled')
        
        # Actualizar estado inicial
        self.on_movement_type_change()
        
        # Botones de acción
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill=tk.X, pady=15)
        
        ttk.Button(buttons_frame, text="Calcular", 
                    command=self.calculate).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Limpiar", 
                    command=self.clear_all).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Graficar", 
                    command=self.plot_results).pack(side=tk.LEFT)
        
        # Sección de resultados
        results_section = ttk.LabelFrame(parent, text="Resultados", padding=10)
        results_section.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = tk.Text(results_section, height=10, width=40, 
                                    wrap=tk.WORD, state=tk.DISABLED)
        scrollbar_results = ttk.Scrollbar(results_section, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar_results.set)
        
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_results.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_plot_area(self, parent):
        """Crear área de gráficos"""
        plot_section = ttk.LabelFrame(parent, text="Gráficos", padding=10)
        plot_section.pack(fill=tk.BOTH, expand=True)
        
        # Crear figura de matplotlib
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, plot_section)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Toolbar para navegación del gráfico
        toolbar_frame = ttk.Frame(plot_section)
        toolbar_frame.pack(fill=tk.X)
        
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
    
    def on_movement_type_change(self):
        """Manejar cambio de tipo de movimiento"""
        if self.movement_type.get() == "uniform":
            # MRU: deshabilitar aceleración
            self.entries['a'].configure(state='disabled')
            self.vars['a'].set('0')
        else:
            # MRUA: habilitar aceleración
            self.entries['a'].configure(state='normal')
    
    def calculate(self):
        """Realizar cálculos de cinemática"""
        try:
            # Obtener valores de entrada
            params = {}
            for key, var in self.vars.items():
                value = var.get().strip()
                if value:
                    if not self.validator.is_valid_number(value):
                        raise ValueError(f"Valor inválido para {key}: {value}")
                    params[key] = float(value)
                else:
                    params[key] = None
            
            # Realizar cálculo según el tipo de movimiento
            if self.movement_type.get() == "uniform":
                self.results = self.calculator.calculate_mru(params)
            else:
                self.results = self.calculator.calculate_mrua(params)
            
            # Mostrar resultados
            self.display_results()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {str(e)}")
    
    def display_results(self):
        """Mostrar resultados en el área de texto"""
        self.results_text.configure(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        if self.results:
            text = "RESULTADOS DEL CÁLCULO\n"
            text += "=" * 30 + "\n\n"
            
            # Mostrar parámetros utilizados
            text += "Parámetros utilizados:\n"
            for key, value in self.results.get('input_params', {}).items():
                if value is not None:
                    text += f"  {key}: {value}\n"
            
            text += "\nResultados calculados:\n"
            for key, value in self.results.get('calculated_values', {}).items():
                text += f"  {key}: {value:.3f}\n"
            
            # Mostrar ecuaciones utilizadas
            if 'equations' in self.results:
                text += "\nEcuaciones utilizadas:\n"
                for eq in self.results['equations']:
                    text += f"  • {eq}\n"
        
        self.results_text.insert(1.0, text)
        self.results_text.configure(state=tk.DISABLED)
    
    def plot_results(self):
        """Generar gráficos de los resultados"""
        if not self.results:
            messagebox.showwarning("Advertencia", "Primero debe realizar un cálculo")
            return
        
        try:
            # Limpiar figura
            self.fig.clear()
            
            # Crear subplots
            ax1 = self.fig.add_subplot(2, 1, 1)
            ax2 = self.fig.add_subplot(2, 1, 2)
            
            # Generar datos para graficar
            plot_data = self.calculator.generate_plot_data(self.results)
            
            # Gráfico de posición vs tiempo
            ax1.plot(plot_data['time'], plot_data['position'], 'b-', linewidth=2, label='Posición')
            ax1.set_xlabel('Tiempo (s)')
            ax1.set_ylabel('Posición (m)')
            ax1.set_title('Posición vs Tiempo')
            ax1.grid(True, alpha=0.3)
            ax1.legend()
            
            # Gráfico de velocidad vs tiempo
            ax2.plot(plot_data['time'], plot_data['velocity'], 'r-', linewidth=2, label='Velocidad')
            ax2.set_xlabel('Tiempo (s)')
            ax2.set_ylabel('Velocidad (m/s)')
            ax2.set_title('Velocidad vs Tiempo')
            ax2.grid(True, alpha=0.3)
            ax2.legend()
            
            # Ajustar layout
            self.fig.tight_layout()
            
            # Actualizar canvas
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar gráfico: {str(e)}")
    
    def clear_all(self):
        """Limpiar todos los campos y resultados"""
        for var in self.vars.values():
            var.set('')
        
        self.results = {}
        
        self.results_text.configure(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.configure(state=tk.DISABLED)
        
        self.fig.clear()
        self.canvas.draw()
        
        # Restaurar estado de campos según tipo de movimiento
        self.on_movement_type_change()