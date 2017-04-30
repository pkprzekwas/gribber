import os

from logger import logger
from config import BASE_DIR


class SingletonType(type):
    def __call__(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(SingletonType, cls).__call__(*args, **kwargs)
            return cls.__instance


class GribStore:
    __metaclass__ = SingletonType

    def __init__(self):
        self.dir = os.path.join(BASE_DIR, 'out')

    @property
    def gribs(self):
        np_gribs = sorted(os.listdir(self.dir))
        # trimming '.npy'
        grib_files = [gf[:-4] for gf in np_gribs]
        return grib_files
