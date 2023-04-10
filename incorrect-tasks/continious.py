import numpy as np

N = 2
alpha = 0.1

y0 = np.array([0, 1])
t0 = 2

tamax = 1
e = 0.0000001


def f(t):
    f1 = np.zeros(N, dtype=np.float64)
    f1[0] = 3
    f1[1] = 9 / 2
    f1 += 1 / t ** 0.5
    return f1


def A(t):
    A1 = np.zeros((N, N), dtype=np.float64)
    A1[0][0] = 2
    A1[0][1] = 3
    A1[1][0] = 3
    A1[1][1] = 9 / 2
    A1 += 1 / t ** 0.5
    return A1


def a(t):
    return 1 / t ** alpha


def deriv(yn, tn):
    return f(tn) - a(tn) * yn - np.matmul(A(tn), yn)


def step(yk, tk, tak):
    k1 = tak * deriv(yk, tk)
    k2 = tak * deriv(yk + k1 / 3, tk + tak / 3)
    k3 = tak * deriv(yk + k1 / 6 + k2 / 6, tk + tak / 3)
    k4 = tak * deriv(yk + k1 / 8 + k3 * 3 / 8, tk + tak / 2)
    k5 = tak * deriv(yk + k1 / 2 - k3 * 3 / 2 + k4 * 2, tk + tak)
    return yk + (k1 + 4 * k4 + k5) / 6, norm((-2 * k1 + 9 * k3 - 8 * k4 + k5) / 10)


def norm(m):
    r = 0
    for i in range(N):
        r += m[i] ** 2
    return np.sqrt(r)


def rk4():
    tk = t0
    yk = y0
    tak = 1
    repeat = True
    while repeat:
        ykp1, r = step(yk, tk, tak)
        repeat = False
        if abs(r) > e:
            tak = tak / 2
            repeat = True
            continue
        if abs(r) < e / 30 and tak < tamax:
            tak = tak * 2
            if tak > tamax:
                tak = tamax
    # print(yk, ykp1, norm(yk - ykp1))
    while norm(yk - ykp1) > e:
        # print(yk, ykp1, norm(yk - ykp1))
        yk = ykp1
        tk = tk + tak
        repeat = True
        while repeat:
            ykp1, r = step(yk, tk, tak)
            repeat = False
            if abs(r) > e:
                tak = tak / 2
                repeat = True
                continue
            if abs(r) < e / 30 and tak < tamax:
                tak = tak * 2
                if tak > tamax:
                    tak = tamax
    return ykp1, tk + tak


print("Нормальное решение: [1.2 0.6]")
print("Начальное условие: y({})={}, точность {}".format(t0, y0, e))
alphas = np.linspace(0.3, 0.3, 1)
for alpha in alphas:
    y, t = rk4()
    print("Alpha={:.2f} : решение y={} найдено при t={}".format(alpha, y, t))
