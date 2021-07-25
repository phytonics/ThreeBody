import numpy as np
from kepler.util.base import phase_fold_time

def remove_events(all_time, all_flux, events, width_factor=1.0):
    single_segment = np.array(all_time).ndim == 1
    if single_segment: all_time, all_flux = [all_time], [all_flux]
    output_time, output_flux = [], []
    for time, flux in zip(all_time, all_flux):
        mask = np.ones_like(time, dtype=np.bool)
        for event in events:
            mask = np.logical_and(mask, np.abs(phase_fold_time(time, event.period, event.t0)) > 0.5 * width_factor * event.duration)
            output_time, output_flux = (time[mask], flux[mask]) if single_segment else (output_time + [time[mask]], output_flux + [flux[mask]])

    return output_time, output_flux