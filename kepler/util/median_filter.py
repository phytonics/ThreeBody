import numpy as np
from kepler.util.base import find_index_above_threshold

def median_filter(x, y, num_bins, bin_width=None, x_min=None, x_max=None):
    if num_bins >= 2 and len(x) >= 2 and len(x) == len(y):
        if x_min is None: x_min = x[0]
        if x_max is None: x_max = x[-1]
        if x_min < x_max and x_min < x[-1]:
            if bin_width is not None: bin_width = (x_max - x_min) / num_bins
            if 0 < bin_width < x_max - x_min:
                bin_spacing = (x_max - x_min - bin_width) / (num_bins - 1)
                result = []
                j_start = j_end = find_index_above_threshold(x, x_min)
                bin_min, bin_max = x_min, x_min + bin_width
                for i in range(num_bins):
                    j_start = find_index_above_threshold(x, bin_min, j_start)
                    j_end = find_index_above_threshold(x, bin_max, j_end)
                    result.append(np.median(y[j_start:j_end]) if j_end > j_start else y)
                    bin_min += bin_spacing
                    bin_max += bin_spacing

                return np.array(result)
    raise ValueError("This won't work due to some reason that I don't want to notify you about because the developer of this code is lazy")



