#!/usr/bin/env python3
"""
CPHYSICS - Computational Physics Application
Main entry point for the application.
"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from gui.base_window import MainWindow

def main():
    """Initializes and runs the application."""
    app = QApplication(sys.argv)

    app.setApplicationName("CPHYSICS")
    app.setApplicationDisplayName("CPHYSICS - Computational Physics")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("CPHYSICS")

    # Set the application icon
    try:
        app.setWindowIcon(QIcon("assets/icon.png"))
    except FileNotFoundError:
        print("Warning: Icon file 'assets/icon.png' not found.")

    # Load the stylesheet
    try:
        with open("gui/styles.qss", "r") as f:
            style_sheet = f.read()
            app.setStyleSheet(style_sheet)
    except FileNotFoundError:
        print("Warning: Stylesheet file 'gui/styles.qss' not found.")

    # Create and show the main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
