from kepler.core import LightCurve, LightCurveAction
import lightkurve as lk
import numpy as np

def keplerRemoveNoise(tpfs: lk.TargetPixelFileCollection):
    """ Removes Instrument noise from the light curve.
    
    This function uses the lightkurve library to perform this function
    The SFF, CBV and PLD correctors are used for noise reduction
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
    As Kepler does not have this issue, it is not used to improve performance

    2) Why Self Flat Fielding (SFF)?

    This is only required for K2 data as it has spacecraft motion noise.
    As a result, we need to use it for noise reduction.

    3) Why Pixel Light Decorrelation (PLD)?

    It removes instrument noise from the lightcurve.

    4) Why Cotrending Basis Vector (CBV)?

    It removes systemic trends in lightcurves.
    As CBV has a risk of overfitting and underfitting, 
    I will use the builtin goodness metrics to get the best fit.
    
    The CBV I will be using is Single-Scale and Spike, as Multi-Scale is for detecting exoplanets
    ! The CBV may not be effective (over/under fitted), if necessary refer to diagnostics
    """

    for tpf in tpfs:
        
        # PLD corrector
        pld = tpf.to_corrector('pld')
        lc_pld = pld.correct()

        # SFF corrector
        sff = lc_pld.to_corrector("sff")
        lc_sff = sff.correct()

        # CBV Corrector 
        # TODO: Get this shit to work
        # cbv = lk.CBVCorrector(lc_sff)
        # correct_lc = cbv.correct_elasticnet(
        #     cbv_type = ["SingleScale"],
        #     cbv_indices = ["1"]
        # )

        yield (lc_sff, pld.diagnose()) #, cbv.diagnose())

# TODO: Implement the TESS
def TESSreduceNoise():
    pass
class NoiseReduction(LightCurveAction):
    def perform(self, lc):
        return reduceNoise(lc)

