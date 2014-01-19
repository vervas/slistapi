import os
from pymongo import MongoClient


class MongoConnection():
    def __init__(self, host='localhost', port=27017, db='slistapi', collection=''):
        try:
            uri = os.environ['MONGOLAB_URI']
            client = MongoClient(uri)
            self.db = client.get_default_database()[collection]
        except KeyError:
            client = MongoClient(host, port)
            self.db = client[db][collection]
