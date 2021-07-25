from lightkurve.lightcurve import KeplerLightCurve
from typing import Union
import os

class LightCurve:
    def __init__(self, klc: KeplerLightCurve, kplrId: Union[int, str, float]):
        self.klc = klc
        self.id = kplrId

    def __enter__(self):
        return self

    def __repr__(self):
        return self.klc.__repr__()

    def __str__(self):
        return self.klc.__str__()

    def delete(self):
        os.remove(self.klc.meta["FILENAME"])

    def __del__(self):
        self.delete()

    def __exit__(self):
        self.__del__()

    def __getattr__(self, item):
        return eval(f"self.klc.{item}")

    def __getitem__(self, key):
        return self.klc[key]

    def __setitem__(self, key, value):
        self.klc[key] = value


