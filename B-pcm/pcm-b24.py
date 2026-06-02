import numpy as np
from scipy.fftpack import fft, fftfreq, rfft
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import pandas as pd

IMAGE_SIZE = (10, 3.5)
SHOW_IMAGES = False


def main(): 
    # read csv to dataframe
    df = pd.read_csv("EV_2026.B24", sep=";")

    t = df.iloc[:,0] # in seconds

    sinais = list(df.columns.values)[1:]
    for i in range(len(sinais)):
        # in m /s^2
        acel_i = df.iloc[:, i + 1] # skip 0, cause is time

        # 9. variacao temporal das grandezas
        plot_sinal_graph(t, acel_i, sinais[i])

        # 10. determinar e apresentar o espetro unilateral de amplitude
        (f, Y) = FFT(t, acel_i.values)
        plot_single_sided_spectrum(f, Y, sinais[i])


def FFT(t, y):
    N = len(t) # data length
    T = t[1] - t[0] # from data
    # espetro unilateral de magnitude, de 0 ate freq de Nyquist
    # O resto corresponde freq negativa da transformada de fourier, real signal, is a mirror  
    n_uni = N//2
    f = fftfreq(N, T)[:n_uni]

    # FFT to get: single-sided magnitude spectrum
    Y = fft(y)
    
    # To get single-sided magnitude spectrum, we need to do:
    # The two-sided amplitude spectrum, where the spectrum in the positive frequencies is the complex conjugate of the spectrum in the negative frequencies, has half the peak amplitudes of the time-domain signal.
    # Also, we need to rescale, dividing by N
    Y = 2 / N * np.abs(Y[:n_uni])
    # DC (0 Hz) is unique in the FT
    Y[0] = Y[0] / 2
    # Nyquist frequency is unique for even N, so we shall not multiply by 2, so we revert the previous multiplication
    if N % 2 == 0:
        Y[-1] = Y[-1] / 2
    return (f, Y)


def get_freq_peaks(f, y, signal_name, height_threshold=0.05):
    peaks_index, properties = find_peaks(np.abs(y), height=height_threshold)
    print('Peaks of signal ' + signal_name)
    print("Frequency: \t Magnitude:")
    [print("%4.4f    \t %3.4f" %(f[peaks_index[i]], properties['peak_heights'][i])) for i in range(len(peaks_index))]
    return peaks_index, properties


def plot_sinal_graph(t, signal, signal_name):
    # Visualization
    plt.figure(figsize=IMAGE_SIZE)

    # Original signal
    plt.plot(t, signal.values, linewidth=0.5)
    plt.title("Variação temporal do sinal " + signal_name)
    plt.xlabel("Tempo [s]")
    plt.ylabel("Aceleracao [m/s^2]")
    plt.grid()

    plt.tight_layout()
    plt.savefig("results/sinal-"+signal_name+".png")
    if SHOW_IMAGES:
        plt.show()


def plot_single_sided_spectrum(f, ftt_signal, signal_name):
    
    # get peaks
    peaks_index, properties = get_freq_peaks(f, ftt_signal, signal_name)

    # Visualization
    plt.figure(figsize=IMAGE_SIZE)

    # Spectral
    plt.plot(f, ftt_signal, '-', f[peaks_index],properties['peak_heights'],'x')
    plt.title("Espetro unilateral de amplitude do sinal " + signal_name)
    plt.xlabel("Freq [Hz]")
    plt.ylabel("Magnitude |X(freq)|")
    plt.grid()

    plt.tight_layout()
    plt.savefig("results/espetro-"+signal_name+".png")
    if SHOW_IMAGES:
        plt.show()


if __name__ == "__main__":
    main()