#!/usr/bin/env python3
"""
Archivo de prueba para verificar que todas las dependencias están instaladas correctamente
"""

def test_imports():
    """Probar todas las importaciones necesarias"""
    print("Probando importaciones...")
    
    try:
        print("✓ Probando PySide6...")
        from PySide6.QtWidgets import QApplication, QWidget
        from PySide6.QtCore import Qt
        from PySide6.QtGui import QFont
        print("  PySide6 OK")
    except ImportError as e:
        print(f"  ✗ Error con PySide6: {e}")
        return False
    
    try:
        print("✓ Probando matplotlib...")
        import matplotlib
        matplotlib.use('QtAgg')
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
        from matplotlib.figure import Figure
        print("  matplotlib OK")
    except ImportError as e:
        print(f"  ✗ Error con matplotlib: {e}")
        return False
    
    try:
        print("✓ Probando numpy...")
        import numpy as np
        print("  numpy OK")
    except ImportError as e:
        print(f"  ✗ Error con numpy: {e}")
        return False
    
    try:
        print("✓ Probando módulos locales...")
        from modules.kinematics import KinematicsCalculator
        from modules.dynamics import DynamicsCalculator
        from utils.validators import InputValidator
        print("  Módulos locales OK")
    except ImportError as e:
        print(f"  ✗ Error con módulos locales: {e}")
        return False
    
    print("\n¡Todas las dependencias están correctamente instaladas!")
    return True

def test_basic_functionality():
    """Probar funcionalidad básica"""
    print("\nProbando funcionalidad básica...")
    
    try:
        # Probar calculadora de cinemática
        from modules.kinematics import KinematicsCalculator
        calc = KinematicsCalculator()
        
        # Probar MRU simple
        params = {'x0': 0, 'v0': 10, 't': 5}
        result = calc.calculate_mru(params)
        print(f"✓ Cálculo MRU: x = {result['calculated_values']['x']:.2f}")
        
        # Probar calculadora de dinámica
        from modules.dynamics import DynamicsCalculator
        dyn_calc = DynamicsCalculator()
        dyn_params = {'m': 10, 'a': 2}
        dyn_result = dyn_calc.calculate_newton_second_law(dyn_params)
        print(f"✓ Cálculo Dinámica: F = {dyn_result['calculated_values']['f']:.2f}")
        
        # Probar validador
        from utils.validators import InputValidator
        validator = InputValidator()
        
        valid = validator.is_valid_number("123.45")
        print(f"✓ Validación de números: {valid}")
        
        print("  Funcionalidad básica OK")
        return True
        
    except Exception as e:
        print(f"  ✗ Error en funcionalidad básica: {e}")
        return False

if __name__ == "__main__":
    print("=== PRUEBA DE DEPENDENCIAS CPHYSICS ===\n")
    
    imports_ok = test_imports()
    
    if imports_ok:
        functionality_ok = test_basic_functionality()
        
        if functionality_ok:
            print("\n🎉 ¡Todo listo! Puedes ejecutar la aplicación con: python main.py")
        else:
            print("\n❌ Hay problemas con la funcionalidad básica")
    else:
        print("\n❌ Faltan dependencias. Ejecuta: pip install PySide6 matplotlib numpy")