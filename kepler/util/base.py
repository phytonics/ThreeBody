# kepler.util.base.py
import numpy as np

def find_index_above_threshold(arr, threshold, start=0, end=None):
    for i in range(start, len(arr) if end is None else end):
        if arr[i] >= threshold: break
    return i

def phase_fold_time(time, period, t0):
    return np.mod(time + (period/2 - t0), period) - period/2


def split(all_time, all_flux, gap_width=0.75):
    if np.array(all_time).ndim == 1: all_time, all_flux = [all_time], [all_flux]
    out_time, out_flux = [], []
    for time, flux in zip(all_time, all_flux):
        start = 0
        for end in range(1, len(time) + 1):
            if end == len(time) or time[end] - time[end - 1] > gap_width:
                out_time.append(time[start:end])
                out_flux.append(flux[start:end])
                start = end

    return out_time, out_flux
