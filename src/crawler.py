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

        for month in months:
            self._crawl_month(month)

    def _crawl_month(self, month):
        url = '{}/{}'.format(NCDC_ROOT, month)

        d_ext = GFSExtractor(root=url)
        days = d_ext.extract_days()

        for day in days:
            self._crawl_day(day, url)

    def _crawl_day(self, day, url=None):
        day_url = '{}/{}'.format(url, day)
        gribs = self._get_full_gribs(day)

        for grib in gribs:
            if grib in self.gs.gribs:
                logger.info('{} already stored. Omitting...'.format(grib))
                continue

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

    def _get_full_gribs(self, day=None):
        _schema = 'gfsanl_4_{}_{}00_000.grb2'
        _hours = ['18', '12', '06', '00']
        return [_schema.format(day, h) for h in _hours]
