"""
Event class, which represents a periodic event in a light curve.
"""

import numpy as np
from dataclasses import dataclass

@dataclass
class Event:
    """
    Represents a periodic event in a light curve.
    """
    # Period of the event, in days.
    period: float
    # Duration of the event, in days.
    duration: float
    # Time of the first occurrence of the event, in days.
    t0: float

    def __eq__(self, other: Event) -> bool:
        return self.equals(other)

    def equals(self, other_event: Event, period_rtol=0.001, t0_durations=1) -> bool:
        """
        Compares this Event to another Event, within the given tolerance.
        
        other_event: An Event.
        period_rtol: Relative tolerance in matching the periods.
        t0_durations: Tolerance in matching the t0 values, in units of the other Event's duration.
        
        Returns True if this Event is the same as other_event, within the given tolerance.
        """
        # First compare the periods.
        period_match = np.isclose(
            self.period, other_event.period, rtol=period_rtol, atol=1e-8)
        if not period_match:
            return False

        """
        To compare t0, we must consider that self.t0 and other_event.t0 may be at different phases.
        Just comparing mod(self.t0, period) to mod(other_event.t0, period) does not work because two similar values could end up at different ends of [0, period).
        Define t0_diff to be the absolute difference, up to multiples of period. This value is always in [0, period/2).
        """
        t0_diff = np.mod(self.t0 - other_event.t0, other_event.period)
        if t0_diff > other_event.period / 2:
            t0_diff = other_event.period - t0_diff

        return t0_diff < t0_durations * other_event.duration
