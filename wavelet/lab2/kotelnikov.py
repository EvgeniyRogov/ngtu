import numpy as np
from matplotlib import pyplot as plt

def x(t):
    return np.sin(2 * np.pi * t) + 1 / 2 * np.sin(4 * np.pi * t)

def KotelnikovSeries(N):
    # N - количество слагаемых
    a = 0
    b = 3

    pRef = 5 # Количество точек отсчёта
    k = np.linspace(0, pRef - 1, pRef)
    Ts = 1 / pRef
    td = k * Ts
    xd = x(td)

    dt = 0.01
    t = np.arange(0, 3 + dt, dt)
    x1 = np.zeros(len(t))

    for t_i in range(len(t)):
        for n in range(-N, N + 1):
            if t[t_i] == n * Ts:
                x1[t_i] += xd[n % len(xd)] * 1; # 1 = lim sin(x) / x, x -> 0 
            else:
                x1[t_i] += xd[n % len(xd)] * \
                np.sin(np.pi * (t[t_i] - n * Ts) / Ts) / \
                (np.pi * (t[t_i] - n * Ts) / Ts)

    plt.plot(td, xd, 'o', label='Точки отсчёта')
    plt.plot(t, x(t), label='Исходная функция')
    plt.plot(t, x1, label='Восстановленная функция')
    plt.grid()
    plt.legend()
    plt.title('Восстановление функции с помощью ряда Котельникова(N=%s)' % N)
    plt.xlabel('Time(t)')
    plt.ylabel('x(t)')
    plt.show()

def main():
    KotelnikovSeries(10)
    KotelnikovSeries(20)
    KotelnikovSeries(30)
    KotelnikovSeries(10000)

if __name__ == "__main__":
    main()
