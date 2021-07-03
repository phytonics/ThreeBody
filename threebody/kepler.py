import lightkurve as lk
from lightkurve.lightcurve import KeplerLightCurve
import os
from typing import Union, List, Callable, Any


def getKplrIds() -> List[int]:
    """
    :returns: A list containing all the certified Kepler Ids.
    """
    with open("data/kepler_ids.txt") as ids_file:
        ids = list(map(int, ids_file.readlines()))
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


__all__ = [
    "retrieveKeplerLightCurve", "getKplrIds", "analyseKeplerLightCurve", "getKplrId"
]
