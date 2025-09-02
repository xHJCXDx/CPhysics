"""
Main window of the CPHYSICS application
Contains the navigation and the container for the different modules
"""

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                                QPushButton, QLabel, QStackedWidget, QFrame)
from PySide6.QtCore import Qt, QSize
from gui.electromagnetism_frame import ElectromagnetismFrame
from PySide6.QtGui import QFont
from gui.kinematics_frame import KinematicsFrame
from gui.dynamics_frame import DynamicsFrame
from gui.thermodynamics_frame import ThermodynamicsFrame
from gui.waves_frame import WavesFrame
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configure the main window
        self.setup_window()
        
        
        
        # Create the interface
        self.create_widgets()
        
        # Set the initial state on the first tab
        self.show_kinematics()
        
    
    def setup_window(self):
        """Configure basic window properties"""
        self.setWindowTitle("CPHYSICS - Computational Physics")
        self.setMinimumSize(QSize(1000, 700))
        self.resize(1200, 800)
        
        # Center the window on the screen
        self.center_window()
    
    def center_window(self):
        """Center the window on the screen"""
        screen = self.screen().availableGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    
    
    def create_widgets(self):
        """Create the main widgets of the window"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        
        # Application title
        title_label = QLabel("CPHYSICS - Computational Physics")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Navigation bar
        nav_layout = self.create_navigation()
        main_layout.addLayout(nav_layout)
        
        # Separator
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.HLine)
        main_layout.addWidget(separator)
        
        # Content area with stack widget to switch between modules
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("content_area")
        main_layout.addWidget(self.content_stack)
        
        # Create the modules
        self.create_modules()
    
    def create_navigation(self):
        """Create navigation bar"""
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(10)
        
        # List of modules with their names and functions
        modules_info = [
            ("Kinematics", self.show_kinematics),
            ("Dynamics", self.show_dynamics),
            ("Thermodynamics", self.show_thermodynamics),
            ("Waves", self.show_waves),
            ("Electromagnetism", self.show_electromagnetism)
        ]
        
        # Create navigation buttons
        self.nav_buttons = []
        for name, callback in modules_info:
            button = QPushButton(name)
            button.setObjectName("nav_button")
            button.setCheckable(True)  # To be able to mark the active button
            button.clicked.connect(callback)
            nav_layout.addWidget(button)
            self.nav_buttons.append(button)
        
        # Add flexible space at the end
        nav_layout.addStretch()
        
        return nav_layout
    
    def create_modules(self):
        """Create all modules and add them to the stack"""
        # Kinematics module
        self.kinematics_frame = KinematicsFrame(self.content_stack)
        self.content_stack.addWidget(self.kinematics_frame)
        
        # Dynamics module
        self.dynamics_frame = DynamicsFrame(self.content_stack)
        self.content_stack.addWidget(self.dynamics_frame)
        
        # Thermodynamics module
        self.thermodynamics_frame = ThermodynamicsFrame(self.content_stack)
        self.content_stack.addWidget(self.thermodynamics_frame)
        
        self.waves_frame = WavesFrame(self.content_stack)
        self.content_stack.addWidget(self.waves_frame)
        
        self.electromagnetism_frame = ElectromagnetismFrame(self.content_stack)
        self.content_stack.addWidget(self.electromagnetism_frame)
    
    def create_placeholder(self, text, parent=None):
        """Create a placeholder widget for modules in development"""
        widget = QWidget(parent)
        layout = QVBoxLayout(widget)
        
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        
        
        layout.addWidget(label)
        return widget
    
    def set_active_button(self, active_index):
        """Mark the active button in the navigation"""
        for i, button in enumerate(self.nav_buttons):
            button.setChecked(i == active_index)
    
    def show_kinematics(self):
        """Show the kinematics module"""
        self.content_stack.setCurrentWidget(self.kinematics_frame)
        self.set_active_button(0)
    
    def show_dynamics(self):
        """Show the dynamics module"""
        self.content_stack.setCurrentWidget(self.dynamics_frame)
        self.set_active_button(1)
    
    def show_thermodynamics(self):
        """Show the thermodynamics module"""
        self.content_stack.setCurrentWidget(self.thermodynamics_frame)
        self.set_active_button(2)
    
    def show_waves(self):
        """Show the waves module"""
        self.content_stack.setCurrentWidget(self.waves_frame)
        self.set_active_button(3)
    
    def show_electromagnetism(self):
        """Show the electromagnetism module"""
        self.content_stack.setCurrentWidget(self.electromagnetism_frame)
        self.set_active_button(4)