from kepler import LightCurve
import lightkurve as lk
from matplotlib import axes

def removeNoise(lcID: Union[int, str, float], quarters: int = 3) -> (LightCurve, axes):
    """ Removes Instrument noise from the light curve.
    
    This function uses the lightkurve library to perform this function
    The lightkurve library uses Pixel Level Decorrelation(PLD)
    A corrector for the curve is created and then applied to itself.
    The result of that is returned.

    NOTE: This function will count exoplanet transits as noise

    Parameters
    -----------------------------------------
    lcID: 
        ID of the light curve
        It will be downloaded as a target pixel file
        Ensure that this has a valid target pixel file
    
    quarters: int
        The number of quarters to download
        Reduce this number if function takes too long

    Returns
    -----------------------------------------
    LightCurve
        The light curve with reduced instrument noise

    Diagnostics
        Some values describing the extent of noise reduction
    """

    lc = lk.search_targetpixelfile(f"KIC {lcID}", mission = "Kepler")[:3].download_all().stitch()
    pld = lc.to_corrector('pld')
    correct_lc = pld.correct()

    return (LightCurve(correct_lc, lcID), pld.diagnose())