# lab2_task1_newton_final.py
import numpy as np

class NewtonSystemSolver:
    def __init__(self, F, J_analytic=None, eps_f=1e-9, eps_x=1e-9,
                 max_iter=200, jacobian_M=0.01,
                 min_alpha=1e-4, alpha_factor=0.5):
        self.F = F
        self.J_analytic = J_analytic
        self.eps_f = eps_f
        self.eps_x = eps_x
        self.max_iter = max_iter
        self.jacobian_M = jacobian_M
        self.min_alpha = min_alpha
        self.alpha_factor = alpha_factor

    def numeric_jacobian(self, x):
        n = x.size
        J = np.zeros((n, n))
        for j in range(n):
            h = self.jacobian_M * max(1.0, abs(x[j]))
            x_plus, x_minus = x.copy(), x.copy()
            x_plus[j] += h
            x_minus[j] -= h
            f_plus, f_minus = self.F(x_plus), self.F(x_minus)
            if np.any(np.isnan(f_plus)) or np.any(np.isnan(f_minus)):
                return np.full((n, n), np.nan)
            J[:, j] = (f_plus - f_minus) / (2.0 * h)
        return J

    def solve(self, x0, verbose=True):
        x = np.array(x0, dtype=float)
        history = []

        for k in range(1, self.max_iter + 1):
            Fx = self.F(x)
            if np.any(np.isnan(Fx)) or np.any(np.isinf(Fx)):
                print(" Недопустимое значение F (log отриц.) на итерации", k)
                return None, {"status": "invalid_F", "iter": k, "x": x, "history": history}

            delta_f = np.max(np.abs(Fx))  # δ1

            J = self.J_analytic(x) if self.J_analytic is not None else self.numeric_jacobian(x)
            if np.any(np.isnan(J)) or np.any(np.isinf(J)):
                return None, {"status": "invalid_J", "iter": k, "x": x, "history": history}

            try:
                dx = np.linalg.solve(J, -Fx)
            except np.linalg.LinAlgError:
                return None, {"status": "singular_J", "iter": k, "x": x, "history": history}

            rel_change = np.max(np.abs(dx) / np.maximum(1.0, np.abs(x)))  # δ2

            # backtracking — уменьшаем шаг, если log(x2+1.5) становится недопустим
            alpha = 1.0
            while alpha >= self.min_alpha:
                x_try = x + alpha * dx
                Fx_try = self.F(x_try)
                if not (np.any(np.isnan(Fx_try)) or np.any(np.isinf(Fx_try))):
                    break
                alpha *= self.alpha_factor

            if alpha < self.min_alpha:
                print(" Не удалось подобрать шаг на итерации", k)
                return None, {"status": "line_search_failed", "iter": k, "x": x, "history": history}

            x = x + alpha * dx
            history.append({"iter": k, "x": x.copy(), "δ1": delta_f, "δ2": rel_change})

            if verbose:
                print(f"{k:3d}: δ1={delta_f:.3e}  δ2={rel_change:.3e}  α={alpha:.2f}  x={x}")

            # условие остановки
            if delta_f <= self.eps_f and rel_change <= self.eps_x:
                return x, {"status": "converged", "iter": k, "x": x, "history": history}

        return x, {"status": "no_convergence", "iter": self.max_iter, "x": x, "history": history}


# --- Лабораторная №2, Задача №1 ---

def F_task1(v):
    x1, x2 = v
    if x2 + 1.5 <= 0:  # защита от log отрицательного
        return np.array([np.nan, np.nan])
    return np.array([
        np.log(x2 + 1.5) + x1 - 0.5,
        x2 - 6 * np.cos(x1 + 3)
    ])

def J_task1(v):
    x1, x2 = v
    return np.array([
        [1.0, 1.0 / (x2 + 1.5)],
        [6 * np.sin(x1 + 3), 1.0]
    ])


if __name__ == "__main__":
    x0 = np.array([1.0, 1.0])  # начальное приближение из таблицы 2.1

    solver = NewtonSystemSolver(F_task1, J_analytic=J_task1,
                                eps_f=1e-9, eps_x=1e-9,
                                max_iter=200, jacobian_M=0.01)

    sol, info = solver.solve(x0, verbose=True)

    if info["status"] == "converged":
        print("\n Метод сошёлся")
        print("Итераций:", info["iter"])
        print("x* =", info["x"])
        print("F(x*) =", F_task1(info["x"]))
    else:
        print("\n️ Метод не сошёлся:", info["status"])
