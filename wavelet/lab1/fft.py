import numpy as np
from scipy.fft import fft
from matplotlib import pyplot as plt

def gaussianFft(a, b, fs):
    dt = 1 / fs
    t = np.arange(a, b + dt, dt)

    x = np.exp(-t**2/2)
    y = fft(x)

    n = len(x)
    f = np.arange(0,n)*(fs/n)
    power = np.abs(y)**2/n

    fig, [ax1, ax2] = plt.subplots(nrows=2, ncols=1)
    ax1.set_title("Gaussian (dt=%s)" % dt)
    ax1.set_xlabel("Time(t)")
    ax1.set_ylabel("f(t)")
    ax1.plot(t, x)
    ax2.set_title("Amplitude Spectrum of Gaussian")
    ax2.set_xlabel("Frequency")
    ax2.set_ylabel("Power")
    ax2.plot(f, power)
    plt.subplots_adjust(wspace=0.5, hspace=0.5)
    plt.show()

def main():
    a = -10
    b = 10
    gaussianFft(a, b, 1)
    gaussianFft(a, b, 10)
    gaussianFft(a, b, 100)

if __name__ == "__main__":
    main()
