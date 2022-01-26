from kepler.core import LightCurve, LightCurveAction
import lightkurve as lk
import numpy as np

def keplerRemoveNoise(lc: lk.LightCurve):
    """ Removes Instrument noise from kepler light curve.
    
    This function uses the lightkurve library to perform this function
    The SFF, CBV and PLD correctors are used for noise reduction
    A corrector for the curve is created and then applied to itself.
    The result of that is returned.

    NOTE: This function will count exoplanet transits as noise

    Parameters
    -----------------------------------------
    lc: 
        A valid lightcurve form Kepler

    Returns
    -----------------------------------------
    LightCurve
        The light curve with reduced instrument noise
    """


    """
    1) Why not Linear Regression?
    
    This is only required for TESS Data as it has scattered light background signal.
    As Kepler does not have this issue, it is not used to improve performance

    2) Why Self Flat Fielding (SFF)?

    This is required for Kepler data as it has spacecraft motion noise.
    As a result, we need to use it for noise reduction.

    4) Why not Cotrending Basis Vector (CBV)?

    It removes systemic trends in lightcurves.
    However, Kepler data has little CBV correctors, and SFF is sufficient.
    (Mentioned on Lightkurve 2.0 site)
    """

    # SFF corrector
    sff = lc.to_corrector("sff")
    lc_sff = sff.correct()

    return (lc_sff)

def TESSRemoveNoise():
    """ Removes Instrument noise from TESS light curve

    This function uses the lightkurve library to perform this function.
    ! However, it is currently not working properly.
    
    Parameters
    -----------------------------------------
    lc: 
        A valid lightcurve form TESS

    Returns
    -----------------------------------------
    LightCurve
        The light curve with reduced instrument noise
    """

    pass

def removeNoise(tpfs: lk.TargetPixelFileCollection, source: str = 'kepler'):
    """ Removes Instrument noise from target pixel collection.
    
    This function uses the lightkurve library to perform this function
    Firstly, it uses the PLD corrector to correct the target pixel collection
    The resulting lightcurve is then passed to the respective 

    NOTE: This function should treat exoplanet transits as noise

    Parameters
    -----------------------------------------
    tpfs: TargetPixelFileCollection
        A valid target pixel file collection

    source: str
        A string stating the source of the target pixel file

    Returns
    -----------------------------------------
    LightCurve
        The light curve with reduced instrument noise
    
    Diagnostics
        Multiple graphs representing the corresponding correctors correction extent
    """


    """
    1) Why Pixel Level Decorrelation?

    It removes instrument noise for all kepler and TESS.
    
    * The other correctors will be used in the differentiated functions
    """

    # Differentiating the keplers from the TESS
    source = source.lower()
    assert source in ["tess", 'kepler', 'k2'], "Source not in TESS, Kepler or K2"

    # The compulsory pass through PLDCorrector
    lc_pld = lk.LightCurveCollection([])
    for tpf in tpfs:
        lc_pld.append(tpf.to_corrector('pld').correct())
    
    lc_pld = lc_pld.stitch().remove_outliers().flatten()

    if source == "kepler" or source == "k2":
        return keplerRemoveNoise(lc_pld)
    else:
        return TESSRemoveNoise(lc_pld)

    return lc_pld

class NoiseReduction(LightCurveAction):
    def perform(self, tpfs: lk.TargetPixelFileCollection):
        return removeNoise(tpfs)

