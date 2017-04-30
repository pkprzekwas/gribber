import os

from logger import logger
from config import BASE_DIR


class GribStore:
    def __init__(self):
        self.dir = os.path.join(BASE_DIR, 'gribs')

    @property
    def gribs(self):
        return sorted(os.listdir(self.dir))

    def _last_grib(self):
        if len(self.gribs) == 0:
            logger.info('No files downloaded yet')
            return
        return self.gribs[0]

    def _last_grib_splited(self):
        grb = self._last_grib()
        if grb is None:
            return
        return grb.split('_')

    def last_gribs_date(self):
        lgs =  self._last_grib_splited()
        if lgs is None:
            return '99999999'
        return lgs[2]

    def last_gribs_month(self):
        date = self.last_gribs_date()
        return date[:6]

    def last_gribs_hour(self):
        lgs = self._last_grib_splited()
        if lgs is None:
            return 25
        return lgs[3][:2]
