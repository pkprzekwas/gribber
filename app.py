import os
import json

import pygrib
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient(
            os.environ['DB_PORT_27017_TCP_ADDR'],
            27017)
db = client.tododb

dir_path = os.path.dirname(os.path.realpath(__file__))
PATH = '{}/gribs/gfs_4_20170328_0000_000.grb2'.format(dir_path)

@app.route('/')
def todo():
    _items = db.tododb.find()
    items = [item for item in _items]
    return render_template('todo.html', items=items)


@app.route('/new', methods=['POST'])
def new():
    item_doc = {
        'name': request.form['name'],
        'description': request.form['description']
    }
    db.tododb.insert_one(item_doc)
    return redirect(url_for('todo'))

@app.route('/grib')
def get_values():
    grbs = pygrib.open(PATH)
    grb = grbs.message(4)
    data = grb.values.tolist()
    db_doc = {
            'file': PATH,
            'data': data,
        }
    #json_data = json.dumps(db_doc)
    db.gribs.insert_one(db_doc)
    return "OK"

