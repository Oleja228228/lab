import numpy as np

A = np.array([
    [-2.0, -8.5, -3.4,  3.5],
    [ 0.0,  2.4,  0.0,  8.2],
    [ 2.5,  1.6,  2.1,  3.0],
    [ 0.3, -0.4, -4.8,  4.6]
])
b = np.array([-1.88, -3.28, -0.5, -2.83])

x = np.linalg.solve(A, b)
print(np.round(x,1))
