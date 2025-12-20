import numpy as np
import matplotlib.pyplot as plt

x_deg = np.linspace(-360, 360, 1000)
x_rad = np.deg2rad(x_deg)

f = np.exp(np.cos(x_rad)) + np.log(np.cos(0.6 * x_rad)**2 + 1) * np.sin(x_rad)
h = -np.log((np.cos(x_rad) + np.sin(x_rad))**2 + 2.5) + 10

plt.figure(figsize=(10, 6))
plt.plot(x_deg, f, label='f(x)')
plt.plot(x_deg, h, label='h(x)')
plt.title('Графики функций f(x) и h(x)')
plt.xlabel('x (в градусах)')
plt.ylabel('Значение функции')
plt.legend()
plt.grid(True)
plt.show()
