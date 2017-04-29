import os

from config import BASE_DIR


class GribStore:
    def __init__(self):
        self.dir = os.path.join(BASE_DIR, 'gribs')

    @property
    def gribs(self):
        return sorted(os.listdir(self.dir))

    def last_grib(self):
        return self.gribs[0]

    def _last_grib_splited(self):
        grb = self.get_last_grib()
        return grb.split('_')

    def last_gribs_date(self):
        return self._last_grib_splited()[2]

    def last_gribs_month(self):
        date = self.get_last_grib_as_date()
        return date[:4]

    def last_gribs_hour(self):
        return self._last_grib_splited()[3]
