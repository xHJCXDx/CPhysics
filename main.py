#!/usr/bin/env python3
"""
CPHYSICS - Aplicación de Física Computacional
Punto de entrada principal de la aplicación
"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from gui.base_window import MainWindow

def main():
    """Función principal que inicia la aplicación"""
    # Crear la aplicación
    app = QApplication(sys.argv)
    
    # Configurar propiedades de la aplicación
    app.setApplicationName("CPHYSICS")
    app.setApplicationDisplayName("CPHYSICS - Física Computacional")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("CPHYSICS")
    
    # Configurar el ícono de la aplicación (opcional)
    try:
        app.setWindowIcon(QIcon("assets/icon.png"))
    except:
        pass  # Si no hay ícono, continuar sin él
    
    # Crear la ventana principal
    window = MainWindow()
    window.show()
    
    # Iniciar el bucle principal
    sys.exit(app.exec())

if __name__ == "__main__":
    main()