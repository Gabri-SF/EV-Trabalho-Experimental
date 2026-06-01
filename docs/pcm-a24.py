import numpy as np
from scipy.fftpack import fft, fftfreq, rfft
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import pandas as pd



def main(): 
    # read csv to dataframe
    df = pd.read_csv("EV_2026.A24", sep=";")

    t = df.iloc[:,0] # in seconds
    
    sinais = list(df.columns.values)[1:]
    for i in range(len(sinais)):
        # in m /s^2
        acel_i = df.iloc[:, i + 1] # skip 0, cause is time
        (f, Y) = FFT(t, acel_i.values)
        plot_sinal_graph(t, acel_i, sinais[i], f, Y)

        play_data_as_audio(acel_i.values, 1000)


        


def play_data_as_audio(data, sample_rate):
    int16_audio = (data * 32767).astype(np.int16)
    p = pyaudio.PyAudio()
    stream = p.open(  
        format=pyaudio.paInt16,  
        channels=1,  
        rate=sample_rate,  
        output=True,  
    ) 
    stream.write(int16_audio.tobytes())

    # Cleanup  
    stream.stop_stream()  
    stream.close()  
    p.terminate()

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
    # no need to multiply by 2 because these amplitudes correspond to the zero and Nyquist frequencies, they dont have complex conjugate in negative freq
    Y[0] = Y[0] / 2
    Y[-1] = Y[-1] / 2
    return (f, Y)


def get_freq_peaks(f, y, signal_name, height_threshold=0.05):
    peaks_index, properties = find_peaks(np.abs(y), height=height_threshold)
    print('Peaks of signal ' + signal_name)
    print("Frequency: \t Magnitude:")
    [print("%4.4f    \t %3.4f" %(f[peaks_index[i]], properties['peak_heights'][i])) for i in range(len(peaks_index))]
    return peaks_index, properties


def plot_sinal_graph(t, signal, signal_name, f, ftt_signal):
    
    # get peaks
    peaks_index, properties = get_freq_peaks(f, ftt_signal, signal_name)

    # Visualization
    plt.figure(figsize=(10, 4))

    # Original signal
    plt.subplot(1, 2, 1)
    plt.plot(t, signal.values)
    plt.title("Variação temporal do sinal")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Aceleracao (m/s^2)")

    # Spectral
    plt.subplot(1, 2, 2)
    plt.plot(f, ftt_signal, '-', f[peaks_index],properties['peak_heights'],'x')
    plt.title("Espetro unilateral de amplitude")
    plt.xlabel("Freq (Hz)")
    plt.ylabel("Magnitude |X(freq)|")

    plt.tight_layout()
    plt.suptitle("Sinal " + signal_name)
    plt.show()


if __name__ == "__main__":
    main()