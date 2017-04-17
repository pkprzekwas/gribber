import os
import re
import json
import pdb # python debugger
import time

import requests
import pygrib
import numpy as np
from bs4 import BeautifulSoup

from sender import send_email
from mongo import db
from config import NCDC_ROOT, GMAIL_USER, PASSWORD, \
                   LAST_TWO_YEARS, RECEIVER, TEMP_GRB

WIND_MESSAGE = 4
DEBUG = False

def get_soup(url=None):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    return soup

def extract_months(soup=None):
    months = soup.find_all('a', href=re.compile(r'^\d{1,6}'))
    months = {month['href'][:-1] for month in months}
    return sorted(list(months))[LAST_TWO_YEARS:]

def extract_days(soup=None):
    days = soup.find_all('a', href=re.compile(r'^\d{1,8}'))
    days = {day['href'][:-1] for day in days}
    return sorted(list(days))

def get_gribs(date=None):
    return ['gfs_4_{}_{}00_000.grb2'.format(date, hour) \
            for hour in ['00', '06', '12', '18']]

def crawl_all():
    """Do not use if not necessary"""
    body = {}
    months_soup = get_soup(url=NCDC_ROOT)
    months = extract_months(soup=months_soup)
    for month in reversed(months):
        crawl_month(month, body)
        break
    print('Finished')
    #send_email(user=GMAIL_USER, pwd=PASSWORD, recipient=RECEIVER,\
    #           subject='GFS raport - Finished', body='Finished')

def crawl_month(month='201704', body=None):
    """Preferred start function"""
    url = '{}/{}'.format(NCDC_ROOT, month)
    body[url] = {}
    days_soup = get_soup(url)
    days = extract_days(soup=days_soup)
    for day in days:
        crawl_day(day, url, body)
        print('Day Finished')
    print('Month Finished')
    #send_email(user=GMAIL_USER, pwd=PASSWORD, recipient=RECEIVER,\
    #           subject='GFS raport - {}'.format(url), body=json.dumps(body))

def crawl_day(day='20170401', url=None, body=None):
    day_url = '{}/{}'.format(url, day)
    gribs = get_gribs(day)
    body[url][day_url] = {}
    for grib in gribs:
        grib_url = '{}/{}'.format(day_url, grib)
        if DEBUG:
            status = check_if_exists(grib_url)
            body[url][day_url][grib] = status
        save_grib(grib_url)
        print('File saved {}'.format(grib))

def check_if_exists(url=None):
    r = requests.head(url)
    return r.status_code

def save_grib(url):
    name = get_name_from_url(url)
    response = requests.get(url)
    if response.status_code == 200:
        with open(TEMP_GRB, 'wb') as f:
            f.write(response.content)
        grbs = pygrib.open(TEMP_GRB)
        grb = grbs.message(WIND_MESSAGE)
        np.save('/tmp/{}'.format(name), grb.values)
        db_doc = {
            'time': time.time(),
            'name': name,
            'url': url,
        }
        db.gribs.insert_one(db_doc)
        grbs.close()
        os.remove(TEMP_GRB)

def get_name_from_url(url):
    url_as_list = url.split('/')
    name = url_as_list[-1]
    return name

