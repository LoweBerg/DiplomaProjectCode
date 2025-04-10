import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import stats
import numpy as np
import xlsxwriter as xl

sample_frequency = 50
samples = 50

df_rank = [0] * 10
dt_rank = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
sr_n = len(df_rank)

plot_all = False

x = []  # delta time (s)
y = []  # delta frequency (Hz)
xf = []
yf = []


for _ in range(samples):

    sampFreq, sound = wavfile.read(f'newSine/sample{_+1}.wav')

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
        if round(f) == sample_frequency:
            start = i
            break

    x_lower = start

    while yf[x_lower - 1] < yf[x_lower]:
        x_lower -= 1

    x_upper = start

    while yf[x_upper + 1] < yf[x_upper]:
        x_upper += 1

    if x_lower == 0:
        dx = (xf[x_upper] - xf[start]) * 2
    else:
        dx = xf[x_upper] - xf[x_lower]

    y.append(dx)

    print(f"---sample {_+1}---")
    print(f"sample frequency: {sampFreq}Hz")
    print(f"duration: {duration}s")
    print(f"dx: {dx}Hz")

    if plot_all or x_lower < 0:
        plt.figure(f"sample {_+1}", facecolor="#EEEEEE", figsize=(8, 3))
        plt.title(f"Sample {_+1} Fourier Transform",
                  fontname="Times New Roman",
                  weight="bold",)

        # sound_samples = np.arange(len(sound))

        # plt.subplot(2, 1, 1)
        # plt.plot(sound_samples/sampFreq, sound)
        # plt.xlabel("t(s)")

        # plt.subplot(2, 1, 2)
        plt.plot(xf, yf, xf[x_lower], yf[x_lower], 'or', xf[x_upper], yf[x_upper], 'ob')
        plt.xlim(0, 300)
        plt.xlabel("Frequency (Hz)", labelpad=10)
        plt.ylabel("Relative Amplitude")
        plt.tight_layout()

# noinspection PyTypeChecker
rank_coef, p_value = stats.spearmanr(x[1:], y[1:])  # first sample will be ignored as an outlier

print("Rs:", rank_coef)

# writing to excel sheet
workbook = xl.Workbook("C:/Users/loweb/DiplomaProject/test.xlsx")
worksheet = workbook.add_worksheet()
worksheet.write_row(1, 1, x)
worksheet.write_row(2, 1, y)
workbook.close()


x2 = np.linspace(0, 1.1, 100)
x2 = x2[1:]

plt.figure("Results", facecolor="#EEEEEE")
plt.title(r"Uncertainty in Frequency for Sounds with Different Durations",
          fontname="Times New Roman",
          weight="bold",
          fontsize=18,
          pad=20)
plt.xlabel(r"Sound Duration $\Delta$t(s)", weight="bold", bbox=dict(facecolor="#FBE4D5"))
plt.ylabel(r"Uncertainty in Frequency $\Delta$f(Hz)", weight="bold", bbox=dict(facecolor="#D9E2F3"))
plt.xlim(0, 1.1)
plt.ylim(0, 110)
plt.xticks(np.arange(0, 1.1, 0.1))
plt.plot(x, y, 'or')
plt.plot(x2, 4.0 / x2, label=r'$\frac{4}{\Delta t}$')

plt.legend(fontsize="15")
plt.grid()

plt.show()
