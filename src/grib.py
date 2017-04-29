import os

import pygrib
import numpy as np

from config import BASE_DIR


class Grib:
    OUT_PATH = os.path.join(BASE_DIR, 'out')

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
        # os.remove(temp_path)

    def _extract_array(self, path):
        grbs = pygrib.open(path)
        grb = grbs.message(4)
        np.save(os.path.join(self.OUT_PATH, self.name), grb.values)
        grbs.close()
