import os

from pymongo import MongoClient

class SingletonType(type):
    def __call__(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(SingletonType, cls).__call__(*args, **kwargs)
            return cls.__instance

class DBConn(object):
    __metaclass__ = SingletonType

    def __init__(self):
        self.client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
        self.db = self.client.gribs

db_conn = DBConn()
db = db_conn.db

