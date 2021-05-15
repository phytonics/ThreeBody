import lightkurve as lk
from lightkurve.lightcurve import KeplerLightCurve
import os
from typing import Union, List, Callable, Any

def getKplrIds() -> List[int]:
    """
    :returns: A list containing all the certified Kepler Ids.
    """
    ids_file = open("../data/kepler_ids.txt")
    ids = list(map(int, ids_file.readlines()))
    ids_file.close()
    return ids

def getKplrId(index: int = 0) -> int:
    """
    :param index: Literally the index you want from the Kepler Ids List
    :returns: Kepler Id as an Integer
    """
    return getKplrIds()[index]

def retrieveKeplerLightCurve(kplrId: Union[int, str, float]) -> KeplerLightCurve:
    """
    :param kplrId: The Kepler Id, as an Integer, String or Float
    :returns: A KeplerLightCurve object
    """
    kplrId = int(kplrId)
    search_result: lk.SearchResult = lk.search_lightcurve(f'KIC {kplrId}', mission='Kepler')
    klc: KeplerLightCurve = search_result.download_all().stitch()
    klc.id = kplrId
    klc.filename = klc.meta["FILENAME"]
    klc.delete = lambda self: os.remove(self.filename)
    return klc

def plotKeplerLightCurve(klc: KeplerLightCurve) -> Any:
    """
    :param klc: The KeplerLightCurve object
    :returns: The axes upon which the data has been plotted
    """
    # ax = klc.plot(column='pdcsap_flux', label='PDCSAP Flux', normalize=True)
    # klc.plot(column='sap_flux', label='SAP Flux', normalize=True, ax=ax)
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

def analyseKeplerLightCurve(kplrId: Union[int, str, float], func: Callable[[KeplerLightCurve], Any]) -> Any:
    """
    :param kplrId: The Kepler Id, as an Integer, String or Float
    :param func: The function to be ran, with the modified KeplerLightCurve as a parameter
    :return: Result of func
    """
    klc = retrieveKeplerLightCurve(kplrId)
    result = func(klc)
    klc.delete()
    del klc
    return result

