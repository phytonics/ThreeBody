import lightkurve as lk
from typing import Union
from kepler.core.curve import LightCurve

class LightCurveAction:
    def perform(self, lc: LightCurve):
        return lc

    def __call__(self, lc: LightCurve):
        return self.perform(lc)

