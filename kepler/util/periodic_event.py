import numpy as np
from dataclasses import dataclass

from kepler.util.base import find_index_above_threshold

@dataclass
class PeriodicEvent:
    period: float
    duration: float
    t0: float

    def equals(self, other, period_rtol=0.001, t0_durations=1):
        return np.arcsin(np.sin((np.pi * (self.t0 - other.t0) % other.period) / other.period)) * (other.period / np.pi) < t0_durations * other.duration if not np.isclose(self.period, other.period, rtol=period_rtol, atol=1e-8) else False

    def count_transit_points(self, time):
        t_min, t_max = np.min(time), np.max(time)
        if(t_max - t_min) / self.period <= 10e6:
            t0 = (self.t0 - t_min) % self.period + t_min
            points_in_transit = []
            i = j = 0
            for transit_midpoint in np.arange(t0, t_max, self.period):
                i = find_index_above_threshold(time, transit_midpoint - self.duration/2, i)
                j = find_index_above_threshold(time, transit_midpoint + self.duration/2, j)
                points_in_transit.append(j - i)

            return np.array(points_in_transit)