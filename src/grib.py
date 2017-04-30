import os

import pygrib
import numpy as np

from config import BASE_DIR


class Grib:
    OUT_PATH = os.path.join(BASE_DIR, 'out')
    U_WIND_SPEED_10M = 265
    V_WIND_SPEED_10M = 266

    def __init__(self, name, data, path):
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
        grb = pygrib.open(path)
        aws = self._cnt_ang_wind_speed(grb)
        np.save(os.path.join(self.OUT_PATH, self.name), aws)
        grb.close()

    def _cnt_ang_wind_speed(self, grb):
        _u = grb.message(self.U_WIND_SPEED_10M).values
        _v = grb.message(self.V_WIND_SPEED_10M).values
        return np.sqrt( _u**2 + _v**2 )
