from matplotlib import pyplot as plt
import numpy as np
from newton import shooting_bvp

def solve_bvp1():

    # bvp1:
    # x''=tx^2-t^3, 0 < t < 1
    # x(0)=0, x(1)=0
    # x1(t), x2(t) при x0(t)=0

    a, b = 0, 1
    A, B = 0, 0
    t = np.linspace(a, b, 1000)

    x_lin1 = (t - t**5) / 20
    x_lin2 = t * (15 * t**12 - 65 * t**8 - 46683 * t**4 + 46733) / 936000

    def odes(t, x):
        return [x[1], t * x[0]**2 - t**3, x[3], 2 * t * x[0] * x[2]]

    sol = shooting_bvp.shooting_bvp(odes, t, t_span=(a, b), x_init=(A, B), s0=0)
    x = sol[0]

    print(f"bvp1: s = {sol[1]}, itr = {sol[2]}")

    plt.plot(t, x_lin1)
    plt.plot(t, x_lin2)
    plt.plot(t, x)
    plt.title(f"B1: x''=tx^2-t^3, x({a})={A}, x({b})={B}")
    plt.xlabel("t")
    plt.ylabel("x")
    plt.legend(["x1(t)", "x2(t)", "x(t)"])
    plt.grid()
    plt.show()

    # linear bvp1 (x0(t)=t):
    # x1''=2t^2x1-2t^3, -1 < t < 1
    # x1(-1)=0, x1(1)=0

    def odes_lin1(t, x):
        return [x[1], 2 * t**2 * x[0] - 2 * t**3, x[3], 2 * t**2 * x[2]]

    sol_bvp_lin1 = shooting_bvp.shooting_bvp(odes_lin1, t, t_span=(a, b), x_init=(A, B), s0=0)
    x_lin1 = sol_bvp_lin1[0]

    print(f"bvp1 lin1: s = {sol_bvp_lin1[1]}, itr = {sol_bvp_lin1[2]}")

    plt.plot(t, x_lin1)
    plt.plot(t, x)
    plt.title(f"B1: x''=tx^2-t^3, x({a})={A}, x({b})={B}")
    plt.xlabel("t")
    plt.ylabel("x")
    plt.legend(["x1(t)", "x(t)"])
    plt.grid()
    plt.show()

def solve_bvp2():

    # bvp2:
    # x''=1-x^2-2(1-t^2)x, -1 < t < 1
    # x(-1) = 0, x(-1) = 0

    a, b = -1, 1
    A, B = 0, 0
    t = np.linspace(a, b, 1000)

    def odes(t, x):
        return [x[1], 1 - x[0]**2 - 2 * (1 - t**2) * x[0], x[3], (-2 * x[0] - 2 * (1 - t**2)) * x[3]]

    sol = shooting_bvp.shooting_bvp(odes, t, t_span=(a, b), x_init=(A, B), s0=0)
    x = sol[0]

    print(f"bvp2: s = {sol[1]}, itr = {sol[2]}")

    # x0(t) = t^2-1
    x_lin1 = 1 / 30 * (t**6 - 5 * t**4 + 30 * t**2 - 26)

    plt.plot(t, x_lin1)
    plt.plot(t, x)
    plt.title("B: x0(t) = t^2-1")
    plt.xlabel("t")
    plt.ylabel("x")
    plt.legend(["x1(t)", "x(t)"])
    plt.grid()
    plt.show()

    # linear bvp2 (x0(t)=0):
    # x1''=1-2(1-t^2)x1, -1 < t < 1
    # x1(-1) = 0, x1(1) = 1
    def odes_lin1(t, x):
        return [x[1], 1 - 2 * (1 - t**2) * x[0], x[3], -2 * (1 - t**2) * x[3]]

    sol_lin1 = shooting_bvp.shooting_bvp(odes_lin1, t, t_span=(a, b), x_init=(A, B), s0=0) # x0(t)=0
    x_lin1 = sol_lin1[0]

    print(f"bvp2 lin 1: s = {sol_lin1[1]}, itr = {sol_lin1[2]}")

    plt.plot(t, x_lin1)
    plt.plot(t, x)
    plt.title("B: x0(t)=0")
    plt.xlabel("t")
    plt.ylabel("x")
    plt.legend(["x1(t)", "x(t)"])
    plt.grid()
    plt.show()

if __name__ == "__main__":
    # solve_bvp1()
    solve_bvp2()
