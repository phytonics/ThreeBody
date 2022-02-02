# fft/__init__.py

from scipy.fftpack import fft
import numpy as np


def getFFT(x):
    """Gets the fourier transform of the curve
    This uses the fft module from scipy

    Parameters
    ----------
    x: array-like
        The data representing the light curve

    Returns
    ----------
    fftarr
        The array representing the fft
    
    r_fftarr
        The real values of the fft

    i_fftarr
        The imaginary values of the fft

    psd
        The power spectral density of the fft
    """
    return [(fftarr, getReal(fftarr), getImag(fftarr), psd(fftarr)) for fftarr in [fft(x)]][0]

def getReal(fftarr):
    """Gets the real values of the fft

    Parameters
    ----------
    fftarr: array-like
        The array representing the fft

    Returns
    ----------
    r_fft
        The real part of every value in fft
    """
    return np.vectorize(lambda c: c.real)(fftarr)

def getImag(fftarr):
    """Gets the imaginary values of the fft

    Parameters
    ----------
    fftarr: array-like
        The array representing the fft

    Returns
    ----------
    i_fft
        The imaginary part of every value in fft
    """
    return np.vectorize(lambda c: c.imag)(fftarr)

def psd(fftarr):
    """Calculates the power spectral density of the fft

    Parameters
    ----------
    fftarr: array-like
        The array representing the fft

    Returns
    ----------
    psd
        The power spectral density of the fft
    """
    return np.abs(fftarr) ** 2
