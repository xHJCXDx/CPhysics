import os

file_path = "c:\\Users\\hiroj\\OneDrive\\HJCXD\\Programacion\\Proyectos\\CPhysics\\gui\\dynamics_frame.py"

with open(file_path, "r") as f:
    content = f.read()

new_content = content.replace(
    """    def display_newton_results(self):
        """Mostrar resultados en el área de texto y en el campo de entrada correspondiente"""
        if not self.results: return

        calculated_values = self.results.get('calculated_values', {})
        if calculated_values:
            calculated_var, calculated_val = list(calculated_values.items())[0]
            self.input_fields[calculated_var].setText(f\"{calculated_val:.4f}\")

        text = \"<b style='font-size:13px;'>RESULTADOS DEL CÁLCULO (2ª Ley de Newton)</b><br>\"
        text += \"=" * 50 + \"<br><br>\"

        text += \"<b>Parámetros utilizados:</b><br>\"
        text += \"-" * 25 + \"<br>\"
        param_map = {
            'f': 'Fuerza Aplicada (N)', 
            'm': 'Masa (kg)', 
            'a': 'Aceleración (m/s²)',
            'mu': 'Coef. Fricción (μ)',
            'angle': 'Ángulo del Plano (°)'
        }
        for key, value in self.results.get('input_params', {}).items():
            if value is not None:
                text += f\"&nbsp;&nbsp;• {param_map.get(key, key)}: {value}<br>\" 

        text += \"<br><b>Resultado calculado:</b><br>\"
        text += \"-" * 25 + \"<br>\"
        for key, value in calculated_values.items():
            text += f\"&nbsp;&nbsp;• <span style='color:#3498db;'>{param_map.get(key, key)}</span>: {value:.4f}<br>\"

        normal_force = self.results.get('normal_force')
        if normal_force is not None:
            text += \"<br><b>Fuerza Normal:</b><br>\"
            text += \"-" * 25 + \"<br>\"
            text += f\"&nbsp;&nbsp;• F_normal: {normal_force:.4f} N<br>\"

        friction_force = self.results.get('friction_force')
        if friction_force is not None:
            text += \"<br><b>Fuerza de Fricción:</b><br>\"
            text += \"-" * 25 + \"<br>\"
            text += f\"&nbsp;&nbsp;• F_fricción: {friction_force:.4f} N<br>\"

        text += \"<br><b style='color:#9b59b6;'>Ecuaciones utilizadas:</b><br>\"
        text += \"-" * 25 + \"<br>\"
        for eq in self.results.get('equations', []):
            text += f\"&nbsp;&nbsp;• {eq}<br>\"
        self.results_text.setHtml(text)"",
    """    def display_newton_results(self):
        """Mostrar resultados en el área de texto y en el campo de entrada correspondiente"""
        if not self.results: return

        calculated_values = self.results.get('calculated_values', {})
        if calculated_values:
            calculated_var, calculated_val = list(calculated_values.items())[0]
            self.input_fields[calculated_var].setText(f\"{calculated_val:.4f}\")

        html_parts = [
            \"<b style='font-size:13px;'>RESULTADOS DEL CÁLCULO (2ª Ley de Newton)</b><br>\",
            \"=" * 50 + \"<br><br>\",
            \"<b>Parámetros utilizados:</b><br>\",
            \"-" * 25 + \"<br>\"
        ] 
        
        param_map = {
            'f': 'Fuerza Aplicada (N)', 
            'm': 'Masa (kg)', 
            'a': 'Aceleración (m/s²)',
            'mu': 'Coef. Fricción (μ)',
            'angle': 'Ángulo del Plano (°)'
        }
        for key, value in self.results.get('input_params', {}).items():
            if value is not None:
                html_parts.append(f\"&nbsp;&nbsp;• {param_map.get(key, key)}: {value}<br>\")

        html_parts.extend([
            \"<br><b>Resultado calculado:</b><br>\",
            \"-" * 25 + \"<br>\"
        ])
        for key, value in calculated_values.items():
            html_parts.append(f\"&nbsp;&nbsp;• <span style='color:#3498db;'>{param_map.get(key, key)}</span>: {value:.4f}<br>\")

        normal_force = self.results.get('normal_force')
        if normal_force is not None:
            html_parts.extend([
                \"<br><b>Fuerza Normal:</b><br>\",
                \"-" * 25 + \"<br>\",
                f\"&nbsp;&nbsp;• F_normal: {normal_force:.4f} N<br>\"
            ])

        friction_force = self.results.get('friction_force')
        if friction_force is not None:
            html_parts.extend([
                \"<br><b>Fuerza de Fricción:</b><br>\",
                \"-" * 25 + \"<br>\",
                f\"&nbsp;&nbsp;• F_fricción: {friction_force:.4f} N<br>\"
            ])

        html_parts.extend([
            \"<br><b style='color:#9b59b6;'>Ecuaciones utilizadas:</b><br>\",
            \"-" * 25 + \"<br>\"
        ])
        for eq in self.results.get('equations', []):
            html_parts.append(f\"&nbsp;&nbsp;• {eq}<br>\")
        
        self.results_text.setHtml("".join(html_parts))""
)

new_content = new_content.replace(
    """    def display_energy_result(self, title, value, equation, params):
        text = f\"<b style='font-size:13px;'>RESULTADO - {title.upper()}</b><br>\"
        text += \"=" * 50 + \"<br><br>\"

        text += \"<b>Parámetros:</b><br>\"
        for name, val in params.items():
            if val is not None:
                text += f\"&nbsp;&nbsp;• {name}: {val}<br>\"
        
        text += f\"<br><b>Ecuación:</b><br>&nbsp;&nbsp;• {equation}<br>\"
        text += f\"<br><b>Resultado:</b><br>&nbsp;&nbsp;• <span style='color:#2ecc71;'>{title}</span>: {value:.4f} Joules<br>\"
        
        self.results_text.setHtml(text)""",
    """    def display_energy_result(self, title, value, equation, params):
        html_parts = [
            f\"<b style='font-size:13px;'>RESULTADO - {title.upper()}</b><br>\",
            \"=" * 50 + \"<br><br>\",
            \"<b>Parámetros:</b><br>\"
        ]
        for name, val in params.items():
            if val is not None:
                html_parts.append(f\"&nbsp;&nbsp;• {name}: {val}<br>\")
        
        html_parts.extend([
            f\"<br><b>Ecuación:</b><br>&nbsp;&nbsp;• {equation}<br>\",
            f\"<br><b>Resultado:</b><br>&nbsp;&nbsp;• <span style='color:#2ecc71;'>{title}</span>: {value:.4f} Joules<br>\"
        ])
        
        self.results_text.setHtml("".join(html_parts))"""
)

new_content = new_content.replace(
    """    def display_momentum_result(self, title, value, equation, params):
        text = f\"<b style='font-size:13px;'>RESULTADO - {title.upper()}</b><br>\"
        text += \"=" * 50 + \"<br><br>\"

        text += \"<b>Parámetros:</b><br>\"
        for name, val in params.items():
            if val is not None:
                text += f\"&nbsp;&nbsp;• {name}: {val}<br>\"
        
        text += f\"<br><b>Ecuación:</b><br>&nbsp;&nbsp;• {equation}<br>\"
        
        unit = \"\"
        if \"Impulso\" in title:
            unit = \"N·s\"
        elif \"Momento\" in title:
            unit = \"kg·m/s\"
        elif \"Fuerza\" in title:
            unit = \"N\"
        elif \"Tiempo\" in title:
            unit = \"s\"
        elif \"Masa\" in title:
            unit = \"kg\"
        elif \"Velocidad\" in title:
            unit = \"m/s\"

        text += f\"<br><b>Resultado:</b><br>&nbsp;&nbsp;• <span style='color:#2ecc71;'>{title}</span>: {value:.4f} {unit}<br>\"
        
        self.results_text.setHtml(text)""",
    """    def display_momentum_result(self, title, value, equation, params):
        html_parts = [
            f\"<b style='font-size:13px;'>RESULTADO - {title.upper()}</b><br>\",
            \"=" * 50 + \"<br><br>\",
            \"<b>Parámetros:</b><br>\"
        ]
        for name, val in params.items():
            if val is not None:
                html_parts.append(f\"&nbsp;&nbsp;• {name}: {val}<br>\")
        
        html_parts.extend([
            f\"<br><b>Ecuación:</b><br>&nbsp;&nbsp;• {equation}<br>\"
        ])
        
        unit_map = {
            \"Impulso\": \"N·s\",
            \"Momento\": \"kg·m/s\",
            \"Fuerza\": \"N\",
            \"Tiempo\": \"s\",
            \"Masa\": \"kg\",
            \"Velocidad\": \"m/s\"
        }
        unit = \"\"
        for key, u in unit_map.items():
            if key in title:
                unit = u
                break

        html_parts.append(f\"<br><b>Resultado:</b><br>&nbsp;&nbsp;• <span style='color:#2ecc71;'>{title}</span>: {value:.4f} {unit}<br>\")
        
        self.results_text.setHtml("".join(html_parts))"""
)

with open(file_path, "w") as f:
    f.write(new_content)
