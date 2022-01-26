from kepler.core.curve import LightCurve
from kepler.core.base import LightCurveAction

"""
A class encapsulating a pipline.
Performs the actions given on construction in order

Attributes
----------
actions: List[ Callable[LightCurve] ]
    The actions to perform in order

Methods
----------
__init__(self, *args)
    *args is the actions to perform in order

perform(self, lc):
    lc is a lightcurve which will be acted on
    The actions are defined on construction
"""
class LightCurvePipeline(LightCurveAction):
    def __init__(self, *args):
        self.actions = args

    def perform(self, lc: LightCurve):
        for action in self.actions:
            lc = action(lc)
        return lc

