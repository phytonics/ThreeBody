"""This didnt work out
B-spline didnt work well with the data
Ignore this file
"""

import numpy as np
import warnings
from pydl.pydlutils import bspline
from kepler.util import *

""" Custom Error for Handling Spline Errors
Extends inbuilt Exception class
"""
class SplineError(Exception): pass

def interpolate_masked_spline(all_time, all_masked_time, all_masked_spline):
    return [np.interp(time, masked_time, masked_spline) if len(masked_time) > 0 else np.full_like(time, np.nan) for time, masked_time, masked_spline in zip(all_time, all_masked_time, all_masked_spline)]

def kepler_spline(time, flux, bkspace=1.5, maxiter=5, outlier_cut=3):
    t_min, t_max = np.min(time), np.max(time)
    time = (time - t_min) / (t_max - t_min)
    bkspace /= t_max - t_min
    spline = mask = None
    for i in range(maxiter):
        if spline is None: mask = np.ones_like(time, dtype=np.bool)
        else:
            new_mask = robust_mean(flux - spline, cut=outlier_cut)[-1]
            if np.all(new_mask == mask): break
            mask = new_mask
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                curve = bspline.iterfit(time[mask], flux[mask], bkspace=bkspace)[0]
            spline = curve.value(time)[0]
        except:
            return
    
    return spline, mask


def choose_kepler_spline(time, flux, bkspaces, maxiter=5, penalty_coeff=1.0, verbose=True):
    abs_deviations = np.abs(flux[1:] - flux[:-1])
    sigma = np.median(abs_deviations) * 1.48 / np.sqrt(2)
    best_bic = best_spline = best_spline_mask = best_bkspace = None
    bad_bkspaces = []
    for bkspace in bkspaces:
        nparams = npoints = ssr = 0
        spline, spline_mask, bad_bkspace = [], [], False
        for time, flux in zip(time, flux):
            if len(time) < 4:
                spline.append(flux)
                spline_mask.append(np.ones_like(flux))
                continue
            response = kepler_spline(time, flux, bkspace=bkspace, maxiter=maxiter)
            if response is None:
                if verbose: warnings.warn("Bad bkspace")
                bad_bkspaces.append(bkspace)
                bad_bkspace = True
                break

            spline_piece, mask = response

            spline.append(spline_piece)
            spline_mask.append(mask)
            nparams += int((np.max(time) - np.min(time)) / bkspace) + 3
            npoints += np,sum(mask)
            ssr += np.sum((flux[mask] - spline_piece[mask]) ** 2)

        if bad_bkspace: continue
        bic = npoints * np.log(2 * np.pi * sigma ** 2) + ssr / sigma ** 2 + penalty_coeff * nparams * np.log(npoints)
        if best_bic is None or bic < best_bic:
            best_bic = bic
            best_spline = spline
            best_spline_mask = spline_mask
            best_bkspace = bkspace

    return best_spline, best_spline_mask, best_bkspace, bad_bkspaces


def process_light_curve(all_time, all_flux, max_gap_width=0.75):
    all_time, all_flux = split(all_time, all_flux, gap_width=0.75)

    bkspaces = np.logspace(np.log10(0.5), np.log10(20), num=20)
    spline = choose_kepler_spline(all_time, all_flux, bkspaces, penalty_coeff=1.0, verbose=False)
    if spline is None: return None
    time = np.concatenate(all_time)
    flux = np.concatenate(all_flux)
    spline = np.concatenate(spline)

    finite_i = np.isfinite(spline)
    time = time[finite_i]
    flux = flux[finite_i]
    spline = spline[finite_i]

    flux /= spline

    return time, flux

def phase_fold_and_sort_light_curve(time, flux, period, t0):
    time = phase_fold_time(time, period, t0)
    sorted_i = np.argsort(time)
    time = time[sorted_i]
    flux = flux[sorted_i]

    return time, flux

def generate_view(time, flux, num_bins, bin_width, t_min, t_max, normalize=True):
    view = median_filter(time, flux, num_bins, bin_width, t_min, t_max)
    if normalize:
        view -= np.median(view)
        view /= np.abs(np.min(view))
    
    return view
