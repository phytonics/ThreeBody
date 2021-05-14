import lightkurve as lk
from astroquery.mast import Observations
from astropy.timeseries import TimeSeries

def retrieveCollection(kplrId):
    search_result = lk.search_lightcurve(f'KIC {kplrId}', mission='Kepler')
    # Download and stitch the data together
    lc = search_result.download_all().stitch()
    lc.plot()
    return lc



