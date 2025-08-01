#!/usr/bin/env python3
"""
CPHYSICS - Aplicación de Física Computacional
Punto de entrada principal de la aplicación
"""

import tkinter as tk
from gui.base_window import MainWindow

def main():
    """Función principal que inicia la aplicación"""
    # Crear la ventana principal
    root = tk.Tk()
    
    # Configuraciones básicas de la ventana
    root.title("CPHYSICS - Física Computacional")
    root.geometry("1000x700")
    root.minsize(800, 600)
    
    # Configurar el ícono (opcional)
    try:
        root.iconbitmap("assets/icon.ico")  # Para Windows
    except:
        pass  # Si no hay ícono, continuar sin él
    
    # Crear la aplicación principal
    app = MainWindow(root)
    
    # Iniciar el bucle principal
    root.mainloop()

if __name__ == "__main__":
    main()