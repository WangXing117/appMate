from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QFormLayout
)
from PyQt5.QtCore import Qt
from interpolacion import euler, interpolar_lagrange
import numpy as np
import matplotlib.pyplot as plt

class EulerInputWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora de EDO por Método de Euler")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Campos de entrada
        self.func_input = QLineEdit()
        self.x0_input = QLineEdit()
        self.y0_input = QLineEdit()
        self.h_input = QLineEdit()
        self.xf_input = QLineEdit()
        self.dec_input = QLineEdit()
        self.dec_input.setPlaceholderText("(Opcional, por defecto 2)")

        form_layout.addRow("Ecuación f(x, y):", self.func_input)
        form_layout.addRow("x0 (valor inicial de x):", self.x0_input)
        form_layout.addRow("y0 (valor inicial de y):", self.y0_input)
        form_layout.addRow("Paso h:", self.h_input)
        form_layout.addRow("x final:", self.xf_input)
        form_layout.addRow("Decimales:", self.dec_input)

        layout.addLayout(form_layout)

        # Botón
        self.solve_btn = QPushButton("Resolver")
        self.solve_btn.clicked.connect(self.on_resolve_clicked)
        layout.addWidget(self.solve_btn)

        self.setLayout(layout)

    def on_resolve_clicked(self):
        try:
            f_expr = self.func_input.text().strip()
            x0 = float(self.x0_input.text().strip())
            y0 = float(self.y0_input.text().strip())
            h = float(self.h_input.text().strip())
            xf = float(self.xf_input.text().strip())
            dec = self.dec_input.text().strip()
            dec = int(dec) if dec else 2

            if not f_expr:
                raise ValueError("La ecuación no puede estar vacía.")

            # Crear función a partir del string f_expr usando eval
            def f(x, y):
                return eval(f_expr, {"x": x, "y": y, "np": np})

            # Calcular número de pasos
            n = int((xf - x0) / h)
            x_vals, y_vals = euler(f, x0, y0, h, n)

            # Interpolación
            poly = interpolar_lagrange(x_vals, y_vals)
            x_interp = np.linspace(x0, x_vals[-1], 100)
            y_interp = poly(x_interp)

            # Mostrar resultados en mensaje
            msg = (f"El resultado aproximado de la ecuación '{f_expr}' es:\n"
                   f"x = {x_vals[-1]:.{dec}f}, y = {y_vals[-1]:.{dec}f}")
            QMessageBox.information(self, "Resultado", msg)

            # Mostrar gráfica
            plt.plot(x_vals, y_vals, 'o', label='Puntos (Euler)')
            plt.plot(x_interp, y_interp, '-', label='Interpolación (Lagrange)')
            plt.title(f"Solución Aproximada de y' = {f_expr}")
            plt.xlabel("x")
            plt.ylabel("y")
            plt.grid(True)
            plt.legend()
            plt.show()

        except Exception as e:
            QMessageBox.critical(self, "Error de entrada", str(e))


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = EulerInputWindow()
    window.show()
    sys.exit(app.exec_())
