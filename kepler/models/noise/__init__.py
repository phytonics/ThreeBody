from kepler.core import LightCurve, LightCurveAction
import lightkurve as lk

def removeNoise(tpf: lk.KeplerTargetPixelFile):
    """ Removes Instrument noise from the light curve.
    
    This function uses the lightkurve library to perform this function
    The SFF and PLD correctors are used for noise reduction
    A corrector for the curve is created and then applied to itself.
    The result of that is returned.

    NOTE: This function will count exoplanet transits as noise

    Parameters
    -----------------------------------------
    tpf: 
        A valid target pixel file form Kepler

    Returns
    -----------------------------------------
    LightCurve
        The light curve with reduced instrument noise

    Diagnostics
        Some values describing the extent of PLD corrector performance
    """


    """
    1) Why not Linear Regression?
    
    This is only required for TESS Data as it has scattered light background signal.
    As Kepler does not have this issue, it is not used.

    2) Why Self Flat Fielding (SFF)?

    This is only required for K2 data as it has spacecraft motion noise.
    As a result, we need to use it for noise reduction

    3) Why Pixel Light Decorrelation (PLD)?

    It removes instrument noise from the lightcurve

    TODO Understand and use CBV Corrector
    """

    # PLD corrector
    pld = tpf.to_corrector('pld')
    lc_pld = pld.correct()

    # SFF corrector
    sff = lc_pld.to_corrector("sff")
    correct_lc = sff.correct()
    
    return (LightCurve(correct_lc, tpf.id), pld.diagnose())


class NoiseReduction(LightCurveAction):
    def perform(self, lc):
        return reduceNoise(lc)
