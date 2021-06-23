from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import scipy

'''
    uklad rownan dla sin, "bez przybliżania"
    y - tuple kata oraz omegi
    d - stosunek g/l 
'''
def func(y, t, d):
    a, w = y
    return w, -d * np.sin(a * np.pi / 180)


def func0(y, t, d):
    a, w = y
    return w, -d * (a * np.pi / 180)


'''
    wykresy
'''
def allfunc(a0):
    while (a0 < 91):
        res = odeint(func, (a0, w0), ts, args=(d,))
        plt.plot(ts, res[:, 0])
        a0 += 1

    plt.title("Wykres alfa od (t) dla wszystkich alfa od 0 do 90 (bez przybliżenia)")
    plt.xlabel("Czas")
    plt.ylabel("Wychylenie alfa0")
    plt.show()

    a0 = 0
    while (a0 < 91):
        res0 = odeint(func0, (a0, w0), ts, args=(d,))
        plt.plot(ts, res0[:, 0])
        a0 += 1

    plt.title("Wykres alfa od (t) dla wszystkich alfa od 0 do 90 (z przybliżeniem)")
    plt.xlabel("Czas")
    plt.ylabel("Wychylenie alfa0")
    plt.show()

'''
      Fs    - czestotliwosc probkowania
      delF  - krok probkowania
      a0    - poczatkowe wychylenie 
      Tw    - czas probkowania
      w0    - poczatkowa predkosc
      d     - g/l
'''

def FFT(Fs, delF, a0, Tw, w0, d):
    N = int(Fs / delF)
    t = np.linspace(0, Tw, num=N)

    Freq = []
    Freq0 = []

    y = []

    while (a0 < 91):
        if a0 == 0:
            Freq.append(0)
            Freq0.append(0)
            y.append(1)
            a0 += 1
        else:
            res = odeint(func, (a0, w0), t, args=(d,))
            res0 = odeint(func0, (a0, w0), t, args=(d,))

            signal = res[:, 0]
            signal0 = res0[:, 0]

            spectrum = np.fft.fft(signal * np.hanning(N)) #zwraca moc sygnału dla danej czestotliwosci
            spectrum0 = np.fft.fft(signal0 * np.hanning(N))

            F = np.fft.fftfreq(N, t[1] - t[0])

            maks = abs(spectrum) > 0.5 * (max(abs(spectrum)))   #filtr
            maks0 = abs(spectrum0) > 0.5 * (max(abs(spectrum0)))

            Freq.append(F[maks][0])
            Freq0.append(F[maks0][0])

            y.append(Freq0[a0] / Freq[a0])

            a0 += 1

    alfa = list(range(0, 91))
    plt.title("Zależność okresu drgań wahadła T od amplitudy drgań")
    plt.xlabel("Kąt alfa")
    plt.ylabel("F0/F")
    plt.xlim([0, 90])
    plt.plot(alfa, y)
    plt.show()


if __name__ == '__main__':

    # wykresy alfa(t)
    '''
    podaję te same wartości do obydwu funkcji, poniewż mamy porównać wykresy dla tych samych danych
    '''

    w0 = 0
    g = input("Podaj wartość g: ")
    l = input("Podaj długośc linki l: ")
    while True:
        if float(l) != 0:
            d = float((float(g) / float(l)))
            break
        else:
            l = input("Długość linki nie może być równa 0! Proszę podać nową wartość l: ")

    dt = 0.01
    ts = np.arange(0, 100, dt)

    a0 = input("Podaj początkowe wychylenie alfa0 z przedziału[0, 90] ")
    while True:
        if 0 <= int(a0) <= 90:
            res = odeint(func, (a0, w0), ts, args=(d,))
            res0 = odeint(func0, (a0, w0), ts, args=(d,))

            plt.plot(ts, res[:, 0])
            plt.plot(ts, res0[:, 0])

            plt.title(f"Wychylenie od czasu alfa(t), kąt początkowy a0 = {a0}")
            plt.xlabel("czas t")
            plt.ylabel("wychylenie alfa w stopniach")
            plt.show()  # pokazuje wykresy a(t) dla obydwu funkcji
            break
        else:
            print("Podano niepoprawną wartość, wartość kąta musi być całkowita i z przedziału [0, 90].")
            a0 = input("Prosze podać wartość ponownie a0: ")

    allfunc(a0=0)

    # wykres (T/T0)(alfa)

    Fs = 100
    delF = 0.01
    a0 = 0
    Tw = 100000
    w0 = 0
    g2 = input("Podaj wartość g: ")
    l2 = input("Podaj długośc linki l: ")

    while True:
        if l2 != 0:
            d2 = float((float(g2) / float(l2)))
            break
        else:
            print("Długość linki nie może być równa 0!")
            l2 = input("Proszę podać nową wartość l: ")

    FFT(Fs, delF, a0, Tw, w0, d2)