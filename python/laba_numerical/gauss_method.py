def gauss_elimination(A, b):
    n = len(b)
    A = [row[:] for row in A]
    b = b[:]

    # Прямой ход
    for k in range(n - 1):
        # выбор ведущего элемента
        max_row = max(range(k, n), key=lambda i: abs(A[i][k]))
        if abs(A[max_row][k]) < 1e-18:
            raise ValueError("Матрица вырождена!")

        # перестановка строк
        if max_row != k:
            A[k], A[max_row] = A[max_row], A[k]
            b[k], b[max_row] = b[max_row], b[k]

        # исключение
        for i in range(k + 1, n):
            factor = A[i][k] / A[k][k]
            for j in range(k, n):
                A[i][j] -= factor * A[k][j]
            b[i] -= factor * b[k]

    # Обратный ход
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = sum(A[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (b[i] - s) / A[i][i]
    return x


def residual(A, x, b):
    n = len(A)
    r = [sum(A[i][j] * x[j] for j in range(n)) - b[i] for i in range(n)]
    norm_inf = max(abs(ri) for ri in r)
    return r, norm_inf


def relative_error(x_ref, x_test):
    num = max(abs(x_ref[i] - x_test[i]) for i in range(len(x_ref)))
    den = max(abs(xi) for xi in x_test)
    return num / den if den != 0 else float('inf')


def fmt_vec(v, prec=6):
    return "[" + ", ".join(f"{val:.{prec}g}" for val in v) + "]"


if __name__ == "__main__":
    A1 = [[6, 13, -17],
          [13, 29, -38],
          [-17, -38, 50]]
    b1 = [2, 1, 1]

    x1 = gauss_elimination(A1, b1)
    r1, norm_r1 = residual(A1, x1, b1)

    b1_aux = [sum(A1[i][j] * x1[j] for j in range(3)) for i in range(3)]
    x1_aux = gauss_elimination(A1, b1_aux)
    rel_err1 = relative_error(x1, x1_aux)

    print("=== Задача 1 ===")
    print("x =", fmt_vec(x1))
    print("невязка =", fmt_vec(r1))
    print("||r||∞ =", f"{norm_r1:.3e}")
    print("x_aux =", fmt_vec(x1_aux))
    print("δ =", f"{rel_err1:.3e}")
