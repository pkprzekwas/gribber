import os

import pygrib
import numpy as np

from config import BASE_DIR
from logger import logger

OUT_PATH = os.path.join(BASE_DIR, 'out')


class Grib:
    U_WIND_SPEED_10M = 265
    V_WIND_SPEED_10M = 266

    def __init__(self, name=None, data=None, path=None):
        self.name = name
        self.data = data
        self.path = path

    @classmethod
    def save(cls, name, data):
        temp_path = os.path.join(BASE_DIR, 'gribs', name)
        grib = cls(name, data, temp_path)
        with open(temp_path, 'wb') as f:
            f.write(data)
        grib._extract_array(temp_path)
        os.remove(temp_path)

    def _extract_array(self, path):
        try:
            grb = pygrib.open(path)
            aws = self._cnt_ang_wind_speed(grb)
            np.save(os.path.join(OUT_PATH, self.name), aws)
            logger.info('File saved {}'.format(self.name))
        except (RuntimeError, IOError) as e:
            logger.error('Ommiting {}. Problem: {}'.format(self.name, e))
        finally:
            grb.close()

    def _cnt_ang_wind_speed(self, grb):
        _u = grb.message(self.U_WIND_SPEED_10M).values
        _v = grb.message(self.V_WIND_SPEED_10M).values
        return np.sqrt( _u**2 + _v**2 )

    @staticmethod
    def out_dir_check():
        if not os.path.exists(OUT_PATH):
            logger.info('Out dir not found. Creating ...')
            os.makedirs(OUT_PATH)
        if not os.path.exists(os.path.join(BASE_DIR, 'gribs')):
            os.makedirs(os.path.join(BASE_DIR, 'gribs'))

