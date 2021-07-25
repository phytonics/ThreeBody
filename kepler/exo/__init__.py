from kepler.io.kepler import retrieveKeplerLightCurve, LightCurve
import pandas as pd
from typing import Union, List, Callable, Any, Tuple


def retrieveExoplanetArchives() -> pd.DataFrame:
    """
    :returns: DataFrame of TCE Data.
    """
    tce_table = pd.read_csv("data/kepler_tce.csv").set_index("kepid")
    tce_table["tce_duration"] /= 24  # Convert hours to days.
    tce_table = tce_table[tce_table.av_training_set.apply(lambda l: l in ["PC", "AFP", "NTP"])]
    return tce_table


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
    return retrieveExoplanetArchives().loc[int(kplrId)]


def analyseExoplanetArchive(kplrId: Union[int, str, float], func: Callable[[pd.Series], Any]) -> Any:
    """
    :param kplrId: The Kepler Id, as an Integer, String or Float
    :param func: The function to be ran, with the modified pd.Series as a parameter
    :return: Result of func
    """
    return func(retrieveExoplanetArchive(kplrId))


def retrieveCompleteExoplanetArchive(kplrId: Union[int, str, float]) -> Tuple[pd.Series, LightCurve]:
    """
    :param kplrId: The Kepler Id, as an Integer, String or Float
    :return: A Tuple containing the TCE Data and Kepler Light Curve Data
    """
    return retrieveExoplanetArchive(kplrId), retrieveKeplerLightCurve(kplrId)


def analyseCompleteExoplanetArchive(kplrId: Union[int, str, float], func: Callable[[pd.Series, LightCurve], Any]):
    """
    :param kplrId: The Kepler Id, as an Integer, String or Float
    :param func: The function to be ran, with the modified KeplerLightCurve and pd.Series as a parameter
    :return: Result of func
    """
    with retrieveCompleteExoplanetArchive(kplrId) as (data, klc):
        return func(data, klc)


__all__ = [
    "getExoplanetArchiveIds", "getExoplanetArchiveId",
    "retrieveExoplanetArchives", "retrieveExoplanetArchive", "analyseExoplanetArchive",
    "retrieveCompleteExoplanetArchive", "analyseCompleteExoplanetArchive"
]
