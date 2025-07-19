from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QFormLayout
)
from PyQt5.QtCore import Qt
from interpolacion import euler, interpolar_lagrange
from derivacion import resolver_por_derivacion
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


class DerivacionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resolución por Derivación")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.func_input = QLineEdit()
        self.x0_input = QLineEdit()
        self.y0_input = QLineEdit()
        self.xf_input = QLineEdit()
        self.dec_input = QLineEdit()
        self.dec_input.setPlaceholderText("(Opcional, por defecto 2)")

        form_layout.addRow("Ecuación f(x, y):", self.func_input)
        form_layout.addRow("x0 (valor inicial de x):", self.x0_input)
        form_layout.addRow("y0 (valor inicial de y):", self.y0_input)
        form_layout.addRow("x final:", self.xf_input)
        form_layout.addRow("Decimales:", self.dec_input)

        layout.addLayout(form_layout)

        self.solve_btn = QPushButton("Resolver")
        self.solve_btn.clicked.connect(self.on_resolve_clicked)
        layout.addWidget(self.solve_btn)

        self.setLayout(layout)

    def on_resolve_clicked(self):
        try:
            f_expr = self.func_input.text().strip()
            x0 = float(self.x0_input.text().strip())
            y0 = float(self.y0_input.text().strip())
            xf = float(self.xf_input.text().strip())
            dec = self.dec_input.text().strip()
            dec = int(dec) if dec else 2

            if not f_expr:
                raise ValueError("La ecuación no puede estar vacía.")

            # x_vals, y_vals, solucion = resolver_por_derivacion(f_expr, x0, y0, xf)
            ###
            try:
                x_vals, y_vals, solucion = resolver_por_derivacion(f_expr, x0, y0, xf)
                # Mostrar resultados solo si la solución es numérica
                if isinstance(y_vals[-1], (float, int)):
                    QMessageBox.information(self, "Solución Analítica",
                        f"La solución simbólica de la ecuación es:\n{solucion}\n\n"
                        f"Valor aproximado en x = {x_vals[-1]:.{dec}f}: y = {y_vals[-1]:.{dec}f}")
                    
                    plt.plot(x_vals, y_vals, label='Solución Analítica')
                    plt.title(f"Solución de y' = {f_expr} por Derivación")
                    plt.xlabel("x")
                    plt.ylabel("y")
                    plt.grid(True)
                    plt.legend()
                    plt.show()
                else:
                    QMessageBox.information(self, "Solución Analítica",
                        f"La solución simbólica de la ecuación es:\n{solucion}\n\n"
                        "La solución no es numéricamente evaluable en el rango dado.")
            except Exception as e:
                QMessageBox.critical(self, "Error de entrada", str(e))
            ###


            plt.plot(x_vals, y_vals, label='Solución Analítica')
            plt.title(f"Solución de y' = {f_expr} por Derivación")
            plt.xlabel("x")
            plt.ylabel("y")
            plt.grid(True)
            plt.legend()
            plt.show()

        except Exception as e:
            QMessageBox.critical(self, "Error de entrada", str(e))


class SelectorMetodoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seleccionar método de resolución")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        label = QLabel("Selecciona el método de resolución:")
        label.setAlignment(Qt.AlignCenter)

        self.interpolacion_btn = QPushButton("Método por Interpolación")
        self.derivacion_btn = QPushButton("Método por Derivación")

        self.interpolacion_btn.clicked.connect(self.lanzar_interpolacion)
        self.derivacion_btn.clicked.connect(self.lanzar_derivacion)

        layout.addWidget(label)
        layout.addWidget(self.interpolacion_btn)
        layout.addWidget(self.derivacion_btn)

        self.setLayout(layout)

    def lanzar_interpolacion(self):
        self.euler_window = EulerInputWindow()
        self.euler_window.show()
        self.close()

    def lanzar_derivacion(self):
        self.derivacion_window = DerivacionWindow()
        self.derivacion_window.show()
        self.close()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    selector = SelectorMetodoWindow()
    selector.show()
    sys.exit(app.exec_())
