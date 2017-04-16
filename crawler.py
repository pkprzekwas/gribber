import os
import re
import json

import requests
import pygrib
from bs4 import BeautifulSoup

from sender import send_email
from mongo import db
from config import NCDC_ROOT, GMAIL_USER, PASSWORD, \
                   LAST_TWO_YEARS, RECEIVER, TEMP_GRB

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
    send_email(user=GMAIL_USER, pwd=PASSWORD, recipient=RECEIVER,\
               subject='GFS raport - Finished', body='Finished')

def crawl_month(month='201704', body=None):
    """Preferred start function"""
    url = '{}/{}'.format(NCDC_ROOT, month)
    body[url] = {}
    days_soup = get_soup(url)
    days = extract_days(soup=days_soup)
    for day in days:
        crawl_day(day, url, body)
        break
    send_email(user=GMAIL_USER, pwd=PASSWORD, recipient=RECEIVER,\
               subject='GFS raport - {}'.format(url), body=json.dumps(body))

def crawl_day(day='20170401', url=None, body=None):
    day_url = '{}/{}'.format(url, day)
    gribs = get_gribs(day)
    body[url][day_url] = {}
    for grib in gribs:
        grib_url = '{}/{}'.format(day_url, grib)
        status = check_if_exists(grib_url)
        body[url][day_url][grib] = status
        if status == 200:
            save_grib(grib_url)

def check_if_exists(url=None):
    r = requests.head(url)
    return r.status_code

def save_grib(url):
    response = requests.get(url)
    if response.status_code == 200:
        with open(TEMP_GRB, 'wb') as f:
            f.write(response.content)
        grbs = pygrib.open(TEMP_GRB)
        grb = grbs.message(4)
        data = grb.values.tolist()
        db_doc = {
            'url': url,
            'data': data,
        }
        db.gribs.insert_one(db_doc)
        os.remove(TEMP_GRB)

