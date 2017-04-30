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
        self.dir = os.path.join(BASE_DIR, 'gribs')

    @property
    def gribs(self):
        return sorted(os.listdir(self.dir))
