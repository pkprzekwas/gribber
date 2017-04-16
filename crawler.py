import re
import json

import requests
from bs4 import BeautifulSoup

from sender import send_email
from config import NCDC_ROOT, GMAIL_USER, PASSWORD, LAST_TWO_YEARS

def check_if_exists(url=None):
    r = requests.head(url)
    return r.status_code

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

def crawl():
    grib_ctr = 0
    day_ctr = 0
    response = {}
    months_soup = get_soup(url=NCDC_ROOT)
    months = extract_months(soup=months_soup)
    for month in reversed(months):
        month_url = '{}{}'.format(NCDC_ROOT, month)
        response[month_url] = {}
        days_soup = get_soup(month_url)
        days = extract_days(soup=days_soup)
        for day in days:
            day_url = '{}/{}'.format(month_url, day)
            gribs = get_gribs(day)
            response[month_url][day_url] = {}
            for grib in gribs:
                grib_url = '{}/{}'.format(day_url, grib)
                status = check_if_exists(grib_url)
                response[month_url][day_url][grib_url] = status
            grib_ctr += len(gribs)
        send_email(user=GMAIL_USER, pwd=PASSWORD, recipient='rzepka94@gmail.com',\
                   subject='GFS raport - {}'.format(day), body=json.dumps(response))
        day_ctr += len(days)
    send_email(user=GMAIL_USER, pwd=PASSWORD, recipient='rzepka94@gmail.com',\
               subject='GFS raport - Finished', body='Finished')

if __name__ == '__main__':
    main()

