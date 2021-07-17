from .kepler import LightCurve
from typing import Any


def plotKeplerLightCurve(klc: LightCurve) -> Any:
    """
    :param klc: The LightCurve object
    :returns: The axes upon which the data has been plotted
    """
    ax = klc.plot()
    ax.set_title(f"Light curve of KIC {klc.id}")
    return ax


def plotKeplerSAPLightCurve(klc: LightCurve) -> Any:
    """
    :param klc: The LightCurve object
    :returns: The axes upon which the data has been plotted
    """
    ax = klc.plot(column='sap_flux', normalize=True)
    ax.set_title(f"SAP Flux Light curve of KIC {klc.id}")
    return ax


def plotKeplerPDCSAPLightCurve(klc: LightCurve) -> Any:
    """
    :param klc: The LightCurve object
    :returns: The axes upon which the data has been plotted
    """
    ax = klc.plot(column='pdcsap_flux', normalize=True)
    ax.set_title(f"PDCSAP Flux Light curve of KIC {klc.id}")
    return ax


__all__ = [
    "plotKeplerLightCurve", "plotKeplerSAPLightCurve", "plotKeplerPDCSAPLightCurve"
]
