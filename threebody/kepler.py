import lightkurve as lk
from lightkurve.lightcurve import KeplerLightCurve
import os
import pandas as pd
from typing import Union, List, Callable, Any, Tuple


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


def retrieveExoplanetArchives() -> pd.DataFrame:
    """
    :returns: DataFrame of TCE Data.
    """
    return pd.read_csv("data/kepler_tce.csv").set_index("kepid")


def getExoplanetArchiveIds() -> List[int]:
    """
    :returns: A list containing all the certified Kepler Ids that are Exoplanet Archives.
    """
    return list(retrieveExoplanetArchives().kepid)


def getExoplanetArchiveId(index: int = 0) -> int:
    """
    :param index: Literally the index you want from the Exoplanet Archive Ids List
    :returns: Kepler Id as an Integer
    """
    return getExoplanetArchiveIds()[index]


def retrieveExoplanetArchive(kplrId: Union[int, str, float]) -> pd.Series:
    """
    :param kplrId: The Kepler Id, as an Integer, String or Float
    :return: The TCE Data
    """
    df = retrieveExoplanetArchives()
    return df.loc[int(kplrId)]


def analyseExoplanetArchive(kplrId: Union[int, str, float], func: Callable[[pd.Series], Any]) -> Any:
    """
    :param kplrId: The Kepler Id, as an Integer, String or Float
    :param func: The function to be ran, with the modified pd.Series as a parameter
    :return: Result of func
    """
    data = retrieveExoplanetArchive(kplrId)
    return func(data)


def retrieveCompleteExoplanetArchive(kplrId: Union[int, str, float]) -> Tuple[pd.Series, KeplerLightCurve]:
    """
    :param kplrId: The Kepler Id, as an Integer, String or Float
    :return: A Tuple containing the TCE Data and Kepler Light Curve Data
    """
    return retrieveExoplanetArchive(kplrId), retrieveKeplerLightCurve(kplrId)


def analyseCompleteExoplanetArchive(kplrId: Union[int, str, float], func: Callable[[pd.Series, KeplerLightCurve], Any]) -> Any:
    """
    :param kplrId: The Kepler Id, as an Integer, String or Float
    :param func: The function to be ran, with the modified KeplerLightCurve and pd.Series as a parameter
    :return: Result of func
    """
    data, klc = retrieveCompleteExoplanetArchive(kplrId)
    result = func(data, klc)
    klc.delete()
    del klc
    return result



__all__ = [
    "getKplrId", "getKplrIds",
    "retrieveKeplerLightCurve", "analyseKeplerLightCurve",
    "getExoplanetArchiveIds", "getExoplanetArchiveId",
    "retrieveExoplanetArchives", "retrieveExoplanetArchive", "analyseExoplanetArchive",
    "retrieveCompleteExoplanetArchive", "analyseCompleteExoplanetArchive"
]
