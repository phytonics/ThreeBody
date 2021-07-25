from kepler.core import LightCurve, LightCurveAction

def reduceNoise(lc: LightCurve):
    """
    Removes Instrumental noise from the light curve.
    
    This function uses the lightkurve library to perform this function
    The lightkurve library uses Pixel Level Decorrelation (PLD)
    A corrector for the curve is created and then applied to itself.
    The result of that is returned.

    NOTE: The intention of this function is to count exoplanet transits as noise

    :param lc: The original light curve
    :return The light curve with reduced instrumental noise, and some values describing the extent of the noise reduction.
    """

    pld = lc.to_corrector('pld')
    correct_lc = pld.correct()

    # Some instructions:
    # if you could, could you please research a bit more about noise reduction algorithms?

    return LightCurve(correct_lc, lc.id), pld.diagnose()


class NoiseReduction(LightCurveAction):
    def perform(self, lc):
        return reduceNoise(lc)
