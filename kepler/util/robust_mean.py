import numpy as np

def robust_mean(y, cut):
    absdev = np.abs(y - np.median(y))
    sigma = 1.4826 * np.median(absdev)
    sigma = np.std(y[absdev <= cut * (1.253 * np.mean(absdev) if np.log10(sigma) < 24 else sigma)])
    sc = cut if cut > 1 else 1
    if cut <= 4.5:
        sigma /= (-0.15405 + 0.90723 * sc - 0.23584 * sc ** 2 + 0.020142 * sc ** 3)

    mask = absdev <= cut * sigma
    mean, sigma = np.mean(y[mask]), np.std(y[mask])
    if cut <= 4.5:
        sigma /= (-0.15405 + 0.90723 * sc - 0.23584 * sc ** 2 + 0.020142 * sc ** 3)
    mean_stddev = sigma / np.sqrt(len(y) - 1)
    return mean, mean_stddev, mask