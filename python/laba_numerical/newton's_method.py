import numpy as np

class NewtonSystemSolver:

    def __init__(self, F, J_analytic=None, eps_f=1e-9, eps_x=1e-9, max_iter=100, jacobian_M=0.01):
        self.F = F
        self.J_analytic = J_analytic
        self.eps_f = eps_f
        self.eps_x = eps_x
        self.max_iter = max_iter
        self.jacobian_M = jacobian_M

    def numeric_jacobian(self, x):
        """Численная матрица Якоби методом конечных разностей (центральные разности)."""
        n = x.size
        J = np.zeros((n, n), dtype=float)
        fx = self.F(x)
        for j in range(n):
            # относительное приращение
            h = self.jacobian_M * max(1.0, abs(x[j]))
            x_plus = x.copy(); x_minus = x.copy()
            x_plus[j] += h
            x_minus[j] -= h
            f_plus = self.F(x_plus)
            f_minus = self.F(x_minus)
            # центральная разность
            J[:, j] = (f_plus - f_minus) / (2.0 * h)
        return J

    def solve(self, x0, verbose=False):
        """
        Выполнить итерации Ньютона от начального приближения x0.
        Возвращает (x, info) где info — словарь с метриками.
        """
        x = np.array(x0, dtype=float)
        n = x.size
        history = []

        for k in range(1, self.max_iter + 1):
            Fx = self.F(x)
            delta_f = np.max(np.abs(Fx))  # критерий 1: макс невязка
            # выбрать Якоби
            if self.J_analytic is not None:
                J = self.J_analytic(x)
            else:
                J = self.numeric_jacobian(x)

            # решить J * dx = -F
            try:
                dx = np.linalg.solve(J, -Fx)
            except np.linalg.LinAlgError:
                return None, {"status": "singular_jacobian", "iter": k, "x": x, "Fx": Fx}

            # критерий на изменение x: воспользуемся относительным правилом
            # δ2 = max_i |Δx_i| / max(1, |x_i|)
            rel_change = np.max(np.abs(dx) / np.maximum(1.0, np.abs(x)))

            # обновление
            x = x + dx

            history.append({"iter": k, "x": x.copy(), "norm_F": delta_f, "rel_change": rel_change})

            if verbose:
                print(f"iter={k:3d}  ||F||_max={delta_f:.3e}  rel_change={rel_change:.3e}")

            # критерии остановки (см. условие в методичке: одновременно по F и по Δx)
            if delta_f <= self.eps_f and rel_change <= self.eps_x:
                return x, {"status": "converged", "iter": k, "x": x, "history": history}

        # если не сошлось за max_iter
        return x, {"status": "no_convergence", "iter": self.max_iter, "x": x, "history": history}

# -------------------------
# Пример использования:
# -------------------------
if __name__ == "__main__":
    def F_example(v):
        x, y = v
        return np.array([x**2 + y**2 - 4.0,
                         np.exp(x) + y - 1.0])

    # Аналитическая Якоби для примера:
    def J_example(v):
        x, y = v
        return np.array([[2*x,      2*y],
                         [np.exp(x), 1.0]])

    x0 = np.array([1.0, 1.0])  # начальное приближение

    # Вариант A: аналитическая Якоби
    solverA = NewtonSystemSolver(F_example, J_analytic=J_example, eps_f=1e-9, eps_x=1e-9, max_iter=50)
    solA, infoA = solverA.solve(x0, verbose=True)
    print("Analytic J result:", infoA["status"], "iter:", infoA.get("iter"), "x:", infoA.get("x"))

    # Вариант B: численный Якоби (с M = 0.01)
    solverB = NewtonSystemSolver(F_example, J_analytic=None, jacobian_M=0.01, eps_f=1e-9, eps_x=1e-9, max_iter=50)
    solB, infoB = solverB.solve(x0, verbose=True)
    print("Numeric J result:", infoB["status"], "iter:", infoB.get("iter"), "x:", infoB.get("x"))
