from math import exp as num_exp
from matplotlib import pyplot as plt
import numpy as np
from sympy import exp as sym_exp

from newton import newton_step

def solve_eq1():

    a, b, l = (10, 10, 1)

    def f(x):
        return a * x * num_exp(b * x) - l

    def df(x):
        return a * num_exp(b * x) * (1 + b * x)

    def f_sym(x):
        return a * x * sym_exp(b * x) - l

    sol_exact = newton_step.exact_roots(1, f_sym)
    print(f"eq1 exact roots: {sol_exact}")

    # graphic for f(x)
    x_plt = np.arange(-10, 1, 0.01)
    f_plt = [f(x_i) for x_i in x_plt]
    plt.plot(x_plt, f_plt)
    plt.axis([-2, 1, -2, 4])
    plt.title(f"F(x)={a}xe^({b}x)-{l}")
    plt.xlabel("x")
    plt.ylabel("F(x)")
    plt.grid()
    plt.show()

    tol_x = 1e-3
    tol_f = 1e-3
    step_max = 100

    x0 = 0
    label = f"M1: x0={x0}"
    newton_step.time_step_dependency(f, df, x0, step_max, tol_x, tol_f, log=True, label=label)

    res_newton = newton_step.newton(f, df, x0, tol_x, tol_f, log=True, label=label)
    print(f"{label}, modif: x = {res_newton[0]}, itr = {res_newton[1]}, "
        f"time = {newton_step.measure_time_newton(f, df, x0, tol_x, tol_f)} ms")

    res_modif = newton_step.modif(f, df, x0, tol_x, tol_f, log=True, label=label)
    print(f"{label}, modif: x = {res_modif[0]}, itr = {res_modif[1]}, "
        f"time = {newton_step.measure_time_modif(f, df, x0, tol_x, tol_f)} ms")

    x0 = 1
    label = f"M1, x0={x0}"
    newton_step.time_step_dependency(f, df, x0, step_max, tol_x, tol_f, log=True, label=label)

    res_newton = newton_step.newton(f, df, x0, tol_x, tol_f, log=True, label=label)
    print(f"{label}, modif: x = {res_newton[0]}, itr = {res_newton[1]}, "
        f"time = {newton_step.measure_time_newton(f, df, x0, tol_x, tol_f)} ms")

    res_modif = newton_step.modif(f, df, x0, tol_x, tol_f, log=True, label=label)
    print(f"{label}, modif: x = {res_modif[0]}, itr = {res_modif[1]}, "
        f"time = {newton_step.measure_time_modif(f, df, x0, tol_x, tol_f)} ms")

def solve_eq2():
    n = 100

    def f(x):
        f = [0] * n
        f[0] = (3 + 2 * x[0]) * x[0] - 2 * x[1] - 3
        f[n - 1] = (3 + 2 * x[n - 1]) * x[n - 1] - x[n - 2] - 4
        for i in range(1, n - 1):
            f[i] = (3 + 2 * x[i]) * x[i] - x[i - 1] - 2 * x[i + 1] - 2

        return f

    def df(x):
        df = [[0] * n for _ in range(n)]
        for i in range(n):
            df[i][i] = 4 * x[i] + 3
            if i > 0:
                df[i][i - 1] = -1
            if i < n - 1:
                df[i][i + 1] = -2

        return df

    # x0 = [0.5] * n
    tol_x = 1e-3
    tol_f = 1e-3
    # step_max = 100
    # label = "M: x0=[0.5]"
    # newton_step.time_step_dependency(f, df, x0, step_max, tol_x, tol_f, log=True, label=label)

    # res_newton = newton_step.newton(f, df, x0, tol_x, tol_f, log=True, label=label)
    # print(f"{label}, modif: x = {res_newton[0]}, itr = {res_newton[1]}, "
    #     f"time = {newton_step.measure_time_newton(f, df, x0, tol_x, tol_f)} ms")

    # res_modif = newton_step.modif(f, df, x0, tol_x, tol_f, log=True, label=label)
    # print(f"{label}, modif: x = {res_modif[0]}, itr = {res_modif[1]}, "
    #     f"time = {newton_step.measure_time_modif(f, df, x0, tol_x, tol_f)} ms")

    x0 = [1.5] * n
    step_max = 9
    label = "M: x0=[1.5]"
    newton_step.time_step_dependency(f, df, x0, step_max, tol_x, tol_f, log=True, label=label)

    res_newton = newton_step.newton(f, df, x0, tol_x, tol_f, log=True, label=label)
    print(f"{label}, modif: x = {res_newton[0]}, itr = {res_newton[1]}, "
        f"time = {newton_step.measure_time_newton(f, df, x0, tol_x, tol_f)} ms")

    res_modif = newton_step.modif(f, df, x0, tol_x, tol_f, log=True, label=label)
    print(f"{label}, modif: x = {res_modif[0]}, itr = {res_modif[1]}, "
        f"time = {newton_step.measure_time_modif(f, df, x0, tol_x, tol_f)} ms")

if __name__ == "__main__":
    # solve_eq1()
    solve_eq2()
