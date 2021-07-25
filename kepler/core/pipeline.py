from kepler.core.curve import LightCurve
from kepler.core.base import LightCurveAction


class LightCurvePipeline(LightCurveAction):
    def __init__(self, *args):
        self.actions = args

    def perform(self, lc: LightCurve):
        for action in self.actions:
            lc = action(lc)
        return lc

