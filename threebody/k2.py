import lightkurve as lk
from lightkurve.lightcurve import KeplerLightCurve
import os
from typing import Union, List, Callable, Any

def getK2Ids() -> List[int]:
    """
    :returns: A list containing all the certified K2 Ids.
    """
    ids_file = open("../data/k2_ids.txt")
    ids = list(map(int, ids_file.readlines()))
    ids_file.close()
    return ids

def getK2Id(index: int = 0) -> int:
    """
    :param index: Literally the index you want from the K2 Ids List
    :returns: K2 Id as an Integer
    """
    return getK2Ids()[index]

def retrieveK2LightCurve(k2Id: Union[int, str, float]) -> KeplerLightCurve:
    """
    :param k2Id: The Kepler Id, as an Integer, String or Float
    :returns: A KeplerLightCurve object
    """
    k2Id = int(k2Id)
    search_result: lk.SearchResult = lk.search_lightcurve(f'EPIC {k2Id}', mission='K2')
    klc: KeplerLightCurve = search_result.download()
    klc.id = k2Id
    klc.filename = klc.meta["FILENAME"]
    klc.delete = lambda self: os.remove(self.filename)
    return klc


def plotK2LightCurve(klc: KeplerLightCurve) -> Any:
    """
    :param klc: The KeplerLightCurve object
    :returns: The axes upon which the data has been plotted
    """
    # ax = klc.plot(column='pdcsap_flux', label='PDCSAP Flux', normalize=True)
    # klc.plot(column='sap_flux', label='SAP Flux', normalize=True, ax=ax)
    ax = klc.plot()
    ax.set_title(f"Light curve of {klc.id}")
    return ax

def analyseK2LightCurve(k2Id: Union[int, str, float], func: Callable[[KeplerLightCurve], Any]) -> Any:
    """
    :param k2Id: The Kepler Id, as an Integer, String or Float
    :param func: The function to be ran, with the modified KeplerLightCurve as a parameter
    :return: Result of func
    """
    klc = retrieveK2LightCurve(k2Id)
    result = func(klc)
    klc.delete()
    del klc
    return result

