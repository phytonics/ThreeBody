# fft/__init__.py

from scipy.fftpack import fft
import numpy as np
from numpy import ix_, outer, zeros
from scipy.ndimage.filters import maximum_filter

def getFFT(x):
    return list(map(lambda fftarr: (fftarr, getReal(fftarr), getImag(fftarr), psd(fftarr)), [fft(x)]))[0]


def getReal(fftarr):
    return np.vectorize(lambda c: c.real)(fftarr)

def getImag(fftarr):
    return np.vectorize(lambda c: c.imag)(fftarr)

def psd(fftarr):
    return np.abs(fftarr) ** 2

class Peak:
    def __init__(self, position, data, dataHeight=None, lineWidth=None):
        self.position = np.array(position)
        self.data = data
        self.point = np.round(self.position).astype(int)
        self.dataHeight = data[self.point] if dataHeight is None else dataHeight
        self.lineWidth = self._calcHalfHeightWidth() if lineWidth is None else lineWidth
        self.fitAmplitude = None
        self.fitPosition = None
        self.fitLineWidth = None

    def _calcHalfHeightWidth(self):
        return [(lambda x: x[1] - x[0])(self._findHalfPoints(dim)) for dim in range(self.data.ndim)]

    def _findHalfPoints(self, dim):
        height = abs(self.dataHeight)
        halfHt = 0.5 * height
        data = self.data
        point = self.point
        testPoint = list(point)
        posA = posB = point[dim]
        prevValue = height
        while posA > 0:  # Search backwards
            posA -= 1
            testPoint[dim] = posA
            value = abs(data[tuple(testPoint)])
            if value <= halfHt:
                posA += (halfHt - value) / (prevValue - value)
                break

            prevValue = value

        lastPoint = data.shape[dim] - 1  # Shape is size
        prevValue = height
        while posB < lastPoint - 1:  # Search forwards
            posB += 1
            testPoint[dim] = posB
            value = abs(data[tuple(testPoint)])
            if value <= halfHt:
                posB -= (halfHt - value) / (prevValue - value)
                break
            prevValue = value
        return posA, posB




