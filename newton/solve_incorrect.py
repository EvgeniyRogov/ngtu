from matplotlib import pyplot as plt
import numpy as np

from newton import newton_reg
from newton.newton_step import exact_roots

def solve_incorrect1():

    def A(x):
        if x < 0:
            return 0
        return x / (1 + x)

    def dA(x):
        if x < 0:
            return 0
        return 1 / (1 + x)**2

    f0 = 0.9

    def F_sym(x):
        return x / (1 + x) - f0

    # graphic Ax
    def gr_Ax():
        x_plt = np.arange(-5, 20, 0.01)
        y_plt = [A(x_i) for x_i in x_plt]
        plt.plot(x_plt, y_plt)
        plt.title('Ax = {x / (1 + x), x>=0; 0, x<0}')
        plt.xlabel('x')
        plt.ylabel('Ax')
        plt.grid()
        plt.show()

    # gr_Ax()

    sol_exact = exact_roots(1, F_sym)
    print(f"E1 exact roots: {sol_exact}")

    t0 = 1
    x0 = 0
    dt = 1e-3
    tol = 1e-3
    b0, a0, g0 = 5, 4.5, 0
    coords=[[], []]

    sol_reg = newton_reg.solve_pertubed_right(A, dA, f0, t0, x0, params=(b0, a0, g0), dt=dt, tol=tol, coords=coords, log=False)
    print(f"E1(f0={f0}, t0={t0}, x0={x0}, b0={b0}, a0={a0}, g0={g0}): "
        f"x = {sol_reg[0]}, t = {sol_reg[1]}, itr = {sol_reg[2]}")

    plt.title(f"E1(f0={f0}, t0={t0}, x0={x0}, b0={b0}, a0={a0}, g0={g0})")
    plt.xlabel("t")
    plt.ylabel("x")
    plt.plot(*coords)
    plt.grid()
    plt.show()

    # t0 = 1
    # x0 = 2
    # b0, a0, g0 = 1, 0.99, 0
    # dt = 1e-3
    # tol = 1e-3
    # coords=[[], []]

    # sol_reg = newton_reg.solve_pertubed_right(A, dA, f0, t0, x0, params=(b0, a0, g0), dt=dt, tol=tol, coords=coords, log=False)
    # print(f"E1(f0={f0}, t0={t0}, x0={x0}, b0={b0}, a0={a0}, g0={g0}): "
    #     f"x = {sol_reg[0]}, t = {sol_reg[1]}, itr = {sol_reg[2]}")

    # plt.title(f"E1(f0={f0}, t0={t0}, x0={x0}, b0={b0}, a0={a0}, g0={g0})")
    # plt.xlabel("t")
    # plt.ylabel("x")
    # plt.plot(*coords)
    # plt.grid()
    # plt.show()

    # def A_pertubed(t, x, h0):
    #     if x < 0:
    #         return 0
    #     return x / ((1 + t**-h0) + (1 + t**-h0) * x)

    # def dA_pertubed(t, x, h0):
    #     if x < 0:
    #         return 0
    #     return 1 / ((1 + t**-h0) + (1 + t**-h0) * x)**2

    # t0 = 1
    # x0 = 9.5
    # b0, a0, g0, h0 = 0.02, 0.01, 0, 0.01
    # dt = 1e-4
    # tol = 1e-1
    # coords=[[], []]

    # sol_reg = newton_reg.solve_pertubed_operator(A_pertubed, dA_pertubed,
    #             f0, t0, x0, params=(b0, a0, g0, h0), dt=dt, tol=tol, coords=coords, log=True)
    # print(f"E2(t0={t0}, x0={x0}, b0={b0}, a0={a0}, g0={g0}, h0={h0}): "
    #     f"x = {sol_reg[0]}, t = {sol_reg[1]}, itr = {sol_reg[2]}")


if __name__ == "__main__":
    solve_incorrect1()
