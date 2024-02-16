import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np

sample_frequency = 50
samples = 10

df_rank = [0] * 10
dt_rank = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
sr_n = len(df_rank)

plot_all = True

x = []  # delta time (s)
y = []  # delta frequency (Hz)

for _ in range(samples):

    sampFreq, sound = wavfile.read(f'Tapered/sample{_}.wav')

    sound = sound / 2.0**15  # normalize amplitudes

    duration = sound.shape[0] / sampFreq

    x.append(duration)

    complex_spectrum = np.fft.rfft(sound)
    yf = []

    for num in complex_spectrum:
        yf.append(np.abs(num))

    xf = np.fft.rfftfreq(sound.size, d=1.0/sampFreq)

    start = 0

    for i, f in enumerate(xf):
        if f == sample_frequency:
            start = i
            break

    x_lower = start

    while yf[x_lower - 1] < yf[x_lower]:
        x_lower -= 1

    x_upper = start

    while yf[x_upper + 1] < yf[x_upper]:
        x_upper += 1

    dx = xf[x_upper] - xf[x_lower]

    y.append(dx)

    print(f"---sample {_}---")
    print(f"sample frequency: {sampFreq}Hz")
    print(f"duration: {duration}s")
    print(f"dx: {dx}Hz")

    if plot_all:
        plt.figure(f"sample {_+1}")

        sound_samples = np.arange(len(sound))

        plt.subplot(2, 1, 1)
        plt.plot(sound_samples/sampFreq, sound)
        plt.xlabel("t(s)")

        plt.subplot(2, 1, 2)
        plt.plot(xf, yf, xf[x_lower], yf[x_lower], 'or', xf[x_upper], yf[x_upper], 'ob')
        plt.xlim(0, 300)
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")

d_i = 0

highest = 0
for i in range(10, 0, -1):
    for j in range(0, 10):
        if y[j] > y[highest]:
            highest = i


for i in range(sr_n):
    d_i += (df_rank[i] - dt_rank[i])**2

spearman_rank = 1 - (6 * d_i) / (sr_n * (sr_n**2 - 1))

print("Rs:", spearman_rank)


x2 = np.linspace(0.000001, 1.000001)

plt.figure("Results", facecolor="#EEEEEE")
plt.title(r"Uncertainty in Frequency for Sounds with Different Durations",
          fontname="Times New Roman",
          weight="bold",
          fontsize=18,
          pad=20)
plt.xlabel(r"Sound Duration $\Delta$t(s)", weight="bold", bbox=dict(facecolor="#FBE4D5"))
plt.ylabel(r"Uncertainty in Frequency $\Delta$f(Hz)", weight="bold", bbox=dict(facecolor="#D9E2F3"))
plt.xlim(0, 1)
plt.ylim(0, 50)
plt.xticks(np.arange(0, 1.1, 0.1))
plt.plot(x, y, 'or')
plt.plot(x2, 4.0 / x2, label=r'$\frac{4}{\Delta t}$')

plt.legend(fontsize="15")
plt.grid()

plt.show()
