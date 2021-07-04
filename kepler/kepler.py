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


class LightCurve:
    def __init__(self, klc: KeplerLightCurve, kplrId: Union[int, str, float]):
        self.klc = klc
        self.id = kplrId

    def __enter__(self):
        return self

    def delete(self):
        os.remove(self.klc.meta["FILENAME"])

    def __del__(self):
        self.delete()

    def __exit__(self):
        self.__del__()

    def __getattr__(self, item):
        return eval(f"self.klc.{item}")


def retrieveKeplerLightCurve(kplrId: Union[int, str, float]) -> LightCurve:
    """
    :param kplrId: The Kepler Id, as an Integer, String or Float
    :returns: A KeplerLightCurve object
    """
    kplrId = int(kplrId)
    search_result: lk.SearchResult = lk.search_lightcurve(f'KIC {kplrId}', mission='Kepler')
    klc: KeplerLightCurve = search_result.download_all().stitch()
    return LightCurve(klc, kplrId)


def analyseKeplerLightCurve(kplrId: Union[int, str, float], func: Callable[[LightCurve], Any]) -> Any:
    """
    :param kplrId: The Kepler Id, as an Integer, String or Float
    :param func: The function to be ran, with the modified KeplerLightCurve as a parameter
    :return: Result of func
    """
    with retrieveKeplerLightCurve(kplrId) as klc:
        return func(klc)


__all__ = [
    "getKplrId", "getKplrIds",
    "retrieveKeplerLightCurve", "analyseKeplerLightCurve",
    "LightCurve"
]
