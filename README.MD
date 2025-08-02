# CPHYSICS - Aplicación de Física Computacional

Una aplicación de escritorio moderna para resolver problemas de física con interfaz gráfica intuitiva y capacidades de visualización avanzadas.

## Características

- **Interfaz gráfica**: Desarrollada con PySide6 (Qt6)
- **Módulo de Cinemática**: Cálculos de MRU y MRUA con visualización gráfica
- **Validación de entradas**: Sistema robusto de validación de datos
- **Conversión de unidades**: Soporte para múltiples sistemas de unidades
- **Gráficos interactivos**: Visualización de resultados con matplotlib
- **Arquitectura modular**: Fácil extensión para nuevos módulos de física
- **Diseño responsivo**: Interfaz adaptable con paneles redimensionables

## Tecnologías Utilizadas

- **PySide6**: Framework de interfaz gráfica basado en Qt6
- **Matplotlib**: Generación de gráficos científicos
- **NumPy**: Cálculos numéricos eficientes
- **Python 3.8+**: Lenguaje de programación principal

## Estructura del Proyecto

```
CPHYSICS/
│
├── main.py                     # Punto de entrada de la app
├── gui/
│   ├── __init__.py
│   ├── base_window.py          # Ventana principal con navegación
│   └── kinematics_frame.py     # Interfaz específica para cinemática
│
├── modules/
│   ├── __init__.py
│   └── kinematics.py           # Funciones físicas de cinemática
│
├── assets/
│   └── icon.png                # Íconos, imágenes, etc.
│
├── utils/
│   ├── __init__.py
│   └── validators.py           # Validación de entradas, conversión de unidades
│
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Este archivo
```

## Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clona el repositorio:**
```bash
git clone <tu-repositorio>
cd CPHYSICS
```

2. **Instala las dependencias:**
```bash
pip install -r requirements.txt
```

3. **Ejecuta la aplicación:**
```bash
python main.py
```

### Instalación alternativa

Si prefieres instalar las dependencias manualmente:

```bash
pip install PySide6 matplotlib numpy
```

## Uso

### Módulo de Cinemática

El módulo de cinemática permite resolver problemas de:

- **Movimiento Rectilíneo Uniforme (MRU)**
- **Movimiento Rectilíneo Uniformemente Acelerado (MRUA)**

#### Funcionalidades principales:

1. **Selección de tipo de movimiento**: Elige entre MRU y MRUA
2. **Entrada de parámetros**: Introduce los valores conocidos en los campos correspondientes
3. **Cálculo automático**: La aplicación calcula automáticamente los valores faltantes
4. **Visualización gráfica**: Genera gráficos de posición y velocidad vs tiempo
5. **Validación inteligente**: Sistema de validación que previene errores de entrada

#### Ejemplo de uso paso a paso:

1. **Selecciona el tipo de movimiento**:
   - MRU para velocidad constante
   - MRUA para aceleración constante

2. **Introduce los parámetros conocidos**:
   - Posición inicial (x₀)
   - Velocidad inicial (v₀)
   - Aceleración (a) - solo para MRUA
   - Tiempo (t)
   - Posición final (x)
   - Velocidad final (v)

3. **Calcula los resultados**:
   - Haz clic en "Calcular"
   - Revisa los resultados en el panel de la derecha

4. **Visualiza el movimiento**:
   - Haz clic en "Graficar"
   - Explora los gráficos interactivos

5. **Limpia y repite**:
   - Usa "Limpiar" para empezar un nuevo problema

## Ecuaciones Implementadas

### Movimiento Rectilíneo Uniforme (MRU)
- **Posición**: `x = x₀ + v₀ × t`
- **Velocidad**: `v = v₀` (constante)

### Movimiento Rectilíneo Uniformemente Acelerado (MRUA)
- **Posición**: `x = x₀ + v₀ × t + ½ × a × t²`
- **Velocidad**: `v = v₀ + a × t`
- **Relación velocidad-posición**: `v² = v₀² + 2 × a × (x - x₀)`

## Características de la Interfaz

### Diseño Moderno
- **Tema visual profesional** con colores armoniosos
- **Tipografía clara** optimizada para lectura científica
- **Iconografía consistente** en toda la aplicación

### Usabilidad Avanzada
- **Paneles redimensionables** para adaptar la vista a tus necesidades
- **Scroll automático** en secciones largas
- **Validación en tiempo real** de las entradas
- **Gráficos interactivos** con zoom y navegación

### Responsive Design
- **Ventana redimensionable** con tamaño mínimo garantizado
- **Layouts flexibles** que se adaptan al tamaño de la ventana
- **Controles optimizados** para diferentes resoluciones

## Desarrollo

### Agregar nuevos módulos de física

Para extender la aplicación con nuevos módulos:

1. **Crea el módulo de cálculo** en `modules/`:
```python
class NewPhysicsCalculator:
    def calculate_something(self, params):
        return {
            'input_params': {},
            'calculated_values': {},
            'equations': [],
            'movement_type': 'new_type'
        }
```

2. **Crea la interfaz gráfica** en `gui/`:
```python
class NewPhysicsFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
```

3. **Agrega la navegación** en `base_window.py`
4. **Actualiza los archivos** `__init__.py`

### Estructura de datos estándar

Todos los módulos deben devolver resultados en el formato:

```python
{
    'input_params': dict,      # Parámetros de entrada utilizados
    'calculated_values': dict, # Valores calculados
    'equations': list,         # Ecuaciones utilizadas
    'movement_type': str       # Tipo de cálculo realizado
}
```

### Guías de estilo

- **PEP 8** para el código Python
- **Docstrings** en formato Google/NumPy
- **Type hints** para mejor documentación
- **Nombres descriptivos** para variables y funciones

## Solución de Problemas

### Problemas comunes

**Error al importar PySide6:**
```bash
pip install --upgrade PySide6
```

**Gráficos no se muestran:**
```bash
pip install --upgrade matplotlib
```

**Problemas de DPI en pantallas de alta resolución:**
- La aplicación incluye soporte automático para DPI alto
- Si persisten problemas, ajusta las variables de entorno del sistema

### Logs y depuración

Para activar el modo de depuración, ejecuta:
```bash
python main.py --debug
```

## Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. **Fork el proyecto**
2. **Crea una rama** para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit tus cambios** (`git commit -am 'Agregar nueva funcionalidad'`)
4. **Push a la rama** (`git push origin feature/nueva-funcionalidad`)
5. **Crea un Pull Request**

### Áreas donde puedes contribuir

- **Nuevos módulos de física**
- **Mejoras en la interfaz**
- **Optimizaciones de rendimiento**
- **Documentación y tutoriales**
- **Pruebas unitarias**
- **Localización (i18n)**

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Roadmap

### Versión 1.1 (Próxima)
- [ ] **Módulo de Dinámica** con fuerzas y leyes de Newton
- [ ] **Exportación de resultados** a PDF y Excel
- [ ] **Guardar/cargar proyectos** en formato JSON

### Versión 1.2
- [ ] **Módulo de Termodinámica** con procesos termodinámicos
- [ ] **Módulo de Ondas** con oscilaciones y propagación
- [ ] **Calculadora de unidades** integrada

### Versión 2.0
- [ ] **Módulo de Electromagnetismo** completo
- [ ] **Simulaciones 3D** interactivas
- [ ] **Modo oscuro** y temas personalizables
- [ ] **Soporte multiidioma** (Español, Inglés, Francés)

### Funcionalidades futuras
- [ ] **Base de datos** de problemas resueltos
- [ ] **Integración con SymPy** para cálculo simbólico
- [ ] **Plugin system** para módulos externos
- [ ] **Modo colaborativo** para trabajo en equipo

## Contacto y Soporte

- **Issues**: Para reportar bugs o solicitar funcionalidades
- **Discussions**: Para preguntas generales y discusiones
- **Wiki**: Documentación técnica detallada

---
