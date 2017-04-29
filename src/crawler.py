import os
import re
import json

import requests

from grib import Grib
from logger import logger
from config import NCDC_ROOT
from extractor import GFSExtractor
from grib_store import GribStore

def check_if_exists(url=None):
    r = requests.head(url)
    return r.status_code


def get_name_from_url(url):
    url_as_list = url.split('/')
    name = url_as_list[-1]
    return name


class Crawler:
    def __init__(self):
        self.gs = GribStore()

    def start(self):
        m_ext = GFSExtractor(root=NCDC_ROOT)
        months = m_ext.extract_months()

        last_month = self.gs.last_grib_month()
        months = [m for m in months if m < last_month]

        for month in months:
            self._crawl_month(month)
            logger.info('Month Finished')


    def _crawl_month(self, month='201704'):
        url = '{}/{}'.format(NCDC_ROOT, month)

        d_ext = GFSExtractor(root=url)
        days = d_ext.extract_days()

        last_day = self.gs.last_grib_as_date()
        days = [d for d in days if d < last_day]

        for day in days:
            self._crawl_day(day, url)
            logger.info('Day Finished')


    def _crawl_day(self, day='20170401', url=None):
        day_url = '{}/{}'.format(url, day)
        gribs = self._get_full_gribs(day)

        last_hour = self.gs.last_gribs_hour()
        gribs = [g for g in gribs if g < last_hour]

        for grib in gribs:
            grib_url = '{}/{}'.format(day_url, grib)
            status = check_if_exists(grib_url)
            if status != 200:
                logger.warning('Problem with {}. Skipping...'.format(grib_url))
                continue
            self._save_grib(grib_url)
            logger.info('File saved {}'.format(grib))

    def _save_grib(self, url):
        name = get_name_from_url(url)
        logger.info('Saving {}'.format(name))
        response = requests.get(url)
        if response.status_code == 200:
            Grib.save(name=name, data=response.content)
        else:
            logger.warning('Unable to fetch {}'.format(name))

    @staticmethod
    def _get_full_gribs(day=None):
        _schema = 'gfsanl_3_{}_{}00_000.grb'
        _hours = ['18', '12', '06', '00']
        return [_schema.format(day, h) for h in _hours]
