import numpy as np
from scipy import integrate

f = lambda x: x**2 * np.sin(x)

I1, err1 = integrate.quad(f, 0, np.pi)
print(f"Определённый интеграл ∫(x^2 * sin(x)) dx от 0 до π = {I1:.4f}")

g = lambda y, x: x * y  
I2, err2 = integrate.dblquad(g, 0, 2, lambda x: 0, lambda x: 3)
print(f"Двойной интеграл ∬(x*y) dx dy, x∈[0,2], y∈[0,3] = {I2:.4f}")
