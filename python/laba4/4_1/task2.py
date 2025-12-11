import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-10, 10, 1000)

mask1 = x < -3
mask2 = (x > -3) & (x < 3)
mask3 = x > 3

def f(x):
    return 5 / (x**2 - 9)

plt.figure(figsize=(8, 5))

plt.plot(x[mask1], f(x[mask1]), color='orange')
plt.plot(x[mask2], f(x[mask2]), color='orange')
plt.plot(x[mask3], f(x[mask3]), color='orange')

plt.title('График функции f(x) = 5 / (x² - 9)')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.show()
