import os
import json
import thread

import pygrib
from bson import json_util
from flask import Flask, Response, redirect, url_for, request, render_template

from crawler import crawl_all
from mongo import db

app = Flask(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))
PATH = '{}/gribs/gfs_4_20170328_0000_000.grb2'.format(dir_path)

@app.route('/')
def gribs():
    _items = db.gribs.find()
    items = [item for item in _items]
    return render_template('todo.html', items=items)

@app.route('/grib')
def get_values():
    grbs = pygrib.open(PATH)
    grb = grbs.message(4)
    data = grb.values.tolist()
    db_doc = {
            'file': PATH,
            'data': data,
        }
    db.gribs.insert_one(db_doc)
    return "OK"

@app.route('/crawl')
def crawler():
    thread.start_new_thread(crawl_all, ())
    return 'Accepted', 202

@app.route('/stats')
def stats():
    return Response(
                json_util.dumps(db.command("dbstats")),
                mimetype='application/json'
            )

if __name__ == '__main__':
    app.run(host='0.0.0.0')

