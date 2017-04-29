import re

import requests
from bs4 import BeautifulSoup

from config import NCDC_ROOT, LAST_TWO_YEARS


class GFSExtractor:
    def __init__(self, root):
        r = requests.get(root)
        data = r.text
        soup = BeautifulSoup(data, 'html.parser')
        self.soup = soup

    def extract_months(self):
        if self.soup is None:
            raise ValueError('Soup object is None')

        months = self.soup.find_all('a', href=re.compile(r'^\d{1,6}'))
        months = {month['href'][:-1] for month in months}
        return reversed(sorted(list(months))[LAST_TWO_YEARS:])

    def extract_days(self):
        if self.soup is None:
            raise ValueError('Soup object is None')

        days = self.soup.find_all('a', href=re.compile(r'^\d{1,8}'))
        days = {day['href'][:-1] for day in days}
        return reversed(sorted(list(days)))
