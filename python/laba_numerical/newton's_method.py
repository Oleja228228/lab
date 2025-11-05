import math
import numpy as np

# --- Вектор функций системы (пример: задача №1 из таблицы 2.1) ---
def f_vec(x):
    x1, x2 = x[0], x[1]
    arg = 1.0 + (x1 + x2) / 5.0
    if arg <= 0:
        # защита: если логарифм не определён, возвращаем большую невязку
        return np.array([1e6, 1e6], dtype=float)
    f1 = math.log(arg) - math.sin(x2 / 3.0) - x1 + 1.1
    f2 = math.cos((x1 * x2) / 6.0) - x2 + 0.5
    return np.array([f1, f2], dtype=float)


# --- Аналитический Якобиан ---
def J_analytic(x):
    x1, x2 = x[0], x[1]
    denom = 5.0 + x1 + x2
    if abs(denom) < 1e-16:
        denom = 1e-16
    df1_dx1 = 1.0 / denom - 1.0
    df1_dx2 = 1.0 / denom - (1.0 / 3.0) * math.cos(x2 / 3.0)
    df2_dx1 = - (x2 / 6.0) * math.sin((x1 * x2) / 6.0)
    df2_dx2 = - (x1 / 6.0) * math.sin((x1 * x2) / 6.0) - 1.0
    return np.array([[df1_dx1, df1_dx2],
                     [df2_dx1, df2_dx2]], dtype=float)


# --- Численный Якобиан (центральная разность) ---
def J_numeric(x, M):
    n = len(x)
    J = np.zeros((n, n), dtype=float)
    for j in range(n):
        dx = M * max(abs(x[j]), 1.0)
        if dx == 0:
            dx = 1e-12
        xp = x.copy()
        xm = x.copy()
        xp[j] += dx
        xm[j] -= dx
        fp = f_vec(xp)
        fm = f_vec(xm)
        J[:, j] = (fp - fm) / (2.0 * dx)
    return J


# --- Метод Гаусса с выбором главного элемента ---
def gauss_solve(A, b):
    A = A.astype(float).copy()
    b = b.astype(float).copy()
    n = len(b)

    for k in range(n):
        # выбор главного элемента
        max_row = k + np.argmax(np.abs(A[k:, k]))
        if abs(A[max_row, k]) < 1e-14:
            raise ZeroDivisionError("Нулевой ведущий элемент")

        if max_row != k:
            A[[k, max_row]] = A[[max_row, k]]
            b[[k, max_row]] = b[[max_row, k]]

        for i in range(k + 1, n):
            m = A[i, k] / A[k, k]
            A[i, k:] -= m * A[k, k:]
            b[i] -= m * b[k]

    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        s = np.dot(A[i, i + 1:], x[i + 1:])
        x[i] = (b[i] - s) / A[i, i]

    return x


# --- Метод Ньютона ---
def newton_method(x0, J_mode='analytic', M=0.01, eps1=1e-9, eps2=1e-9, max_iter=100):
    x = np.array(x0, dtype=float)
    print()
    if J_mode == 'analytic':
        print("МЕТОД НЬЮТОНА — АНАЛИТИЧЕСКИЙ ЯКОБИАН")
    else:
        print(f"МЕТОД НЬЮТОНА — ЧИСЛЕННЫЙ ЯКОБИАН, M = {M}")

    print(" k |      x1       |      x2       |      f1      |      f2      |     Δx1      |     Δx2      |   δ1=||F||∞  |   δ2=||Δx||∞")
    print("-" * 120)

    for k in range(1, max_iter + 1):
        F = f_vec(x)
        J = J_analytic(x) if J_mode == 'analytic' else J_numeric(x, M)

        detJ = np.linalg.det(J)
        if abs(detJ) < 1e-12:
            print(f"ПРЕРВАНО: Вырожденный Якобиан (det = {detJ:.2e}) на итерации {k}")
            return x, k

        delta = gauss_solve(J, -F)
        x_new = x + delta

        # δ1 и δ2 по формулам (2.4)
        delta1 = np.max(np.abs(F))
        delta2 = np.max(np.abs(delta) / np.maximum(np.abs(x_new), 1.0))

        print(f"{k:2d} | {x_new[0]: .10f} | {x_new[1]: .10f} | {F[0]: .4e} | {F[1]: .4e} | {delta[0]: .4e} | {delta[1]: .4e} | {delta1: .4e} | {delta2: .4e}")

        # критерий остановки
        if delta1 < eps1 and delta2 < eps2:
            print("-" * 120)
            print(f"СОШЛОСЬ за {k} итераций: x1 = {x_new[0]:.10f}, x2 = {x_new[1]:.10f}, ||F||∞ = {delta1:.3e}")
            return x_new, k

        x = x_new

    print("-" * 120)
    print(f"Не сошлось за {max_iter} итераций. Последнее приближение: x1 = {x[0]:.10f}, x2 = {x[1]:.10f}, ||F||∞ = {np.max(np.abs(f_vec(x))):.3e}")
    return x, max_iter


# --- Основная программа ---
def main():
    x0 = [8.0, 8.0]     # начальное приближение
    eps1 = 1e-9
    eps2 = 1e-9
    max_iter = 50

    # Аналитический Якобиан
    newton_method(x0, J_mode='analytic', eps1=eps1, eps2=eps2, max_iter=max_iter)

    # Численный Якобиан для разных M
    for M in [0.01, 0.05, 0.1]:
        newton_method(x0, J_mode='numeric', M=M, eps1=eps1, eps2=eps2, max_iter=max_iter)


if __name__ == "__main__":
    main()
