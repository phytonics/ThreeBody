from lightkurve.lightcurve import KeplerLightCurve
from typing import Any


def plotKeplerLightCurve(klc: KeplerLightCurve) -> Any:
    """
    :param klc: The KeplerLightCurve object
    :returns: The axes upon which the data has been plotted
    """
    ax = klc.plot()
    ax.set_title(f"Light curve of {klc.id}")
    return ax

def plotKeplerSAPLightCurve(klc: KeplerLightCurve) -> Any:
    """
    :param klc: The KeplerLightCurve object
    :returns: The axes upon which the data has been plotted
    """
    ax = klc.plot(column='sap_flux', normalize=True)
    ax.set_title(f"SAP Flux Light curve of {klc.id}")
    return ax

def plotKeplerPDCSAPLightCurve(klc: KeplerLightCurve) -> Any:
    """
    :param klc: The KeplerLightCurve object
    :returns: The axes upon which the data has been plotted
    """
    ax = klc.plot(column='pdcsap_flux', normalize=True)
    ax.set_title(f"PDCSAP Flux Light curve of {klc.id}")
    return ax
