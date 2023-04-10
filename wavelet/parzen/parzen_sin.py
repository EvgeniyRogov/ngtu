from scipy import signal
from scipy.fftpack import fft, fftshift
import matplotlib.pyplot as plt
import numpy as np

def f(t):
    return np.sin(t**3)

def h(t):
    return np.cos(2 * np.pi * 10 * t) + np.cos(2 * np.pi * 25 * t) + np.cos(2 * np.pi * 50 * t) + np.cos(2 * np.pi * 100 * t)

t = np.linspace(0, 1, 5000)
window = h(t)
plt.plot(t, window)
plt.title("Parzen window")
plt.ylabel("Amplitude")
plt.xlabel("Sample")

# plt.figure()
# A = fft(window, 2048) / (len(window)/2.0)
# freq = np.linspace(-0.5, 0.5, len(A))
# response = 20 * np.log10(np.abs(fftshift(A / abs(A).max())))
# plt.plot(freq, response)
# plt.axis([-0.5, 0.5, -40, 0])
# plt.title("Frequency response of the Parzen window")
# plt.ylabel("Normalized magnitude [dB]")
# plt.xlabel("Normalized frequency [cycles per sample]")
plt.show()