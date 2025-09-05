"""
Main window for the CPhysics application.

This module defines the main window, which contains the primary layout,
navigation controls, and the content area for displaying physics modules.
"""

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLabel, QStackedWidget, QFrame)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont

from gui.kinematics_frame import KinematicsFrame
from gui.dynamics_frame import DynamicsFrame
from gui.thermodynamics_frame import ThermodynamicsFrame
from gui.waves_frame import WavesFrame
from gui.electromagnetism_frame import ElectromagnetismFrame

class MainWindow(QMainWindow):
    """
    Main application window.

    Sets up the UI, including a navigation bar to switch between physics
    modules and a central stacked widget to display module content.
    """
    def __init__(self):
        """Initializes the main window and sets up the UI."""
        super().__init__()
        
        self.setup_window()
        self.create_widgets()
        
        # Show the Kinematics module by default on startup.
        self.show_kinematics()

    def setup_window(self):
        """Configures basic properties of the main window."""
        self.setWindowTitle("CPhysics - Computational Physics")
        self.setMinimumSize(QSize(1000, 700))
        self.resize(1200, 800)
        self.center_window()

    def center_window(self):
        """Centers the main window on the screen."""
        screen = self.screen().availableGeometry()
        window_geometry = self.geometry()
        self.move(
            (screen.width() - window_geometry.width()) // 2,
            (screen.height() - window_geometry.height()) // 2
        )

    def create_widgets(self):
        """Creates and arranges the main widgets of the application."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        
        title_label = QLabel("CPhysics - Computational Physics")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        nav_layout = self.create_navigation()
        main_layout.addLayout(nav_layout)
        
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.HLine)
        main_layout.addWidget(separator)
        
        # This widget holds the different physics module frames.
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("content_area")
        main_layout.addWidget(self.content_stack)
        
        self.create_modules()

    def create_navigation(self):
        """Creates the navigation bar with buttons to switch modules."""
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(10)
        
        # Tuples contain the button label and the callback to switch views.
        modules_info = [
            ("Kinematics", self.show_kinematics),
            ("Dynamics", self.show_dynamics),
            ("Thermodynamics", self.show_thermodynamics),
            ("Waves", self.show_waves),
            ("Electromagnetism", self.show_electromagnetism)
        ]
        
        self.nav_buttons = []
        for name, callback in modules_info:
            button = QPushButton(name)
            button.setObjectName("nav_button")
            # A checkable button can be toggled to show a persistent active state.
            button.setCheckable(True)
            button.clicked.connect(callback)
            nav_layout.addWidget(button)
            self.nav_buttons.append(button)
        
        nav_layout.addStretch()
        return nav_layout

    def create_modules(self):
        """Instantiates all physics modules and adds them to the QStackedWidget."""
        self.kinematics_frame = KinematicsFrame(self.content_stack)
        self.content_stack.addWidget(self.kinematics_frame)
        
        self.dynamics_frame = DynamicsFrame(self.content_stack)
        self.content_stack.addWidget(self.dynamics_frame)
        
        self.thermodynamics_frame = ThermodynamicsFrame(self.content_stack)
        self.content_stack.addWidget(self.thermodynamics_frame)
        
        self.waves_frame = WavesFrame(self.content_stack)
        self.content_stack.addWidget(self.waves_frame)
        
        self.electromagnetism_frame = ElectromagnetismFrame(self.content_stack)
        self.content_stack.addWidget(self.electromagnetism_frame)

    def set_active_button(self, active_index):
        """
        Sets the visual state of the navigation buttons.

        Args:
            active_index (int): The index of the button to be marked as active.
        """
        for i, button in enumerate(self.nav_buttons):
            button.setChecked(i == active_index)

    def show_kinematics(self):
        """Switches the view to the Kinematics module."""
        self.content_stack.setCurrentWidget(self.kinematics_frame)
        self.set_active_button(0)

    def show_dynamics(self):
        """Switches the view to the Dynamics module."""
        self.content_stack.setCurrentWidget(self.dynamics_frame)
        self.set_active_button(1)

    def show_thermodynamics(self):
        """Switches the view to the Thermodynamics module."""
        self.content_stack.setCurrentWidget(self.thermodynamics_frame)
        self.set_active_button(2)

    def show_waves(self):
        """Switches the view to the Waves module."""
        self.content_stack.setCurrentWidget(self.waves_frame)
        self.set_active_button(3)

    def show_electromagnetism(self):
        """Switches the view to the Electromagnetism module."""
        self.content_stack.setCurrentWidget(self.electromagnetism_frame)
        self.set_active_button(4)