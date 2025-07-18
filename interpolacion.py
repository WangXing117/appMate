import numpy as np
from scipy.interpolate import lagrange

# interpolacion.py
import numpy as np
from scipy.interpolate import lagrange

def euler(f, x0, y0, h, n):
    x_vals = [x0]
    y_vals = [y0]
    for _ in range(n):
        y0 = y0 + h * f(x0, y0)
        x0 = x0 + h
        x_vals.append(x0)
        y_vals.append(y0)
    return np.array(x_vals), np.array(y_vals)

def interpolar_lagrange(x_vals, y_vals):
    return lagrange(x_vals, y_vals)  
