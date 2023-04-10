from scipy import signal
from scipy.fft import fftshift
import matplotlib.pyplot as plt
import numpy as np

def f1(t):
    return np.sin(t**3)

def f2(t):
    return np.cos(2 * np.pi * 10 * t) + np.cos(2 * np.pi * 25 * t) + np.cos(2 * np.pi * 50 * t) + np.cos(2 * np.pi * 100 * t)

fs = 1000
dt = 1 / fs
t = np.arange(0, 2 * np.pi, dt)
x = f1(t)

f, t, Sxx = signal.spectrogram(x, fs, window='parzen')
plt.pcolormesh(t, f, Sxx)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()