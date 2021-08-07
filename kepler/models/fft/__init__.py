# fft/__init__.py

from scipy.fftpack import fft
import numpy as np

def getFFT(x):
    return [(fftarr, getReal(fftarr), getImag(fftarr), psd(fftarr)) for fftarr in [fft(x)]][0]

def getReal(fftarr):
    return np.vectorize(lambda c: c.real)(fftarr)

def getImag(fftarr):
    return np.vectorize(lambda c: c.imag)(fftarr)

def psd(fftarr):
    return np.abs(fftarr) ** 2
