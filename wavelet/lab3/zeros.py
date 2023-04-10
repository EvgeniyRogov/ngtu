import numpy as np
from matplotlib import pyplot as plt
from scipy.fft import fft, ifft

L = 5
N = 5

def x(t):
    return np.sin(2 * np.pi * t) + 1 / 2 * np.sin(4 * np.pi * t)

def O(F, m):
    if m < 0.5 * L:
        return F[m] * np.sqrt(N)
    elif L * N - 0.5 * L <= m:
        return F[(m - L * N) + L] * np.sqrt(N)
    else:
        return 0

def main():
    a = 0
    b = 3

    k = np.linspace(0, L - 1, L).astype('int')
    m = L * N
    M = np.linspace(0, m - 1, m).astype('int')

    Ts = 1 / L
    td = k * Ts
    xd = x(td)
    F = fft(xd)
    print(F)

    FD = np.zeros(m)
    for i in range(m):
        FD[i] = O(F, i)

    AD = ifft(FD)
    print(FD)

    dt = 0.01
    t = np.arange(0, 3 + dt, dt)

    # plt.plot(td, xd, 'o', label='Точки отсчёта')
    # plt.plot(t, x(t), label='Исходная функция')
    # plt.plot(ty, AD, label='Восстановленная функция')
    # plt.grid()
    # plt.legend()
    # plt.xlabel('Time(t)')
    # plt.ylabel('x(t)')
    # plt.show()

if __name__ == "__main__":
    main()
