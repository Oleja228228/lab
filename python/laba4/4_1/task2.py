import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-10, 10, 1000)
y = 5 / (x**2 - 9)

y[np.abs(x - 3) < 0.001] = np.nan
y[np.abs(x + 3) < 0.001] = np.nan

plt.figure(figsize=(8, 5))
plt.plot(x, y, color='orange')
plt.title('График функции f(x) = 5 / (x² - 9)')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.show()
