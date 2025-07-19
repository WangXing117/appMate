import numpy as np
from sympy import symbols, Eq, Function, dsolve, Derivative, sympify, lambdify

def resolver_por_derivacion(f_expr_str, x0, y0, xf, num_puntos=100):
    x = symbols('x')
    y = Function('y')(x)  # ¡Importante! Definir y como función de x

    try:
        # Convertir string a expresión simbólica (reemplazar ^ por **)
        f_expr_str = f_expr_str.replace('^', '**')
        f_expr = sympify(f_expr_str)
        
        # Reemplazar 'y' por y(x) en la expresión
        if 'y' in f_expr_str:
            y_sym = Function('y')(x)
            f_expr = f_expr.subs('y', y_sym)

        # Definir la ecuación diferencial: dy/dx = f(x, y)
        edo = Eq(Derivative(y, x), f_expr)

        # Resolver simbólicamente con condición inicial
        solucion = dsolve(edo, y, ics={y.subs(x, x0): y0})

        # Convertir la solución en una función numérica
        y_sol = solucion.rhs
        y_func = lambdify(x, y_sol, modules=['numpy'])

        # Evaluar en los puntos deseados
        x_vals = np.linspace(x0, xf, num_puntos)
        y_vals = y_func(x_vals)

        return x_vals, y_vals, str(solucion)

    except Exception as e:
        raise ValueError(f"Error al resolver por derivación: {e}")